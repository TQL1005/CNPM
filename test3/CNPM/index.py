from flask import render_template, Flask, request, redirect, session, jsonify
from CNPM import dao, app, login, admin, ultis
from flask_login import login_user, logout_user, current_user, login_required
from CNPM.decorators import annonymous_user
from CNPM.admin import *


@app.route("/")
def home():
    list_san_bay = dao.load_san_bay()
    diem_di = request.args.get('di')
    diem_den = request.args.get('den')

    return render_template('index.html', list_san_bay=list_san_bay)


# @app.route('/search', methods=['get'])
# def searchChuyenBay():
#     return render_template('search.html')


@app.route('/banve')
def ban_ve():
    return render_template('banve.html')


@app.route('/tuyenbay')
def tuyen_bay():
    producs = ultis.load_product()
    return render_template('tuyenbay.html', products=producs)


@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')


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


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/api/tuyen-bay', methods=['post'])
def add():
    data = request.json
    id = str(data.get('id'))
    di = data.get('di')
    den = data.get('den')

    import pdb
    pdb.set_trace()

    tuyen = session.get('tuyen')
    tuyen[id] = {
        'id': id,
        'di': di,
        'den': den
    }
    session['tuyen'] = tuyen

    return jsonify(ultis.chuyentuyenve(tuyen))


if __name__ == '__main__':
    app.run(debug=True)
