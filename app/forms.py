from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.models import User, Spell, TimeLog

class LoginForm(FlaskForm):
    uname = StringField('Username', id='uname', validators=[DataRequired()])
    pword = PasswordField('Password', id='pword', validators=[DataRequired()])
    twoFA = StringField('TwoFactor', id='2fa')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    uname = StringField('Username', id='uname', validators=[DataRequired()])
    pword = PasswordField('Password', id='pword', validators=[DataRequired()])
    twoFA = StringField('TwoFactor', id='2fa')
    submit = SubmitField('Register')

    def validate_uname(self, uname):
        user = User.query.filter_by(uname=uname.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class SpellForm(FlaskForm):
    inputtext = TextAreaField('Enter text below', id='inputtext', validators=[DataRequired()])
    submit = SubmitField('Submit')

class logHistoryForm(FlaskForm):
    userid = StringField('Username', id='userid', validators=[DataRequired()])
    submit = SubmitField('Submit')

class queryHistoryForm(FlaskForm):
    userquery = StringField('Username', id='userquery', validators=[DataRequired()])
    history = TextAreaField('History')
    submit = SubmitField('Submit')
