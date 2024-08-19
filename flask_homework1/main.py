from flask import Flask

app = Flask(__name__)


@app.route('/')
def home_route():
    return 'Hello, Flask!'


@app.route('/name/<string:user_name>')
def hello(user_name):
    return f'Hello, your name is {user_name}'


if __name__ == '__main__':
    app.run(debug=True)
