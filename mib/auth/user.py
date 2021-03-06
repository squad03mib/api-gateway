from flask_login import UserMixin


class User(UserMixin):
    """
    This class represents an authenticated user.
    It is not a model, it is only a lightweight class used
    to represents an authenticated user.
    """
    id = None
    email = None
    firstname = None
    lastname = None
    date_of_birth = None
    is_active = None
    is_admin = None
    authenticated = None
    is_anonymous = False
    extra_data = None

    @staticmethod
    def build_from_json(json: dict):
        kw = {key: json[key] for key in json}
        extra = json.copy()
        all(map(extra.pop, kw))
        kw['extra'] = extra

        return User(**kw)

    def __init__(self, **kw):
        if kw is None:
            raise RuntimeError('You can\'t build the user with none dict')
        self.id = kw["id"]
        self.email = kw["email"]
        self.is_active = kw["is_active"]
        self.authenticated = kw["authenticated"]
        self.is_anonymous = kw["is_anonymous"]
        self.firstname = kw["firstname"]
        self.lastname = kw["lastname"]
        self.date_of_birth = kw["date_of_birth"]
        self.extra_data = kw['extra']

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]
        elif item in self.extra_data:
            return self.extra_data[item]
        else:
            raise AttributeError('Attribute %s does not exist' % item)

    def __str__(self):
        s = 'User Object\n'
        for (key, value) in self.__dict__.items():
            s += "%s=%s\n" % (key, value)
        return s
