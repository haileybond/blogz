from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

# TODO - update database info (done!)
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:letsblog@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

# TODO - add a user class with a column for foreign key user ID (done!)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    blogs = db.relationship('Blog', backref='blogger')

# TODO - add a constructor for the User class (done!)
    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(10000))
    # TODO assign blogs to a user via relationship (done!)
    blogger_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, blogger):
        self.title = title
        self.body = body
        self.blogger = blogger


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
            # TODO - rework error message as flash message (DONE!)
            flash('* All fields are required', 'error')
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

#TODO - add a "before_request" app route that will check if a user is logged in before letting them access the add post page; add other pages to an allowed routes list

# TODO - add an app route + function for index.html

# TODO - add an app route + function for login.html
# TODO - add validation for user login and create flash error messages
# TODO - add flash message for logged in users - "You are currently loggin in"
# TODO - "remember" that the user is logged in until they click to logout or exit the browser

# TODO - add an app route + function for signup.html (DONE!)
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        verify = request.form['verify']



        # TODO - add validation and error messages for user signup (similar to "User Signup" assignment; use flash messages?)
    
        # TODO validate email (length, no spaces, contains @ and .) (DONE!)
        if is_empty(email):
            # TODO Add error message
            flash('* A valid email is required', 'error')
        else:
            if not is_correct_length(email):
                # TODO Add error message #email_error = "Email must be between 3 and 20 characters"
                flash('* Email must be between 3 and 20 characters', 'error')
                email= ''

        # TODO - Make sure the user doesn't already exhist
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('* User account already exhists. Please log in.', 'error')
            return redirect('/login')

        # TODO - Validate first and last name (must not be empty) (DONE!)
        if is_empty(first_name) or is_empty(last_name):
            flash('* Full name is required', 'error')
        
        #TODO - Validate the password and verify password (DONE!)
        if is_empty(password):
            flash('* Password is required.', 'error')
        elif contains_space(password):
            flash('* Password may not contain spaces', 'error')
        elif not is_correct_length(password):
            flash('* Password must be between 3 and 20 characters', 'error')
    
        #validate that password = password2 (must match password)
        if is_empty(verify):
            flash('* Password verification is required', 'error')
        elif password != verify:
            flash('* Passwords must match', 'error')

        if not is_empty(email) and is_correct_length(email) and not existing_user and not is_empty(first_name) and not is_empty(last_name) and not is_empty(password) and not contains_space(password) and is_correct_length(password) and password==verify:
            new_user = User(email, first_name, last_name, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            flash("You are currenly logged in")
            return redirect('/') 
    return render_template('signup.html')


# TODO - add a function for logout.html
# TODO - redirect to homepage and add flask message "You have been logged out"


#FUNCTIONS FOR SIGNUP VALIDATION
@app.route('/')
def index():
    return redirect('/blog')
    
def is_empty(input):
    if not input:
        return True

def is_correct_length(input):
    if len(input) >= 3 and len(input) <= 20:
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

    if period_count == 1 and at_count == 1:
        return True





if __name__ == '__main__':
    app.run()