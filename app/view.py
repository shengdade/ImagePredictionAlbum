import ast

import boto3
from flask import render_template, request, session, redirect, url_for, escape

from . import config
from . import webapp
from .utils import get_db, ServerError


@webapp.route('/view', methods=['POST'])
def image_view():
    key = str(request.form['key'])
    if key == "":
        return redirect(url_for('index'))

    if 'username' not in session:
        return redirect(url_for('login'))

    username = str(session['username'])
    cnx = get_db()
    cursor = cnx.cursor()

    try:
        query = '''SELECT i.imageKey, i.predict
                   FROM users u, images i
                   WHERE u.id = i.userId AND u.login = %s AND i.imageKey = %s;'''
        cursor.execute(query, (username, key))
        row = cursor.fetchone()
        if not row:
            raise ServerError('Invalid image key')

    except ServerError:
        print('ServerError: Invalid image key')
        return redirect(url_for('index'))

    s3_cli = boto3.client('s3', **config.conn_args)
    url = s3_cli.generate_presigned_url('get_object', Params={'Bucket': config.bucket_name, 'Key': row[0]},
                                        ExpiresIn=600)

    predict = row[1]
    if predict != 'unpredicted':
        predict = ast.literal_eval(predict)[0]

    username_session = escape(session['username']).capitalize()
    return render_template('view.html', user_name=username_session, image_url=url, predict=predict)
