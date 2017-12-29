from flask import (Flask, render_template, redirect, url_for,
                   request, make_response, flash)

app = Flask(__name__)
app.secret_key = '1u40rnegisrgnafewar'
HOST = '0.0.0.0'
PORT = 8000


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/maps/<filename>')
def show_map(filename='map.html'):
    return render_template('/maps/{}'.format(filename))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
