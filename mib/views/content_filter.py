from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required
from mib.rao.content_filter_manager import ContentFilterManager
from mib.models.content_filter import ContentFilter

content_filter = Blueprint('content_filter', __name__)


@content_filter.route('/userinfo/content_filter/<filter_id>', methods=['GET', 'PUT'])
@login_required
def user_content_filter(filter_id):
    if request.method == 'GET':
        result = ContentFilterManager.get_content_filter_info(filter_id)
    if request.method == 'PUT':
        active = request.form.get('active') == 'true'
        result = ContentFilterManager.set_content_filter(filter_id, active)

    return ContentFilter.from_dict(result.to_dict()).to_dict()
