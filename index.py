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

    list_chuyen_bay= dao.tim_chuyen_bay(diem_di=diem_di, diem_den=diem_den)

    return render_template('index.html', list_san_bay=list_san_bay, list_chuyen_bay=list_chuyen_bay)


# @app.route('/search', methods=['get'])
# def searchChuyenBay():
#     return render_template('search.html')



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


@app.route('/datve/<int:chuyenBay_id>', methods=['post', 'get'])
def dat_ve(chuyenBay_id):
    cb = dao.get_chuyen_bay_id(chuyenBay_id)
    list_hang_ve = dao.load_hang_ve()
    if request.method.__eq__('POST'):
        name = request.form['name']
        last_name = request.form['lastname']
        cccd = request.form['cccd']
        hinh_cccd = request.files['hinh_cccd']
        sdt = request.form['sdt']
        chuyen_bay = request.form['chuyenbay']
        hang_ve = request.form['hangve']
        dao.dat_ve_online(name=name,lastname=last_name,cccd=cccd,hinh_cccd=hinh_cccd,sdt=sdt,chuyen_bay=chuyen_bay,hang_ve=hang_ve)

    return render_template('datve.html', cb=cb, list_hang_ve=list_hang_ve)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
