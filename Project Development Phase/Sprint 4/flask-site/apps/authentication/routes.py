# -*- encoding: utf-8 -*-
  

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass

from cloudant.client import Cloudant

ACCOUNT_NAME, API_KEY="bcd094f1-83ad-463f-9a94-cb77d637e4ff-bluemix","UujnPeap7D8PHMnJWtNeFDfd5tkooe8aqy2pE1hABW3y"
client = Cloudant.iam(ACCOUNT_NAME, API_KEY, connect=True)

my_db=client.create_database('my_db')

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']
        usertype = request.form['usertype']

        query = {'_id': {'$eq': username}}

        # Locate user
        res = my_db.get_query_result(query) 

        # Check the password
        if (username == res[0][0]['_id'] and password == res[0][0]['pass']):
            user = Users.query.filter_by(username=username).first()
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)

    #if usertype == "admin":
    #    return render_template('accounts/admin.html')

    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        usertype = request.form['usertype']

        data = {
            '_id': username,
            'email': email,
            'usertype': usertype,
            'pass': password
        }

        query = {'_id': {'$eq': data['_id']}}

        docs= my_db.get_query_result(query) 

        if len(docs.all()) != 0:
            return render_template('accounts/register.html',
                                   msg='User already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = my_db.create_document(data)
        
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()
        # Delete user from session
        logout_user()        

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
