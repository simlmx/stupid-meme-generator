import os, json

# read some infos for our config
data_dir = os.environ.get('OPENSHIFT_DATA_DIR', '.')
config = json.load(open(os.path.join(data_dir, 'config.json')))

# and a bit of a hack to add the data_dir to the image_dir folders
for blob in config['installations']:
    blob['image_dir'] = os.path.join(data_dir, blob['image_dir'])
