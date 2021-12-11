import pytz
import base64
from typing import List
from flask import Blueprint, request, redirect, abort
from flask_login.utils import login_required
from datetime import datetime, timedelta, timezone
from flask.templating import render_template
from flask_login import current_user
from mib.rao.user_manager import UserManager, User
from mib.rao.message_manager import MessageManager, MessagePost, Message
from mib.rao.draft_manager import DraftManager, DraftPost, Draft

messages = Blueprint('messages', __name__)


@ messages.route('/messages/send', methods=['GET', 'POST'])
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
            user = UserManager.get_user_by_email(email)
            check = True
            if  user is not None and user.is_active:
                    recipient_list.append(user.id)
                    check = False
            if check:
                recipient_error_list.append(email)

        new_message :MessagePost = MessagePost()
        new_message.attachment_list = []
        new_message.id_sender = current_user.id
        new_message.recipients_list = recipient_list

        message_date = request.form.get('date')
        tz=timezone(timedelta(hours=1))
        message_date = datetime.fromisoformat(message_date)
        message_date = message_date.replace(tzinfo=tz)
        message_date = message_date.astimezone(pytz.UTC)
        message_date = message_date.isoformat()

        new_message.date_delivery = message_date
        new_message.text = request.form.get('text')
        uploaded_files = request.files.getlist("files")

        if uploaded_files and any(f for f in uploaded_files):
            for file in uploaded_files:
                if file:
                    attachment = file.read()
                    new_message.attachment_list.append(base64.b64encode(attachment).decode('ascii'))
        
        new_message = MessageManager.send_message(new_message)

        if new_message is not None:
            message_ok = True
        else:
            for email in emails:
                recipient_error_list.append(email)

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


@messages.route('/messages/<message_id>', methods=["GET"])
@login_required
def view_message(message_id):
    ''' GET: visualize the chosen message '''
    message: Message = MessageManager.get_message(message_id)

    if message is None:
        abort(404)
    else:
        recipient: User = UserManager.get_user_by_id(message.id_recipient)
        sender: User = UserManager.get_user_by_id(message.id_sender)
        return render_template("message.html",
                               sender=sender,
                               recipient=recipient,
                               message=message,
                               images=message.attachment_list)


@messages.route('/messages/<message_id>/delete', methods=["POST"])
@login_required
def deleteMessage(message_id):
    ''' POST: delete the chosen message '''

    ret: int = MessageManager.delete_message(message_id)

    if ret == 404:
        abort(404)
    elif ret == 403:
        abort(403)
    else:
        return redirect('/inbox')


@messages.route("/messages/<id>/withdraw", methods=['POST'])
@login_required
def withdraw_message(id):
    ''' POST: withdraw a message not sent yet, paying points '''

    ret: int = MessageManager.withdraw_message(id)

    if ret == 404:
        abort(404)
    elif ret == 403:
        abort(403)
    else:
        return redirect('/outbox')

@messages.route('/messages/<id_message>/forward', methods=['GET'])
@login_required
def send_forward_msg(id_message):
    ''' GET: get the send message page filled with the text to forward '''
    recipient_message = request.args.items(multi=True)
    text = MessageManager.get_message(id_message).text
    form = dict(recipient="", text=text, message_id=id_message)
    for recipient in recipient_message:
        if recipient[1] != '':
            form['recipient'] += recipient[1] if form['recipient'] == '' else ', ' + recipient[1]
    return render_template("send_message.html", form=form, forward=True)