import os
from flask import Flask, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

print(os.environ['DATABASE_URL'])

if not app.debug:
    import logging, sys
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)

db = SQLAlchemy(app)

import data

from flask import request
import json

@app.route('/')
def root():
    """ Redirect root requests to the project page on github. """
    return redirect("https://github.com/othrayte/Mixin-Hub", 301)

@app.route('/test')
def test():
    """ Prove that the server is alive. """
    return "Yes, I'm still alive"

@app.route('/user/register', methods=['POST'])
def registerUser():
    """ Regester an email address as a user.
    A verification email will be sent when a client is first added. """

    email = request.form['email']

    newUser = data.User(email)

    db.session.add(newUser)
    db.session.commit()
    
@app.route('/login')
def login():
    """ Start a secure session. """
    
    uuid = request.form['client']
    email = data.Client.query.get(uuid).user.email

    session['email'] = email
    
@app.route('/client/add')
def addClient():
    """ Add a client to the user, sends verification email. """

    email = request.form['name']
    user = data.User.query.get(session['email'])

    client = data.Client(name)
    db.session.add(client)

    action = data.VerifyAction(True, client, user)

    db.session.add(action)
    db.session.commit()

@app.route('/client/remove')
def removeClient():
    """ Removes a client from the user, sends verification email. """
    
    email = request.form['name']
    user = data.User.query.get(session['email'])

    client = data.Client(name)
    db.session.add(client)

    action = data.VerifyAction(False, client, user)

    db.session.add(action)
    db.session.commit()

@app.route('/mixes/create')
def createMix():
    """ Create a new mix. """
    email = request.form['name']
    user = data.User.query.get(session['email'])

    mix = data.Mix()
    db.session.add(mix)

    role = data.Role.get('owner')
    db.session.add(role)

    permission = data.Permission(user, role, mix)
    db.session.add(permission)

    mix.permissions.append(permission)

    db.session.commit()
    
@app.route('/mixes/list')
def listMixes():
    """ List all mixes for the logged in user. """
    email = request.form['name']
    user = data.User.query.get(session['email'])

    mixes = []
    mixPermissions = {}
    items = data.Mix.query.add_columns(Role.codeName, Role.displayName).filter(Permission.user == user).all()
    raise items
    


    return json.dumps()
    
@app.route('/clients/list')
def listClients():
    """ List all clients for the logged in user. """
    
@app.route('/key/use')
def useKey():
    """ Use a key with the logged in user. """
    
@app.route('/mix/channels/list')
def mixListChannels():
    """ List all channels in a mix.
    Requires sufficient permissions."""
    if not user.hasRole():
        pass
    
@app.route('/mix/channels/add')
def mixAddChannel():
    """ Add a new channel to a mix.
    Requires sufficient permissions."""
    
@app.route('/mix/permissions/list')
def mixListPermissions():
    """ List permissions on a mix allocated to users.
    Requires sufficient permissions."""

@app.route('/mix/permission/revoke')
def mixRevokePermission():
    """ Revoke a role from a mix.
    Requires sufficient permissions.""" 
    
@app.route('/mix/key/create')
def mixCreateKey():
    """ Create a shareable permission key for a mix.
    Requires sufficient permissions.""" 
    
@app.route('/channel/delete')
def channelDelete():
    """ Delete a channel, removes it from its mix.
    Requires sufficient permissions.""" 
    
@app.route('/channel/volume/update')
def channelUpdateVolume():
    """ Modify the volume of a channel.
    Requires sufficient permissions.""" 
    
@app.route('/action/verify')
def verifyAction():
    uuid = request.args.get('uuid')
    action = data.VerifyAction.query.get(uuid)
    if action.add:
        action.client.verified = True
    else:
        db.session.remove(action.client)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)