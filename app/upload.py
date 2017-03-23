import os
import tempfile

import boto3
from flask import request, session, redirect, url_for
from wand.image import Image

from app import config
from app import webapp, celery
from app.classify import classify_image
from app.utils import get_db


@webapp.route('/upload', methods=['POST'])
# Upload a new file and store in the systems temp directory
def file_upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    # check if the post request has the file part
    if 'uploadedfile' not in request.files:
        return "Missing uploaded file"

    new_file = request.files['uploadedfile']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    s3 = boto3.client('s3', **config.conn_args)
    username = str(session['username'])
    s3.create_bucket(Bucket=config.bucket_name)

    with Image(file=new_file) as image:
        fd, path = tempfile.mkstemp(prefix=username + '_')
        key = os.path.basename(path)
        try:
            image.save(filename=path)
            with os.fdopen(fd, 'r') as tmp:
                s3.upload_fileobj(tmp, config.bucket_name, key)
        finally:
            classify.delay(key, path)

    cnx = get_db()
    cursor = cnx.cursor()

    query = '''SELECT id FROM users WHERE login = %s'''
    cursor.execute(query, (username,))
    user_id = cursor.fetchone()[0]

    query = '''INSERT INTO images (userId,imageKey,predict) VALUES (%s,%s,%s)'''
    cursor.execute(query, (user_id, key, 'unpredicted'))
    cnx.commit()

    return redirect(url_for('index'))


def save_to_database(key, predict):
    cnx = get_db()
    cursor = cnx.cursor()

    query = ''' UPDATE images SET predict=%s WHERE imageKey = %s '''
    cursor.execute(query, (predict, key))
    cnx.commit()


@celery.task
def classify(key, tmp_path):
    print('>>>>>>>>>>>>>>>>>>>>>>>>> begin celery predict task <<<<<<<<<<<<<<<<<<<<<<<<<')
    predict = []

    try:
        with webapp.app_context():
            predict = classify_image(tmp_path)

    finally:
        os.remove(tmp_path)
        with webapp.app_context():
            save_to_database(key, str(predict))
        print('>>>>>>>>>>>>>>>>>>>>>>>>> celery predict task done <<<<<<<<<<<<<<<<<<<<<<<<<')
