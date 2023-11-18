from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exists_email
    

class LoginForm(FlaskForm):
    username            = StringField("username", validators=[DataRequired()])
    password            = PasswordField("password", validators=[DataRequired()])
    submit              = SubmitField("Login")

class SignUpForm(FlaskForm):
    username            = StringField("username", validators=[DataRequired(), Length(min=4, max=12)])
    fullname            = StringField("full name", validators=[DataRequired(), Length(min=4, max=16)])
    email               = EmailField("email", validators=[DataRequired(), Email(), exists_email])
    password            = PasswordField("password", validators=[DataRequired(), Length(min=8)])
    confirm_password    = PasswordField("confirm password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
    submit              = SubmitField("Sign Up")

class EditProfileForm(SignUpForm):
    username            = StringField("username", validators=[DataRequired(), Length(min=4, max=12)])
    password            = None
    confirm_password    = None
    email               = None
    bio                 = StringField("bio", )
    profile_pic         = FileField("picture", validators= [FileAllowed(["jpg", "png", "jpeg", "webp"])])
    submit              = SubmitField("Erledigt")

class ResetPasswordForm(FlaskForm):
    old_password        = PasswordField("old password", validators=[DataRequired(), Length(min=8)])
    new_password        = PasswordField("new password", validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField("confirm new password", validators=[DataRequired(), Length(min=8), EqualTo("new_password")])
    submit              = SubmitField("reset password")

class ForgotPasswordForm(FlaskForm):
    email               = EmailField("email", validators=[DataRequired(), not_exists_email])
    recaptcha           = RecaptchaField()
    submit              = SubmitField("send link verification to email")

class VerificationResetPasswordForm(FlaskForm):
    password            = PasswordField("new password", validators=[DataRequired(), Length(min=8)])
    confirm_password    = PasswordField("confirm new password", validators=[DataRequired(), Length(min=8), EqualTo("password")])
    submit              = SubmitField("reset password")

    

class CreatePostForm(FlaskForm):
    post_pic            = FileField("picture", validators=[DataRequired(), FileAllowed(["jpg", "png", "jpeg", "webp"])])
    caption             = TextAreaField("caption")
    submit              = SubmitField("Post")

class EditPostForm(FlaskForm):
    caption             = StringField("caption")
    photo               = FileField("Photo")
    submit              = SubmitField("update post")