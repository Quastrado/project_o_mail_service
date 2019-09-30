from datetime import datetime
from flask import current_app as app
from flask import flash, redirect, render_template, request, jsonify, session, url_for
from flask_login import login_user, logout_user
from owl_mail.check import Check
from owl_mail.forms import CheckForm, LoginForm, StudentForm, ContentForm, FinishForm
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
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
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
        if form.menu.data:
            return redirect(url_for('menu'))
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
    if form.write_another.data:
        return redirect(url_for('form_post'))
    elif form.menu.data:
        return redirect(url_for('menu'))
    elif form.logout.data:
        return redirect(url_for('logout'))

    return render_template('finish.html', form=form)


@app.route('/check', methods=['GET', 'POST'])
def check():
    inst_check = Check()
    form = CheckForm()    
    id_list = [str(val) for val, in db.session.query(Docs.id).all()]
    name_list = [val for val, in db.session.query(Docs.name).all()]
    date_of_creation_list = [val.strftime('%d-%m-%Y') for val, in 
                            db.session.query(Docs.date_of_creation)]
    count = db.session.query(Docs).count()
    
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
                                        id_list = id_list,
                                        name_list = name_list,
                                        date_of_creation_list = date_of_creation_list,
                                        count = count)


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