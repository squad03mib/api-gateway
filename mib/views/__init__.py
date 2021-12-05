from .auth import auth
from .home import home
from .users import users
from .lottery import lottery

"""List of the views to be visible through the project
"""
blueprints = [home, auth, users, lottery]
