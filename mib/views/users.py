
from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import (login_user, login_required, current_user)
import datetime
from mib.forms import UserForm
from mib.rao.user_manager import UserManager
from mib.auth.user import User

users = Blueprint('users', __name__)


@users.route('/create_user/', methods=['GET', 'POST'])
def create_user():
    """This method allows the creation of a new user into the database

    Returns:
        Redirects the user into his profile page, once he's logged in
    """
    form = UserForm()

    if form.is_submitted():
        email = form.data['email']
        password = form.data['password']
        firstname = form.data['firstname']
        lastname = form.data['lastname']
        birthdate = form.data['birthdate']
        date = birthdate.strftime('%Y-%m-%d')
        response = UserManager.create_user(
            email,
            password,
            firstname,
            lastname,
            date,
        )

        if response.status_code == 201:
            # in this case the request is ok!
            user = response.json()
            to_login = User.build_from_json(user)
            login_user(to_login)
            return redirect('/')
        elif response.status_code == 200:
            # user already exists
            flash('User already exists!')
            return render_template('create_user.html', form=form)
        else:
            flash('Unexpected response from users microservice!')
            return render_template('create_user.html', form=form)
    else:
        for fieldName, errorMessages in form.errors.items():
            for errorMessage in errorMessages:
                flash('The field %s is incorrect: %s' %
                      (fieldName, errorMessage))

    return render_template('create_user.html', form=form)


@users.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """Deletes the data of the user from the database.

    Args:
        id_ (int): takes the unique id as a parameter

    Returns:
        Redirects the view to the home page
    """

    response = UserManager.delete_user(id)
    if response.status_code != 202:
        flash("Error while deleting the user")
        return redirect(url_for('auth.profile', id=id))

    return redirect(url_for('home.index'))


@ users.route('/userinfo', methods=["GET", "POST"])
@ login_required
def get_user_info():
    ''' GET: get the profile info page
        POST: edit profile info'''
    if request.method == "GET":
        user = UserManager.get_user_by_id(current_user.id)
        return render_template('user_info.html', user=user)
    else:
        new_email = request.form["email"]
        new_firstname = request.form["first_name"]
        new_lastname = request.form["last_name"]
        new_date_of_birth = datetime.datetime.strptime(
            request.form["date_of_birth"], '%Y-%m-%d').date()
        new_password = request.form["password"]
        user_dict = dict(email=new_email, firstname=new_firstname, lastname=new_lastname,
                         date_of_birth=new_date_of_birth)

        checkEmail = UserManager.get_user_by_email(new_email)
        if checkEmail:
            return render_template('user_info.html', emailError=True, user=user_dict)

        UserManager.update_user(current_user.id, new_email, new_firstname,
                                new_lastname, new_password, new_date_of_birth)
        return render_template('user_info.html', user=user_dict)


@ users.route('/users', methods=["GET", "POST"])
@ login_required
def get_users():
    '''GET: get the list of users
       POST: create a user'''
    if request.method == 'GET':
        users = UserManager.get_all_users()

    return render_template('users.html', users=users)


@ users.route('/account/blacklist/add', methods=["GET", "POST"])
@ login_required
def add_user_to_blacklist():
    ''' GET: get the list of users that the user can add to the blacklist
        POST: add a user to the blacklist'''

    if request.method == 'POST':
        email = request.form.get('email')
        user_blacklisted = UserManager.get_user_by_email(email)
        id_blacklisted = user_blacklisted.id
        UserManager.add_user_to_blacklist(id_blacklisted)

        return redirect('/account/blacklist')

    else:
        blacklist = UserManager.get_blacklist(current_user.id)

        users = []

        if blacklist == []:
            user_list = UserManager.get_all_users()
            for item in user_list:
                if item['id'] != current_user.id:
                    users.append(item)
        else:
            for item in blacklist:
                user_blacklisted = UserManager.get_user_by_id(
                    item['id_blacklisted'])
                if user_blacklisted.email not in users:
                    users.append(user_blacklisted)

        return render_template('add_to_blacklist.html', users=users)


@ users.route('/account/blacklist', methods=["GET"])
@ login_required
def get_blacklist():
    '''GET: get the user blacklist'''
    blacklist = UserManager.get_blacklist(current_user.id)

    print(blacklist)

    users = []

    for item in blacklist:
        user_blacklisted = UserManager.get_user_by_id(
            item['id_blacklisted'])
        users.append({'email': user_blacklisted.email,
                     'firstname': user_blacklisted.first_name, 'lastname': user_blacklisted.last_name})

    print(users)

    return render_template('blacklist.html', blacklist=users)
