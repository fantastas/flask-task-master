# virtualenv env
# source env/bin/activate
# pip3 install flask flask-sqlalchemy
# lsof -i tcp:5000

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.before_first_request
def create_tables():
    db.create_all()

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content= task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error adding the task"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        print(repr(tasks))

        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete_task(id):
    task = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an error deleting the task"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error updating the task"

    else:
        return render_template("update.html", task = task)


if(__name__ == "__main__"):
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    db.init_app(app)
