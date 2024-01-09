import math

from flask import render_template, request, redirect, url_for, session, jsonify
from app import app, login, dao
from flask_login import login_user


@app.route('/home/', methods=['post', 'get'])
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


@app.route("/", methods=['post', 'get'])
def load_login():
    return render_template("login.html")


@app.route("/login", methods=['post', 'get'])
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username, password)

    if user:
        login_user(user=user)
        return redirect('/admin')
    else:
        return redirect(url_for("home"))

@app.route('/tracuuCB', methods=['get'])
def load_tracuu():
    return render_template('tracuu.html')

if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
