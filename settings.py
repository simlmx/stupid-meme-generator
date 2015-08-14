import os, json

# read some infos for our config
data_dir = os.environ.get('OPENSHIFT_DATA_DIR', '.')
config = json.load(open(os.path.join(data_dir, 'config.json')))

# and a bit of a hack to add the data_dir to the image_dir folders
for blob in config['installations']:
    blob['image_dir'] = os.path.join(data_dir, blob['image_dir'])

# same for extra templates
if 'extra_templates' in config:
    config['extra_templates'] = [os.path.join(data_dir, 'extra_templates', x)
                                 for x in config['extra_templates']]
