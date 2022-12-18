from flask import render_template, Flask, request, redirect, session, jsonify
from CNPM import dao, app, login, admin #, utils
from flask_login import login_user, logout_user, current_user, login_required
from CNPM.decorators import annonymous_user
from CNPM.admin import *
import json


@app.route("/")
def home():
    list_san_bay = dao.load_san_bay()
    diem_di= request.args.get('di')
    diem_den= request.args.get('den')

    return render_template('index.html', list_san_bay=list_san_bay)


# @app.route('/search', methods=['get'])
# def searchChuyenBay():
#     return render_template('search.html')


@app.route('/banve')
def ban_ve():
    return render_template('banve.html')



@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')


@app.route('/api/data/phieuthongke', methods=['get'])
def phieu_thong_ke():
    json_object = []
    with open('data/sample.json', 'r', encoding='utf-8') as openfile:
        json_object = json.loads(openfile.read())
    # import pdb;
    # pdb.set_trace()
    tong_doanh_thu = 0.0

    return render_template('/admin/phieuthongke.html', json_object=json_object)


@app.route("/login", methods=['get', 'post'])
@annonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']
        user = dao.auth_user(username, password)
        if user:
            login_user(user=user)
            return redirect('/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/api/data', methods=['post'])
def add_data():
    data = request.json
    id = str(data['id'])
    data1 = session['data1'] if 'data1' in session else {}
    if id in data1:
        pass
    else:
        name = data['name']
        price = data['price']
        so_luot_bay = data['so_luot_bay']
        ty_le = data['ty_le']
        tong_doanh_thu = data['tong_doanh_thu']

        data1[id] = {
            "id": id,
            "name": name,
            "price": price,
            "so_luot_bay": so_luot_bay,
            "ty_le": ty_le,
            "tong_doanh_thu": tong_doanh_thu,
        }

    session['data1'] = data1
    json_object = json.dumps([session.get('data1')])
    with open("data/sample.json", "w", encoding='utf-8') as outfile:
        outfile.write(json_object)
    # import pdb;
    # pdb.set_trace()
    return jsonify(session.get('data1'))


@app.route('/api/data', methods=['delete'])
def delete_data():
    session.pop('data1', None)
    # import pdb;
    # pdb.set_trace()
    return jsonify("test")


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
