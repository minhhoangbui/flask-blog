import os
import secrets
from flask_mail import Message
from flask import url_for, current_app
from PIL import Image
from flaskblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,
                                'static/profile_pics', filename)
    image = Image.open(form_picture)
    image.thumbnail((125, 125))
    image.save(picture_path)
    return filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config.get('MAIL_USERNAME'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, then simply ignore this message and 
    no change will be applied to your account
    '''
    mail.send(msg)