from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:    
        return f"{self.sno} - {self.title}"

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    return f"Username: {username}, your Password is: {password}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # created the database 
        app.run(debug=True, port=8000)
