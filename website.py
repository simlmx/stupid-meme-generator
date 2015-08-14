import os, json, sys
from flask import Flask, render_template, send_from_directory
import jinja2
from settings import config


app = Flask(__name__)

if 'extra_templates' in config:
    template_folders = [app.jinja_loader]
    for path in config['extra_templates']:
        template_folders.append(jinja2.FileSystemLoader(path))
    my_loader = jinja2.ChoiceLoader(template_folders)
    app.jinja_loader = my_loader


def get_image_dir(token):
    return config['installations'][token]['image_dir']


def get_preset(token, preset):
    return config['installations'][token]['presets'][preset]


@app.route('/')
def route_home():
    return '404 coco!'


@app.route('/<token>/')
def route_index(token):
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


@app.route('/<token>/<preset>/')
def route_maker(token, preset):
    preset = get_preset(token, preset)
    template = preset['template']
    return render_template(template)


if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        debug = True
    app.run(debug=debug)
