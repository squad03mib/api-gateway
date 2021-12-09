import pytz
import base64
from typing import List
from flask import Blueprint, request, redirect, abort
import flask
from flask_login.utils import login_required
from datetime import datetime, timedelta, timezone
from flask.templating import render_template
from flask_login import current_user
from mib.rao.user_manager import UserManager, User
from mib.rao.message_manager import MessageManager, MessagePost, Message
from mib.rao.draft_manager import DraftManager, DraftPost, Draft

drafts = Blueprint('drafts', __name__)



@drafts.route('/drafts', methods=['GET', 'POST'])
@login_required
def see_draft_messages():
    ''' GET: get the draft page'''
    ''' POST: save a message as a draft '''
    if request.method=='GET':
        draft_msgs = []
        draft_list :List[Draft] = DraftManager.get_all_drafts()
        for draft in draft_list:
            user :User = {}
            user['email'] = ''
            if draft.recipients_list is not None and len(draft.recipients_list) > 0:
                user = UserManager.get_user_by_id(draft.recipients_list[0])
            draft_msgs.append({'draft': draft, 'recipient': user})
        return render_template('msgs_draft.html', draft_msgs=draft_msgs)
    else:
        data = request.form
        draft_post: DraftPost = DraftPost()
        draft_post.id_sender = current_user.id
        draft_post.recipients_list = []
        emails = data['receiver'].split(',')

        for email in emails:
            email = email.strip(' ')
            user :User = UserManager.get_user_by_email(email)
            if user is not None:
                draft_post.recipients_list.append(user.id)
        draft_date = request.form.get('date')
        tz=timezone(timedelta(hours=1))
        draft_date = datetime.fromisoformat(draft_date)
        draft_date = draft_date.replace(tzinfo=tz)
        draft_date = draft_date.astimezone(pytz.UTC)
        draft_date = draft_date.isoformat()
        draft_post.date_delivery = draft_date
        draft_post.text = data['text']

        DraftManager.save_draft(draft_post)

        return redirect('/drafts')

@drafts.route('/drafts/<draft_id>', methods=["GET", "POST"])
@login_required
def view_draft(draft_id):
    ''' GET: visualize the chosen draft '''
    ''' POST: update the chosen draft '''
    draft: Draft = DraftManager.get_draft(draft_id)
    
    if draft is None:
        abort(404)
    if request.method == 'GET':
        recipients_email_list :str = ''
        emails = request.args.items(multi=True)
        
        for email in emails:
            if email[1] != '':
                recipients_email_list += email[1] if recipients_email_list == '' else ', ' + email[1]
            
        if recipients_email_list == '' and draft.recipients_list is not None and len(draft.recipients_list) > 0:
            recipient = UserManager.get_user_by_id(draft.recipients_list[0])
            recipients_email_list += recipient.email
            for i in range(1, len(draft.recipients_list)):
                recipient = UserManager.get_user_by_id(draft.recipients_list[i])
                recipients_email_list += ', ' + recipient.email
        
        sender: User = UserManager.get_user_by_id(draft.id_sender)
        
        draft.date_delivery = datetime.fromisoformat(draft.date_delivery).strftime('%Y-%m-%d %H:%M')

        form = dict(recipients_email_list = recipients_email_list, sender = sender, draft=draft)

        return render_template("edit_draft.html", form=form)
    else:
        DraftManager.delete_draft(draft_id)

        data = request.form
        draft_post: DraftPost = DraftPost()
        draft_post.id_sender = current_user.id
        draft_post.recipients_list = []
        emails = data['receiver'].split(',')

        for email in emails:
            email = email.strip(' ')
            user :User = UserManager.get_user_by_email(email)
            if user is not None:
                draft_post.recipients_list.append(user.id)
        draft_date = request.form.get('date')
        tz=timezone(timedelta(hours=1))
        draft_date = datetime.fromisoformat(draft_date)
        draft_date = draft_date.replace(tzinfo=tz)
        draft_date = draft_date.astimezone(pytz.UTC)
        draft_date = draft_date.isoformat()
        draft_post.date_delivery = draft_date
        draft_post.text = data['text']

        DraftManager.save_draft(draft_post)

        return redirect('/drafts')


@drafts.route('/drafts/<id_draft>/send', methods=['POST'])
@login_required
def send_draft(id_draft):
    ''' POST: send the draft message and delete it from drafts '''
    DraftManager.delete_draft(id_draft)

    data = request.form
    draft_post: DraftPost = DraftPost()
    draft_post.id_sender = current_user.id
    draft_post.recipients_list = []
    emails = data['receiver'].split(',')

    for email in emails:
        email = email.strip(' ')
        user :User = UserManager.get_user_by_email(email)
        if user is not None:
            draft_post.recipients_list.append(user.id)
    draft_date = request.form.get('date')
    tz=timezone(timedelta(hours=1))
    draft_date = datetime.fromisoformat(draft_date)
    draft_date = draft_date.replace(tzinfo=tz)
    draft_date = draft_date.astimezone(pytz.UTC)
    draft_date = draft_date.isoformat()
    draft_post.date_delivery = draft_date
    draft_post.text = data['text']

    for file in request.files:
        attachment = request.files[file].read()
        draft_post.attachment_list.append(base64.b64encode(attachment).decode('ascii'))

    draft = DraftManager.save_draft(draft_post)
    DraftManager.send_draft(draft.id_draft)
    return redirect('/outbox')