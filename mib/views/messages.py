import json
from typing import List
from flask import Blueprint, request, redirect, abort
import flask
from flask_login.utils import login_required
from dateutil import parser
from flask.templating import render_template
from flask_login import current_user
from mib.rao.user_manager import UserManager, User
from mib.rao.message_manager import MessageManager, MessagePost, Message
from mib.rao.draft_manager import DraftManager, DraftPost, Draft

messages = Blueprint('messages', __name__)


@ messages.route('/message/send', methods=['GET', 'POST'])
@login_required
def send_message():
    ''' GET: get the page for write and send a message to the chosen recipient/s
        POST: send the message to the recipient/s at the chosen date '''
    if request.method == 'POST':

        emails = request.form.get('receiver').split(',')
        recipient_list = []
        recipient_error_list = []
        message_ok = False

        for email in emails:
            email = email.strip(' ')
            user_list :List[User] = UserManager.get_user_by_email(email)
            # TODO: UserManager.get_user_by_email returns a List???
            #if db.session.query(User).filter(User.email == email,
            #                                 User.is_active.is_(True), User.email != current_user.email).first() is None:
            #    recipient_error_list.append(email)
            check = True
            for user in user_list:
                if user['is_active']:
                    recipient_list.append(user['id'])
                    check = False
            if check:
                recipient_error_list.append(email)

        new_message = MessagePost()
        new_message.id_sender = current_user.id
        new_message.recipients_list = recipient_list
        new_message.date_delivery = request.form.get('date')
        new_message.text = request.form.get('text')
        
        new_message = MessageManager.send_message(new_message)

        if new_message is not None:
            message_ok = True

        return render_template("send_message.html", form=dict(), message_ok=message_ok,
                               recipient_error_list=recipient_error_list)
    else:
        # landing from the recipients page, we want to populate the field with the chosen one
        recipient_message = request.args.items(multi=True)
        form = {'recipient': ''}
        for recipient in recipient_message:
            if recipient[1] != '':
                form['recipient'] += recipient[1] if form['recipient'] == '' else ', ' + recipient[1]

        return render_template("send_message.html", form=form)


@messages.route('/message/send/<id_message>', methods=['GET', 'POST'])
@login_required
def send_draft(id_message):
    ''' GET: get the message page filled with the draft message (<id_message>) info
        POST: send the draft message and delete it from drafts '''
    if request.method == 'POST':
        new_message :Message = DraftManager.send_draft(id_message)
        message_ok = False if new_message is None else True
        return render_template("send_message.html", form=dict(), message_ok=message_ok)
    else:
        draft :Draft = DraftManager.get_draft(id_message)
        if draft is None:
            abort(404)
        
        recipient_list = draft.recipients_list
        date = draft.date_delivery
        text = draft.text
        form = dict(recipient=recipient_list, text=text, date=date, message_id=draft.id_draft)
        return render_template("send_message.html", form=form)


@ messages.route('/draft', methods=['POST'])
@ login_required
def draft():
    ''' POST: save a message as a draft '''
    data = request.form
    draft_post :DraftPost = DraftPost()
    draft_post.id_sender = current_user.id
    draft_post.recipients_list = []
    emails = data['receiver'].strip('\', [, ]')
    for email in emails:
        draft_post.recipients_list.append(UserManager.get_user_by_email(email)['id'])
    draft_post.date_delivery = parser.parse(data['date'])
    draft_post.text = data['text']

    DraftManager.save_draft(draft_post)

    return redirect('/mailbox/draft')


@ messages.route('/message/forward/<id_message>', methods=['GET'])
@ login_required
def send_forward_msg(id_message):
    ''' GET: get the send message page filled with the text to forward '''
    recipient_message = request.args.items(multi=True)
    text = MessageManager.get_message(id_message).text
    form = dict(recipient="", text=text, message_id=id_message)
    for recipient in recipient_message:
        if recipient[1] != '':
            form['recipient'] += recipient[1] if form['recipient'] == '' else ', ' + recipient[1]
    return render_template("send_message.html", form=form, forward=True)


@ messages.route("/message/recipients", methods=["GET"])
@ login_required
def chooseRecipient():
    ''' GET: get the page for choosing the recipient/s for a new message '''
    raw_recipient_list :List[User]= UserManager.get_all_users()
    recipients = []
    for raw_recipient in raw_recipient_list:
        if raw_recipient['email'] != current_user.email and\
           raw_recipient['is_active']:
# TODO:           not raw_recipient.is_reported and\
#                 not raw_recipient['is_admin'] and\
           recipients.append(raw_recipient)
    
    form = dict(recipients=recipients)
    return render_template("recipients.html", form=form)


@ messages.route('/message/recipients/<id_message>', methods=['GET'])
@ login_required
def choose_recipient_msg(id_message):
    ''' GET: get the page for choosing the recipient/s for the chosen message'''
    raw_recipient_list :List[User]= UserManager.get_all_users()
    recipients = []
    for raw_recipient in raw_recipient_list:
        if raw_recipient['email'] != current_user.email and\
           raw_recipient['is_active']:
# TODO:           not raw_recipient.is_reported and\
#                 not raw_recipient['is_admin'] and\
           recipients.append(raw_recipient)
    
    form = dict(recipients=recipients, id_message=id_message)
    return render_template("recipients.html", form=form)


@ messages.route('/message/<message_id>', methods=["GET"])
@ login_required
def view_message(message_id):
    ''' GET: visualize the chosen message '''
    message :Message = MessageManager.get_message(message_id)

    if message is None:
        abort(404)
    else:
        recipient :User = UserManager.get_user_by_id(message.id_recipient)
        sender :User = UserManager.get_user_by_id(message.id_sender)
        return render_template("message.html",
                               sender=sender,
                               recipient=recipient,
                               message=message,
                               images=message.attachment_list)


@ messages.route("/message/withdraw/<id>", methods=['POST'])
@ login_required
def withdraw_message(id):
    ''' POST: withdraw a message not sent yet, paying points '''
    
    ret :int = MessageManager.withdraw_message(id)

    if ret==404:
        abort(404)
    elif ret==403:
        abort(403)
    else:
        return redirect('/mailbox/sent')


@ messages.route('/message/<message_id>/delete', methods=["POST"])
@login_required
def deleteMessage(message_id):
    ''' POST: delete the chosen message '''
    
    ret :int = MessageManager.delete_message(message_id)

    if ret==404:
        abort(404)
    elif ret==403:
        abort(403)
    else:
        return redirect('/mailbox/received')
