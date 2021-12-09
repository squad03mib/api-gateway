
from typing import List
from flask import Blueprint
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required
from mib.rao.user_manager import UserManager, User
from mib.rao.message_manager import MessageManager, Message
from mib.rao.lottery_manager import LotteryManager

calendar = Blueprint('calendar', __name__)


@calendar.route('/calendar/sent', methods=['GET'])
@login_required
def calendar_sent():
    ''' GET: get the inbox page '''
    msgs_sent = []
    msg_list: List[Message] = MessageManager.get_all_messages('sent')
    lottery = {}
    lottery['points'] = 0
    for msg in msg_list:
        user: User = UserManager.get_user_by_id(msg.id_recipient)
        lottery = LotteryManager.get_lottery_by_id_user(current_user.id)
        msgs_sent.append({'msg': msg, 'recipient': user})
    return render_template('calendar.html', msgs_sent=msgs_sent)


@calendar.route('/calendar/received', methods=['GET'])
@login_required
def calendar_received():
    ''' GET: get the outbox page'''
    msgs_rcv = []
    msg_list: List[Message] = MessageManager.get_all_messages('received')
    for msg in msg_list:
        user: User = UserManager.get_user_by_id(msg.id_sender)
        msgs_rcv.append({'msg': msg, 'sender': user})

    return render_template('calendar.html', msgs_rcv=msgs_rcv)
