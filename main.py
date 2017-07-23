from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashutils import make_pw_hash, check_pw_hash

# update database info (done!)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:letsblog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 'l337kGcys&zP3B'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(10000))
    #assign blogs to a user via relationship (done!)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


#add a user class with a column for foreign key user ID (done!)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    pw_hash = db.Column(db.String(120))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    blogs = db.relationship('Blog', backref='owner')

#add a constructor for the User class (done!)
    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.pw_hash = make_pw_hash(password)
        self.first_name = first_name
        self.last_name = last_name

#add a "before_request" app route that will check if a user is logged in before letting them access the add post page; add other pages to an allowed routes list
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/blog', methods=['GET'])
def blog():
    #if the request is just /blogs, then the length of request.args = 0, and it
    # means that there is no request for a specific post or a user's posts. If there
    #is an additional request, we need to test and see whether it's for a post id or user id
    if len(request.args) != 0:
        #find out if the request is for a post id or user id
        post_id = request.args.get('post_id')
        user_id = request.args.get('user_id')
        # if it's a post id, then redirect to the post.html template
        if post_id:
            posts = Blog.query.filter_by(id=[post_id]).all()
            return render_template("blog.html", posts=posts, page_title="Blogz")
        # if it's a user id, then redirect to the blogger.html template
        if user_id:
            posts = Blog.query.filter_by(owner_id = user_id).all()
            return render_template("blogger.html", posts=posts, page_title="Blogz")
    #if the len == 0, it means we just want the regular blogger page
    posts = Blog.query.all()    
    return render_template('blog.html', page_title="Blogz", posts=posts)

@app.route('/addpost', methods=['POST', 'GET'])
def add_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(email=session['email']).first()

        if title == "" or body == "":
            #rework error message as flash message (DONE!)
            flash('* All fields are required', 'error')
            return render_template('/addpost.html', title=title, page_title="Blogz- Add a new Post", body=body)
        else: 
            #the Blog class needs both body and title passed to it
            post = Blog(title, body, owner)
            #add the post to the database
            db.session.add(post)
            #commit it
            db.session.commit()
            #get the post id (as a string), so that we can use it to display the post
            post_id = str(post.id)
            #redirect using the post id # in address (GET)
            return redirect('/blog?post_id=' + post_id)
    return render_template('/addpost.html', page_title="Blogz- Add a new Post")

#add an app route + function for login.html

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #add validation for user login and create flash error messages
        user = User.query.filter_by(email=email).first()
        
        if user and check_pw_hash(password, user.pw_hash):
            session['email'] = email
            flash("You are currenly logged in", 'info')
            return redirect('/blog')

        if not user:
            email_error = "User account does not exhist"
            return render_template('login.html', email_error=email_error, page_title="Blogz- Log In")

        if not check_pw_hash(password, user.pw_hash):
            password_error = "Password is incorrect. Please try again"
            return render_template('login.html', password_error=password_error, page_title="Blogz- Log In")

    return render_template('login.html', page_title="Blogz- Log In")


#add an app route + function for index.html



#"remember" that the user is logged in until they click to logout or exit the browser

#add an app route + function for signup.html (DONE!)
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        input_email = request.form['email']
        input_password = request.form['password']
        password_hash = make_pw_hash(input_password)
        input_verify = request.form['verify']
        input_first_name = request.form['first_name']
        input_last_name = request.form['last_name']

        email_error = ''
        password_error = ''

        existing_user = User.query.filter_by(email=input_email).first()
        if existing_user:

            email_error = "User account already exhists. Please Log In"
            return redirect('/login')


        #EMAIL VALIDATION
        if contains_space(input_email):
            email_error = "Email must not contain spaces"
            input_email = ''
        if not is_correct_length(input_email):
            email_error = "Email must be between 3 and 40 characters"
            input_email = ''
        if not valid_email(input_email):
            email_error = "Email must contain these symbols: '@' and '.'"
            input_email = ''


        #PASSWORD VALIDATION
        if contains_space(input_password):
            password_error = "Email must contain these symbols: '@' and '.'"
            input_password = ''
        if not is_correct_length(input_password):
            password_error = "Email must be between 3 and 40 characters"
            input_password = ''
        if input_password != input_verify:
            password_error = "Passwords must match"
            input_password = ''
            verify_password = ''

        if password_error or email_error:
            return render_template('signup.html', password_error = password_error, email_error = email_error, email = input_email, first_name=input_first_name, last_name=input_last_name)   


        #IF NO ERRORS:
        if not password_error and not email_error:
            new_user = User(input_email, password_hash, input_first_name, input_last_name)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = input_email
            flash("You are currenly logged in")
            return redirect('/')

    return render_template('signup.html', page_title="Blogz- Sign Up")


#add a function for logout.html
@app.route('/logout')
def logout():
    del session['email']
    flash("You have been logged out")
    return redirect('/')

#redirect to homepage and add flask message "You have been logged out"


#FUNCTIONS FOR SIGNUP VALIDATION

    
def is_correct_length(input):
    if len(input) >= 3 and len(input) <= 40:
        return True
    
def contains_space(input):
    if " " in input:
        return True

def valid_email(input):
    at_count = 0
    for each_char in input:
        if each_char == '@':
            at_count = at_count + 1
    
    period_count = 0
    for each_char in input:
        if each_char == '.':
            period_count = period_count + 1

    if period_count >= 1 and at_count == 1:
        return True


@app.route('/')
def index():
    users = User.query.all() 
    return render_template('index.html', page_title="Blogz- Blogger Index", users=users)

if __name__ == '__main__':
    app.run()