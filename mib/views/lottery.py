from flask import Blueprint, redirect, render_template, request
from flask_login import (login_user, login_required, current_user)
from mib.rao.lottery_manager import LotteryManager

lottery = Blueprint('lottery', __name__)


@lottery.route('account/lottery', methods=['GET'])
@login_required
def account_lottery_get():
    """This method allows to retrieve the lottery page for the current user

     Args:
        None

    Returns: 
        Return the page of the lottery
    """
    lottery = LotteryManager.get_lottery_by_id_user(current_user.id)
    return render_template('lottery.html', points=lottery['points'], trials=lottery['trials'])


@lottery.route('account/lottery/spin', methods=['POST'])
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
        old_points = lottery['points']
        lottery = LotteryManager.update_lottery(
            current_user.id, lottery['points'], lottery['trials'])

    lottery = LotteryManager.get_lottery_by_id_user(current_user.id)
    points = lottery['points']
    prize = points - old_points

    return render_template('lottery.html', points=lottery['points'], trials=lottery['trials'], prize=prize)
