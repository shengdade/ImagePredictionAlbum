from datetime import timedelta

import boto3
from botocore.client import ClientError
from flask import redirect, render_template, request, session, url_for, escape

from app import config
from app import webapp
from app.utils import get_db, ServerError

webapp.secret_key = '\x96\xc5\xf5\x06\x0fs\x0e\xf0\x15\xd5H\xb3\x03`\xab\xd1U=\x07W\xd1C+\xc3'


@webapp.before_request
def make_session_permanent():
    session.permanent = True
    webapp.permanent_session_lifetime = timedelta(minutes=5)


@webapp.route('/index', methods=['GET'])
@webapp.route('/', methods=['GET'])
# Return html with pointers to the examples
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    else:
        username = str(session['username'])
        cnx = get_db()
        cursor = cnx.cursor()

        query = '''SELECT images.imageKey FROM users, images WHERE users.id = images.userId AND users.login = %s'''
        cursor.execute(query, (username,))

        s3_cli = boto3.client('s3', **config.conn_args)
        url_list = []
        for key in cursor:
            url = s3_cli.generate_presigned_url('get_object', Params={'Bucket': config.bucket_name, 'Key': key[0]},
                                                ExpiresIn=300)
            url_list.append((key[0], url))

        username_session = escape(session['username']).capitalize()
        return render_template('main.html', user_name=username_session, image_list=url_list)


@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        redirect(url_for('index'))

    error = None
    try:
        if request.method == 'POST':

            username_form = request.form['username']
            password_form = request.form['password']

            # handle admin login
            if username_form.strip() == 'admin':
                if password_form == 'admin':
                    return redirect(url_for('admin'))
                else:
                    raise ServerError('Invalid password')

            # connect to database
            cnx = get_db()
            cursor = cnx.cursor()

            # determine whether valid username
            query = "SELECT COUNT(*) FROM users WHERE login = %s"
            cursor.execute(query, (username_form,))
            if not cursor.fetchone()[0]:
                raise ServerError('Invalid username')

            # verify user password
            query = "SELECT password FROM users WHERE login = %s"
            cursor.execute(query, (username_form,))
            if cursor.fetchone()[0] == password_form:
                session['username'] = request.form['username']
                return redirect(url_for('index'))

            raise ServerError('Invalid password')

    except ServerError as e:
        error = str(e)

    return render_template('login.html', error=error)


@webapp.route('/register', methods=['POST'])
def register():
    username_form = request.form['username']
    password_form = request.form['password']

    error = "register successfully, please log in"
    try:
        s3 = boto3.client('s3', **config.conn_args)
        s3.create_bucket(Bucket=config.bucket_name)

        cnx = get_db()
        cursor = cnx.cursor()

        query = "SELECT COUNT(*) FROM users WHERE login = %s"
        cursor.execute(query, (username_form,))
        if cursor.fetchone()[0]:
            raise ServerError('Username already exists')

        query = '''INSERT INTO users (login,password) VALUES (%s,%s)'''
        cursor.execute(query, (username_form, password_form))
        cnx.commit()

    except ServerError as e:
        error = str(e)

    except ClientError as e:
        error = str(e)

    return render_template('login.html', error=error)


@webapp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@webapp.route('/admin')
def admin():
    return 'No admin right now.'


@webapp.route('/a1')
def a1():
    return redirect("http://ece1779-a1-548293034.us-east-1.elb.amazonaws.com", code=302)


@webapp.route('/a1-admin')
def a1_admin():
    return redirect("http://ec2-54-175-182-31.compute-1.amazonaws.com", code=302)
