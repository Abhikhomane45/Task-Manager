from flask import Flask,render_template,request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    return f"Username: {username},your Password is : {password}"

if __name__=="__main__":
    app.run(debug=True, port=8000)
    



