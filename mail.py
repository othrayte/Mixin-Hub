from flaskext.mail import Mail

from app import app

print(os.environ)
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']

mail = Mail(app)