import math

from flask import render_template, request, redirect, url_for, session, jsonify
import dao
from app import app, login
from flask_login import login_user, logout_user


@app.route('/')
def home():
    page = request.args.get('page')
    tuyen_bay = request.args.get('tuyen_bay')
    flights = dao.load_flights(tuyen_bay, page)
    routes = dao.load_routes()
    num = dao.count_flight()
    return render_template('index.html', flights=flights, routes=routes, pages=math.ceil(num/app.config['PAGE_SIZE']))




@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route("/login", methods=['post', 'get'])
def load_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)

        if user:
            login_user(user=user)
            return redirect('/')
    return render_template("login.html")


@app.route("/admin/login", methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)

    if user:
        login_user(user=user)
        return redirect('/admin')

@app.route('/logout')
def user_logout():
    logout_user()
    return redirect('/login')

@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(hoTen=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             CCCD=request.form.get('id'),
                             SDT=request.form.get('phone'),
                             email=request.form.get('mail'))
            except Exception as ex:
                print(str(ex))
                err_msg = "Hệ thống bị lỗi!"
            else:
                return redirect('/login')
        else:
            err_msg = 'Mậu khẩu không đúng'
    return render_template('/register.html', err_msg=err_msg)
@app.route('/tracuuCB', methods=['get'])
def load_tracuu():
    return render_template('tracuu.html')

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
