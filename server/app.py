import uuid
import os
import datetime

from flask import Flask, jsonify, request, json, render_template
from flask_cors import CORS

from flask_mysqldb import MySQL


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_api2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# POSTS
@app.route('/API/posts', methods=['GET', 'POST'])
def all_posts():
    cur = mysql.connection.cursor()
    response_object = {'status': 'success'}

    #date
    dt = datetime.datetime.now()
    today = dt.strftime("%Y-%m-%d %H:%M:%S")

    #upload path
    target = os.path.join(APP_ROOT, 'images/')
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


if __name__ == '__main__':
    app.run()