from flask import Flask, render_template, redirect, url_for

# from . import routes

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():  # put application's code here
    # return 'Hello World!'
    return render_template('index.html')


@app.route('/info/', methods=['GET'])
def info():
    return redirect(url_for('index'))


@app.route('/contacts/', methods=['GET'])
def contacts():
    return redirect(url_for('index'))


@app.route('/todo/', methods=['GET'])
def todo():
    return render_template('todo_dashboard.html')


if __name__ == '__main__':
    app.run()
