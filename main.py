from flask import Flask, render_template
from data import db_session

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('main_page.html')


@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=8080, host='127.0.0.1')
