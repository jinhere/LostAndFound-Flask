
from cgi import FieldStorage
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me') # remeber me: accidently closed the browser, if u reopen it, u r still logged in
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    password2=PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Register')
    
    def validate_username(self,username): # 위의 validators이외에 wtf는 이런 custom validators도 수행해준다
        user=User.query.filter_by(username=username.data).first()
        if user is not None: # 입력된 username이 이미 존재한다면
            raise ValidationError('Please use a different username.') # 이 validator에서 error가 발생하면 error가 빨간 글씨로 나올것이다.
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me=TextAreaField('About me',validators=[Length(min=0,max=140)])
    submit=SubmitField('Submit')
    def __init__(self,original_username,*args,**kwargs):
        super(EditProfileForm,self).__init__(*args,**kwargs)
        self.original_username=original_username
        
    def validate_username(self,username): #username duplicate error fixed
        if username.data!=self.original_username:
            user=User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
    
class EmptyForm(FlaskForm): # follow 기능에 필요함
    submit=SubmitField('Submit')
    
class PostForm(FlaskForm):
    post=TextAreaField('Say something',validators=[DataRequired(),Length(min=1,max=140)])
    submit=SubmitField('Submit')
