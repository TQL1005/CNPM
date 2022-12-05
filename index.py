from flask import render_template, Flask
#from CNPM import dao, app, login, admin, utils
from flask_login import login_user, logout_user, current_user, login_required
#from CNPM.decorators import annonymous_user

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route('/chuyenbay')
def searchChuyenBay():
    return render_template('search.html')

"""
@app.route('/login', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return render_template('login.html')
"""

if __name__ == '__main__':
    app.run(debug=True)
