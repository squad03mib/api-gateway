from .auth import auth
from .home import home
from .users import users
from .drafts import drafts
from .lottery import lottery
from .mailbox import mailbox
from .messages import messages
from .content_filter import content_filter

"""List of the views to be visible through the project
"""
blueprints = [home, auth, users, lottery, messages, mailbox, content_filter, drafts]
