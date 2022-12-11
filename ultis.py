import json, os
from CNPM.models import ChuyenBay
from flask_login import current_user
from CNPM import db

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_cate():
    return read_json(os.path.join(app.root_path, 'data/categories.json'))


def load_product():
    return read_json(os.path.join(app.root_path, 'saleapp/data/product.json'))

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()