from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/user/<string:username>')
def get_user(username: str) -> str:
    return f'Hello, {username}!'

if __name__ == "__main__":
    app.run(debug=True)



