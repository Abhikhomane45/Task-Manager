from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DB Model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route('/')
def index():
    all_todos = Todo.query.all()
    return render_template('index.html', allTodo=all_todos)

@app.route('/', methods=['POST'])
def add_task():
    title = request.form['title']
    desc = request.form['desc']
    if title and desc:
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        flash("Task added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form['email']
    password = request.form['password']
    if email == "admin@example.com" and password == "admin123":
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials", "danger")
        return redirect(url_for('login'))

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = db.session.get(Todo, sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = db.session.get(Todo, sno)
    db.session.delete(todo)
    db.session.commit()
    flash("Task deleted!", "warning")
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
