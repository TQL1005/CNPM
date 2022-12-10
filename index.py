from flask import render_template, Flask, request, redirect
from CNPM import dao, app, login, admin #, utils
from flask_login import login_user, logout_user, current_user, login_required
from CNPM.decorators import annonymous_user


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/chuyenbay')
def searchChuyenBay():
    return render_template('search.html')

'''
@app.route('/login', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return render_template('login.html')
'''


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


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
