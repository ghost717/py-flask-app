from flask import Flask, jsonify, request, json, render_template
from flask_cors import CORS

from flask_mysqldb import MySQL


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

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
    target = os.path.join(APP_ROOT, 'images/upload/')
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("couldn't create upload dir: {}".format(target) )
    
    if request.method == 'POST':
        target = os.path.join(APP_ROOT, 'images/upload/')
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


if __name__ == '__main__':
    app.run()