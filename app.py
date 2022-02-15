from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html', data=items)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')


@app.route('/post')
def post():
    return render_template('post.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        item = Item(title=title, body=body)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Error("

    else:
        return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
