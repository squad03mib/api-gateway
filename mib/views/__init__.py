from .auth import auth
from .home import home
from .users import users
from .lottery import lottery
from .messages import messages
from .mailbox import mailbox
from .content_filter import content_filter

"""List of the views to be visible through the project
"""
blueprints = [home, auth, users, lottery, messages, mailbox, content_filter]
