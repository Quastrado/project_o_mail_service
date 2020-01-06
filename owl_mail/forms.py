from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FormField, Form, StringField, SelectField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'Login'})
    password = PasswordField('', validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Remember me', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-light"})

class StudentForm(FlaskForm):
    name = StringField('', validators=[DataRequired()], render_kw={'placeholder':'Name'})
    surname = StringField('', render_kw={'placeholder':'Surname'})
    email = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    date_of_birth = DateField('', format='%Y-%m-%d', validators=[DataRequired()], render_kw={'placeholder': '0000/00/00'})
    house_number_and_street = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'house number and street'})
    area = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'area'})
    locality = StringField('', validators=[DataRequired()], render_kw={'placeholder': 'locality'})
    subaddress = StringField('', render_kw={'placeholder': 'Subaddress'})
    owl = SelectField('', choices=[
        ('Eared Owl', 'eared owl'),
        ('White Owl', 'white owl'),
        ('Barn Owl', 'barn owl'),
        ('Tawny Owl', 'tawny owl')
        ],
        validators=[DataRequired()]
        )
    menu = SubmitField('Menu')
    submit = SubmitField('Submit')
    

class ContentForm(FlaskForm):
    name = StringField('Name:', render_kw={'readonly': True})
    surname = StringField('Surname:', render_kw={'readonly': True})
    email = StringField('Email:', render_kw={'readonly': True})
    date_of_birth = StringField('Date of birth:', render_kw={'readonly': True})
    address = StringField('Address:', render_kw={'readonly': True})
    subaddress = StringField('Subaddress:', render_kw={'readonly': True})
    owl = StringField('Deliveryman:', render_kw={'readonly': True})
    to_fix = SubmitField('To fix')
    submit = SubmitField('Subscribe')
    

class FinishForm(FlaskForm):
    write_another = SubmitField('Write another', render_kw={"class": "btn btn-light"})
    menu = SubmitField('Menu', render_kw={"class": "btn btn-light"})
    logout = SubmitField('Logout', render_kw={"class": "btn btn-light"})


class CheckForm(FlaskForm):
    checkbox = BooleanField()
    file_name = StringField(validators=[DataRequired()], render_kw={'readonly': True})


class CheckTableForm(FlaskForm):
    files = FieldList(FormField(CheckForm), min_entries=0)
        