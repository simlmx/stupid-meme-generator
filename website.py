import os, json, sys
from flask import Flask, render_template, send_from_directory
import jinja2

app = Flask(__name__)


def get_image_dir(token):
    return os.path.join('installations', token)


def is_token_valid(token):
    return token in os.listdir('installations')


@app.route('/')
def route_home():
    return 'You need to know the right url!'


@app.route('/<token>/')
def route_index(token):
    if not is_token_valid(token):
        return 'Wrong url.'
    image_dir = get_image_dir(token)
    return render_template('index.html', image_dir=image_dir)


@app.route('/<token>/images/<filename>')
def route_image(token, filename):
    image_dir = get_image_dir(token)
    return send_from_directory(image_dir, filename)


@app.route('/<token>/image_list/')
def route_image_list(token):
    """ returns the list of image names """
    image_dir = get_image_dir(token)
    files = [os.path.splitext(f)[0] for f in os.listdir(image_dir)
             if f.endswith('.jpg') and not f.endswith('_t.jpg')]
    return json.dumps(files)


if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True
    app.run(debug=debug)
