from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(10000))

    def __init__(self, name):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def index():
    posts = Blog.query.all()    
    return render_template('homepage.html', title="Blog", posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    
    return render_template('newpost.html', title="Add a New Post")  

@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        post_title = request.form['title']
        new_title = Blog(post_title)
        db.session.add(new_title)
        db.session.commit()
       
        post_body = request.form['body']
        new_body = Blog(post_body)
        db.session.add(new_body)
        db.session.commit()

    return redirect('/blog')
    
if __name__ == '__main__':
    app.run()