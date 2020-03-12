from datetime import datetime
from flask import current_app as app
from flask import flash, redirect, render_template, request, jsonify, session, url_for
from flask_login import  login_required,login_user, logout_user
from owl_mail.check import Check
from owl_mail.forms import CheckForm, CheckTableForm, LoginForm, StudentForm, ContentForm
from owl_mail.models import db, User, Docs
from owl_mail.save_data import to_xml
from owl_mail.views.back_to_menu import Menu
from owl_mail.views.slider import Slider
import owl_mail.save_data as SD

from wtforms import FieldList, FormField


@app.route('/')
def start():
    write_states = {
        'spelling': False,
        'view': False
    }
    session['write_states'] = write_states
    print(f'session at start:/n{session}' )
    return redirect(url_for('login'))  # here maust be 'login'


@app.route('/login')
def login():
    title = "Who are you?"
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@app.route('/process-login', methods=['POST'])
def process_login():  # need import User, db / redirect, flash, url_for ???
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('menu'))

    flash('Invalid username or password')
    return redirect(url_for('login'))


@app.route('/logout_btn')
def logout_btn():
    return render_template('logout.html')

@app.route('/logout')
def logout():  # need import flash, redirect, url_for / logout_user
    logout_user()
    return redirect(url_for('login'))

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/wrong')
def wrong():
    return render_template('wrong.html')

@app.route('/menu')
@login_required
def menu():
    print(f'session at menu:/n{session}' )
    slider = Slider()
    picture = slider.random_picture()
    return render_template('menu.html', picture=picture)

@app.route('/back_to_menu')
def back_to_menu():
    menu = Menu()
    return menu.back('menu')


@app.route('/form_post', methods=['GET', 'POST'])
@login_required
def form_post():
    states = session['write_states']
    form = StudentForm()
    if request.method == 'POST':
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
                states['spelling'] = True
                session['write_states'] = states
                return redirect(url_for('stamp'))

    return render_template('index.html', form=form)  # form=form


@app.route('/stamp', methods=['GET', 'POST'])
@login_required
def stamp():
    states = session['write_states']
    if states['spelling']:
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

        # if form.to_fix.data:
        #     return redirect(url_for('form_post'))
        # elif form.submit.data:
        if form.validate_on_submit():
            try:
                SD.execute_save(c_dict)
                states['view'] = True
                session['write_states'] = states
                return redirect(url_for('finish'))
            except Exception:
                flash(
                    'Something went wrong in working with the s3 service.'
                    'The document was not saved'
                    )
        return render_template('show_data.html', form=form, img=img)
    else:
        return redirect(url_for('wrong'))


@app.route('/finish', methods=['GET', 'POST'])
@login_required 
def finish():
    states = session['write_states']
    if states['view']:
        return render_template('finish.html')
    else:
        return redirect(url_for('wrong'))


@app.route('/check', methods=['GET', 'POST'])
def check():
    inst_check = Check()
    data_list = db.session.query(Docs.id, Docs.name, Docs.date_of_creation).all()
    form = CheckTableForm()
    name_list = []
    date_of_creation_list = []
    for file_id, name, date in data_list:
        file_form = CheckForm()
        file_form.checkbox = False
        form.files.append_entry(file_form)
        file_form.file_name = str(file_id)
        print(str(file_id))
        print(file_form.file_name)
        name_list.append(name)
        date_of_creation_list.append(date.strftime('%d-%m-%Y'))
    
    try:
        if inst_check.files_count_discrepancy() == True or inst_check.file_names_discrepancy() == True:
            message = """
                Data Security at Risk. 
                Information about the number of files is not reliable. 
                Or the names do not matched
                """
            flash(message)
    except Exception:
        flash("""
            Something went wrong in working with the s3 service.
            Failed to get information about stored files
            """)
    
    return render_template('check.html', form = form, 
                                        name_list = name_list,
                                        date_of_creation_list = date_of_creation_list)


@app.route('/check_option', methods=['POST'])
def check_option():
    form = CheckForm()
    inst_check = Check()
    if request.method == 'POST':
        values_list = request.form.getlist('data[]')
        files = inst_check.hash_compare(values_list)
        return jsonify(files)


@app.route('/delete_option', methods=['POST'])
def delete_option():
    form = CheckForm()
    inst_check = Check()
    if request.method == 'POST':
        values_list = request.form.getlist('data[]')
        deleted_docs = inst_check.delete_docs(values_list)
        return jsonify(deleted_docs)

@app.route('/slider', methods=['GET'])
def slider():
    slider = Slider()
    picture = slider.random_picture()
    if request.method == 'GET':
        return picture

    return render_template('slider.html', picture=picture)
