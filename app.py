import uuid
import os
import datetime

from flask import Flask, jsonify, request, json, render_template
from flask_cors import CORS

from flask_mysqldb import MySQL

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

from werkzeug.utils import secure_filename

from flask_login import LoginManager, login_user, logout_user, login_required

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'python_flask'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# POSTS
@login_required
@app.route('/API/posts', methods=['GET', 'POST'])
def all_posts():
    cur = mysql.connection.cursor()
    response_object = {'status': 'success'}

    #date
    dt = datetime.datetime.now()
    today = dt.strftime("%Y-%m-%d %H:%M:%S")

    #upload path
    target = os.path.join(APP_ROOT, 'images')
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("couldn't create upload dir: {}".format(target) )
    
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'images/')
        data = json.loads(request.form['postData'])

        if data['date'] == '':
            data['date'] = today

        if data['author'] == 0:
            data['author'] = 1

        print('[#] ', data)

        cur.execute("INSERT INTO posts (`title`, `post_content`, `author`, `date`) VALUES ('" + str(data['title']) + "', '" + str(data['post_content']) + "', '" + str(data['author']) + "', '" + str(data['date']) + "')")
        mysql.connection.commit()
        postID = cur.lastrowid
        print('[#] postID: ', postID)

        for upload in request.files:
            print('[#]: dodaje ', request.files[upload].filename)

            destination = '/'.join([target, request.files[upload].filename])
            request.files[upload].save(destination)

            cur.execute("INSERT INTO photos (`post_id`, `img`) VALUES ('" + str(postID) + "', '" + str(request.files[upload].filename) + "')")
            mysql.connection.commit()

        response_object['message'] = 'Post added!'
        
        print('Post added!')
    else: 
        cur.execute("SELECT * FROM posts")
        query = cur.fetchall()
        response_object['posts'] = query

        for post in response_object['posts']:
            print('[#] ', post['id'])
            cur.execute("SELECT * FROM photos")
            query = cur.fetchall()
            response_object['photos'] = query
            print('[#] ', response_object['photos'])


    cur.close()

    return jsonify(response_object)

@app.route('/API/posts/<post_id>', methods=['PUT', 'DELETE'])
def single_post(post_id):
    cur = mysql.connection.cursor()
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        post_data = request.get_json()
        cur.execute("UPDATE `posts` SET `id`='" + post_id + "',`title`='" + post_data['title'] + "', `post_content`='" + post_data['post_content'] + "', `author`='" + post_data['author'] + "', `date`='" + post_data['date'] + "' WHERE `id`='" + post_id + "'")
        mysql.connection.commit()
        response_object['message'] = 'Post updated!'

    if request.method == 'DELETE':
        cur.execute("DELETE FROM `posts` WHERE `id`='" + post_id + "'")
        mysql.connection.commit()
        response_object['message'] = 'Post removed!'

    return jsonify(response_object)

# TASKS
@app.route('/API/tasks', methods=['GET', 'POST'])
def all_tasks():
    cur = mysql.connection.cursor()
    response_object = {'status': 'success'}

    #date
    dt = datetime.datetime.now()
    today = dt.strftime("%Y-%m-%d %H:%M:%S")
    
    if request.method == 'POST':
        data = request.get_json()
        print('[#] dodaje: ', data)

        if data['date'] == '':
            data['date'] = today
        
        if data['created'] == '':
            data['created'] = today

        data['author'] = 1

        cur.execute("INSERT INTO tasks (`title`, `content`, `author`, `status`, `date`, `created`) VALUES ('" + str(data['title']) + "', '" + str(data['content']) + "', '" + str(data['author']) + "', '" + str(data['status']) + "', '" + str(data['date']) + "', '" + str(data['created']) + "')")
        mysql.connection.commit()
        postID = cur.lastrowid
        # print('[#] postID: ', postID)
        response_object['message'] = 'Task added!'
        
        print('Task added!')
    else: 
        cur.execute("SELECT * FROM tasks")
        query = cur.fetchall()
        response_object['tasks'] = query
        print(query)

    cur.close()

    return jsonify(response_object)

@app.route('/API/tasks/<task_id>', methods=['PUT', 'DELETE'])
def single_task(task_id):
    cur = mysql.connection.cursor()
    response_object = {'status': 'success'}

    if request.method == 'PUT':
        data = request.get_json()

        if data['title'] != '':
            cur.execute("UPDATE tasks SET title='" + data['title'] + "' WHERE id='" + task_id + "'")

        if data['content'] != '':
            cur.execute("UPDATE tasks SET content='" + data['content'] + "' WHERE id='" + task_id + "'")
        
        if data['status'] != '':
            cur.execute("UPDATE tasks SET status='" + data['status'] + "' WHERE id='" + task_id + "'")

        if data['author'] != '':
            cur.execute("UPDATE tasks SET author='" + data['author'] + "' WHERE id='" + task_id + "'")

        if data['date'] != '':
            cur.execute("UPDATE tasks SET date='" + data['date'] + "' WHERE id='" + task_id + "'")

        mysql.connection.commit()  
        response_object['message'] = 'Task updated!'

    if request.method == 'DELETE':
        cur.execute("DELETE FROM tasks WHERE id='" + task_id + "'")
        mysql.connection.commit()
        response_object['message'] = 'Task removed!'

    return jsonify(response_object)

# USERS
@app.route('/API/users', methods=['GET', 'POST'])
def all_users():
    cur = mysql.connection.cursor()
    response_object = {'status': 'success'}

    cur.execute("SELECT * FROM users")
    query = cur.fetchall()
    response_object['users'] = query

    cur.close()

    return jsonify(response_object)

@app.route('/API/users/register', methods=['POST'])
def register():
    dt = datetime.datetime.now()
    created = dt.strftime("%Y-%m-%d %H:%M:%S")
    cur = mysql.connection.cursor()
    data = request.get_json()
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    cur.execute("INSERT INTO users (first_name, last_name, email, password, created) VALUES ('" + str(data['first_name']) + "', '" + str(data['last_name']) + "', '" + str(data['email']) + "', '" + str(password) + "', '" + str(created) + "')")
    mysql.connection.commit()

    result = {
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'password': password,
        'created': created
    }

    return jsonify(result)

@app.route('/API/users/login', methods=['POST'])
def login():
    cur = mysql.connection.cursor()
    data = request.get_json()
    result = ""  

    cur.execute("SELECT * FROM users where email = '" + str(data['email']) + "'")
    rv = cur.fetchone()

    if bcrypt.check_password_hash(rv['password'], data['password']):
        access_token = create_access_token(identity = {'first_name': rv['first_name'], 'last_name': rv['last_name'], 'email': rv['email']})
        result = access_token
    else:
        result = jsonify({'error': 'invalid username and password'})
    
    return result

if __name__ == '__main__':
    app.run()