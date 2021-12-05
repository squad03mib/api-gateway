from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_user, login_required, current_user
from mib.forms import UserForm
from mib.rao.user_manager import UserManager
from mib.rao.lottery_manager import LotteryManager
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


@users.route('account/lottery', methods=['GET'])
@login_required
def account_lottery_get():
    """This method allows to retrieve the lottery page for the current user

     Args:
        None

    Returns: 
        Return the page of the lottery
    """
    lottery = LotteryManager.get_lottery_by_id_user(current_user.id)
    print(lottery)

    return render_template('lottery.html', points=lottery.points, trials=lottery.trials)


@users.route('account/lottery/spin', methods=['POST'])
@login_required
def account_lottery_spin_post():  # noqa: E501
    """This method allows to spin the lottery

     # noqa: E501


    :rtype: None
    """
    lottery = LotteryManager.get_lottery_by_id_user(current_user.id)
    if lottery is None:
        old_points = 0
        lottery = LotteryManager.create_lottery(current_user.id, 0, 1)
    else:
        old_points = lottery.trials
        lottery = LotteryManager.update_lottery(
            current_user.id, lottery.points, lottery.trials)

    prize = lottery.points - old_points

    return render_template('lottery.html', points=lottery.points, trials=lottery.trials, prize=prize)
