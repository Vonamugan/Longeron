from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String)
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    body = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.date_posted.desc()).all()
    return render_template('index.html', posts=items)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Item.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        subtitle = request.form['subtitle']
        author = request.form['author']

        post = Item(title=title, body=body, subtitle=subtitle, author=author, date_posted=datetime.now())

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except:
            return "Error("

    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
