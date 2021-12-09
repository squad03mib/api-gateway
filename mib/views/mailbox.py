from typing import List
from flask import Blueprint
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required
from mib.rao.user_manager import UserManager, User
from mib.rao.message_manager import MessageManager, Message
from mib.rao.draft_manager import DraftManager, Draft
from mib.rao.lottery_manager import LotteryManager

mailbox = Blueprint('mailbox', __name__)


@mailbox.route('/mailbox/sent', methods=['GET'])
@login_required
def see_sent_messages():
    ''' GET: get the inbox page '''
    msgs_sent = []
    msg_list :List[Message] = MessageManager.get_all_messages('sent')
    lottery = {}
    lottery['points'] = 0
    for msg in msg_list:
        user :User = UserManager.get_user_by_id(msg.id_recipient)
        lottery = LotteryManager.get_lottery_by_id_user(current_user.id)
        msgs_sent.append({'msg': msg, 'recipient': user})
    return render_template('msgs_sent.html', msgs_sent=msgs_sent, points=lottery['points'])


@mailbox.route('/mailbox/received', methods=['GET'])
@login_required
def see_received_messages():
    ''' GET: get the outbox page'''
    msgs_rcv = []
    msg_list :List[Message] = MessageManager.get_all_messages('received')
    for msg in msg_list:
        user :User = UserManager.get_user_by_id(msg.id_sender)
        msgs_rcv.append({'msg': msg, 'sender': user})
        
    return render_template('msgs_rcv.html', msgs_rcv=msgs_rcv)


@mailbox.route('/mailbox/draft', methods=['GET'])
@login_required
def see_draft_messages():
    ''' GET: get the draft page'''
    draft_msgs = []
    draft_list :List[Draft] = DraftManager.get_all_drafts()
    for draft in draft_list:
        user :User = {}
        user['email'] = ''
        if draft.recipients_list is not None and len(draft.recipients_list) > 0:
            user = UserManager.get_user_by_id(draft.recipients_list[0])
        draft_msgs.append({'draft': draft, 'recipient': user})
    return render_template('msgs_draft.html', draft_msgs=draft_msgs)
