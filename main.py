from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

# TODO - update database info (check)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:letsblog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# TODO - add a user class with a column for foreign key user ID
class User(db.Model):

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(10000))
    # TODO assign blogs to a user via relationship

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['GET'])
def homepage():
    if len(request.args) != 0:
        post_id = request.args.get("id")
        post = Blog.query.get(post_id)
        return render_template('post.html', post=post)
    posts = Blog.query.all()    
    return render_template('homepage.html', title="Blog", posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    return render_template('addpost.html', title="Add a New Post")  

@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == "" or body == "":
            error = "* All fields are required"
            return render_template('/addpost.html', title=title, body=body, error=error)
        else: 
            #the Blog class needs both body and title passed to it
            post = Blog(title, body)
            #add the post to the database
            db.session.add(post)
            #commit it
            db.session.commit()
            #get the post id (as a string), so that we can use it to display the post
            post_id = str(post.id)
            #redirect using the post id # in address (GET)
            return redirect('/blog?id=' + post_id)
    return render_template('/addpost.html')

# TODO - add an app route + function for index.html

# TODO - add an app route + function for login.html
# TODO - add validation for user login and create flash error messages
# TODO - add flash message for logged in users - "You are currently loggin in"
# TODO - "remember" that the user is logged in until they click to logout or exit the browser

# TODO - add an app route + function for signup.html
# TODO - add validation and error messages for user signup (similar to "User Signup" assignment; use flash messages?)

# TODO - add a function for logout.html
# TODO - redirect to homepage and add flask message "You have been logged out"

@app.route('/')
def index():
    return redirect('/blog')
    
if __name__ == '__main__':
    app.run()