import json, os
from saleapp import app


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_cate():
    return read_json(os.path.join(app.root_path, 'data/categories.json'))


def load_product():
    return read_json(os.path.join(app.root_path, 'saleapp/data/product.json'))
