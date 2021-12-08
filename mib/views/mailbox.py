from typing import List
from flask import Blueprint
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required
from mib.rao.user_manager import UserManager, User
from mib.rao.message_manager import MessageManager, Message
from mib.rao.draft_manager import DraftManager, Draft

mailbox = Blueprint('mailbox', __name__)


@mailbox.route('/mailbox/sent', methods=['GET'])
@login_required
def see_sent_messages():
    ''' GET: get the inbox page '''
    msgs_sent :List[Message] = MessageManager.get_all_messages('sent')
    return render_template('msgs_sent.html', msgs_sent=msgs_sent)


@mailbox.route('/mailbox/received', methods=['GET'])
@login_required
def see_received_messages():
    ''' GET: get the outbox page'''
    msgs_rcv :List[Message] = MessageManager.get_all_messages('received')
    return render_template('msgs_rcv.html', msgs_rcv=msgs_rcv)


@mailbox.route('/mailbox/draft', methods=['GET'])
@login_required
def see_draft_messages():
    ''' GET: get the draft page'''
    draft_msgs :List[Draft] = DraftManager.get_all_drafts()
    return render_template('msgs_draft.html', draft_msgs=draft_msgs)
