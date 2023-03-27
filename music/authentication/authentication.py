from flask import Flask, render_template, redirect, url_for, session, request, Blueprint, abort
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from music.domainmodel.user import User
from music.authentication import services

authentication_blueprint = Blueprint('authentication_bp', __name__, url_prefix="/authentication")

@authentication_blueprint.route('/register', methods=['GET', 'POST']) #TODO: IMPLEMENT PASSWORD HASHING
def register():
    form = RegisterForm()
    invalid_username = None

    if form.validate_on_submit():
        try:
            services.create_and_add_user(form.username.data, form.password.data, app.repo)

            return redirect(url_for('authentication_bp.login'))
            
        except services.UsernameInUse:
            invalid_username = 'That username is already taken!'
    
    return render_template(
        'authentication/credentials.html',
        title='Register',
        form=form,
        user_name_error_message=invalid_username,
        password_error_message=None,
        handler_url=url_for('authentication_bp.register'),
    )

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    invalid_username = None
    invalid_password = None

    if form.validate_on_submit():
        try:
            services.sign_in(session, form.username.data, form.password.data, app.repo)

            return redirect(url_for('home'))

        except services.UnknownUserException:
            invalid_username = 'No known user with that Username'

        except services.AuthenticationException:
            invalid_password = 'Your password is incorrect'

    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=invalid_username,
        password_error_message=invalid_password,
        form=form,
    )

@authentication_blueprint.route('/logout')
def logout():
    services.sign_out(session)
    return redirect(url_for('home'))



class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = 'Your password must be at least 8 characters long, contain an upper case letter, a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(message="Your username is required"), Length(min=4, max=16, message="Your username is too short")])
    password = PasswordField('Password', [DataRequired(message="Your password is required"), PasswordValid()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired(), PasswordValid("Your password is incorrect")])
    submit = SubmitField('Login')