import os, json
from flask import Flask, render_template, send_from_directory
from settings import config


app = Flask(__name__)


def parse_token(token):
    for inst in config['installations']:
        if inst['token'] == token:
            image_dir = inst['image_dir']
            return image_dir
    raise ValueError('invalid url')


@app.route('/')
def route_home():
    return '404 coco!'


@app.route('/<token>/')
def route_index(token):
    image_dir = parse_token(token)
    return render_template('index.html', image_dir=image_dir)


@app.route('/<token>/images/<filename>')
def route_image(token, filename):
    image_dir = parse_token(token)
    return send_from_directory(image_dir, filename)


@app.route('/<token>/image_list/')
def route_image_list(token):
    """ returns the list of image names """
    image_dir = parse_token(token)
    files = [os.path.splitext(f)[0] for f in os.listdir(image_dir)
             if f.endswith('.jpg') and not f.endswith('_t.jpg')]
    return json.dumps(files)


if __name__ == '__main__':
    app.run()
