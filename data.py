import uuid
import sqlalchemy.dialects.postgresql

from app import db

class Channel(db.Model):
    """ A source connected through a volume slider. """
    uuid = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True)
    sourceUri = db.Column(db.String())
    volume = db.Column(db.Integer)

    def __init__(self, sourceUri, volume):
        self.uuid = uuid.uuid4()
        self.sourceUri = sourceUri
        self.volume = volume

    def __repr__(self):
        return '<Channel %s@%d as %s>' % (self.sourceUri, self.volume, self.uuid)

class Mix(db.Model):
    """ A configuration describing how to mix sources together. """
    uuid = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True)
    channels = db.relationship('Channel', backref='mix', lazy='dynamic')
    permissions = db.relationship('Permission', backref='mix', lazy='dynamic')
    keys = db.relationship('Key', backref='mix', lazy='dynamic')

    def __init__(self):
        self.uuid = uuid.uuid4()

    def __repr__(self):
        return '<Mix %s>' % (self.uuid,)

class Permission(db.Model):
    """ Who has what role. """

    def __init__(self, user, role, mix):
        self.user = user
        self.role = role
        self.mix = mix

    def __repr__(self):
        return '<Permission %s as %s for %s>' % (self.user, self.role, self.mix)

class User(db.Model):
    """ The unique combination of a user and a client, uniquely identified by anonid """
    email = db.Column(db.String(), primary_key=True)
    clients = db.relationship(Client, backref='user', lazy='dynamic')
    unverifiedActions = db.relationship('VerifyAction', backref='user', lazy='dynamic')
    permissions = db.relationship(Permission, backref='user', lazy='dynamic')
    keys = db.relationship('Key', backref='provider', lazy='dynamic')
    joined = db.Column(db.Date())

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<User %s>' % (self.email,)

    def hasRole(self, mix, codeName):
        query = Permission.query
        query = query.filter(Permission.user == self)
        query = query.filter(Permission.mix == mix)
        query = query.filter(Role.codeName == codeName)
        return query.count() > 0

class Client(db.Model):
    """ A spotify client, can be verified by email. """
    uuid = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True)
    name = db.Column(db.String())
    verified = db.Column(db.Boolean())
    unverifiedActions = db.relationship('VerifyAction', backref='client', lazy='dynamic')

    def __init__(self, name):
        self.uuid = uuid.uuid4()
        self.name = name
        self.verified = false

    def __repr__(self):
        return '<Client %s {%s}>' % (self.name, self.uuid)

class VerifyAction(db.Model):
    """ An action that reuires email verification. """
    uuid = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True)
    add = db.Column(db.Boolean())
    emailSent = db.Column(db.Date())

    def __init__(self, add, client, user):
        self.uuid = uuid.uuid4()
        self.add = add
        self.client = client
        self.user = user

    def __repr__(self):
        return '<VerifyAction %s client %s {%s}>' % (self.add, self.client, self.uuid)

class Role(db.Model):
    """ A named role that a User can get/have over a Mix. """
    codeName = db.Column(db.String(), primary_key=True)
    displayName = db.Column(db.String())
    permissions = db.relationship(Permission, backref='role', lazy='dynamic')
    keys = db.relationship('Key', backref='role', lazy='dynamic')

    def __init__(self, codeName, displayName):
        self.codeName = codeName
        self.displayName = displayName

    def __repr__(self):
        return '<Role %s: "%s">' % (self.codeName, self.displayName)

class Key(db.Model):
    """ A key that can be given to share a mix with specific role. """
    uuid = db.Column(sqlalchemy.dialects.postgresql.UUID(), primary_key=True)

    def __init__(self, role, mix):
        self.uuid = uuid.uuid4()
        self.role = role
        self.mix = mix

    def __repr__(self):
        return '<Key %s on %s {%s}>' % (self.role, self.mix, self.uuid)