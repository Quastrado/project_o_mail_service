from datetime import datetime

import boto3

from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user

import owl_mail.check as C
from config import BaseConfig

from owl_mail.forms import LoginForm, StudentForm, ContentForm, FinishForm
from owl_mail.models import db, User, Docs
from owl_mail.save_data import to_xml
import owl_mail.save_data as SD


@app.route('/')
def start():
    return redirect(url_for('login'))  # here maust be 'login'


@app.route('/login')
def login():
    title = "Who are you?"
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():  # need import User, db / redirect, flash, url_for ???
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You successfully logged in')
            return redirect(url_for('menu'))

    flash('Invalid username or password')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():  # need import flash, redirect, url_for / logout_user
    logout_user()
    return redirect(url_for('login'))


@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/form_post', methods=['GET', 'POST'])
def form_post():
    form = StudentForm()

    if request.method == 'POST':
        if form.logout.data:
            return redirect(url_for('logout'))
        elif form.submit.data:
            if form.validate_on_submit():
                exists = db.session.query(Docs.id).filter(Docs.email == form.email.data).scalar()
                if exists is not None:
                    flash('Specified email already exists')
                    form.email.data = ''
                else:
                    content_dict = {
                        'Name':  form.name.data,
                        'Surname': form.surname.data,
                        'Email': form.email.data,
                        'Date_of_birth': form.date_of_birth.data,
                        'Address': '{}; {}; {}'.format(
                            form.house_number_and_street.data,
                            form.area.data,
                            form.locality.data
                        ),
                        'Subaddress': form.subaddress.data,
                        'Owl': form.owl.data,
                        'Date_of_creation': ''
                    }
                    session['content'] = content_dict
                    return redirect(url_for('stamp'))

    return render_template('index.html', form=form)  # form=form


@app.route('/stamp', methods=['GET', 'POST'])
def stamp():
    form = ContentForm()
    c_dict = session['content']
    owls = {
        'Eared Owl': '/static/eared-owl.jpg',
        'White Owl': '/static/white-owl.jpg',
        'Barn Owl': '/static/barn-owl.jpg',
        'Tawny Owl': '/static/tawny-owl.jpg'
    }

    form.name.data = c_dict['Name']
    form.surname.data = c_dict['Surname']
    form.email.data = c_dict['Email']
    form.date_of_birth.data = c_dict['Date_of_birth']
    form.address.data = c_dict['Address']
    form.subaddress.data = c_dict['Subaddress']
    form.owl.data = c_dict['Owl']
    img = owls[form.owl.data]

    if form.to_fix.data:
        return redirect(url_for('form_post'))
    elif form.submit.data:
        if form.validate_on_submit():
            try:
                SD.execute_save(c_dict)
                return redirect(url_for('finish'))
            except Exception:
                flash(
                    'Something went wrong in working with the s3 service.'
                    'The document was not saved'
                    )

    return render_template('show_data.html', form=form, img=img)


@app.route('/finish', methods=['GET', 'POST'])
def finish():
    form = FinishForm()
    if form.write_another_entry.data:
        return redirect(url_for('form_post'))
    elif form.logout.data:
        return redirect(url_for('logout'))

    return render_template('finish.html', form=form)


@app.route('/check', methods=['GET', 'POST'])
def check():
    s3 = boto3.client(
        's3',
        aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY,
        region_name = BaseConfig.AWS_REGION,
        )
    
    files = s3.list_objects(Bucket = BaseConfig.AWS_BUCKET_NAME)['Contents']
       
    return render_template('check.html', files = files)

