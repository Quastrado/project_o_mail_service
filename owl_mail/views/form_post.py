# Midas, i know you'd like to see a class here,
# but Even told me it's like to use a cannon on vorobey
from flask import flash, redirect, render_template, session, url_for
from owl_mail.forms import StudentForm
from owl_mail.models import db, Docs

def form_post_processing():
    states = session['write_states']
    form = StudentForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)  # form=form
    
    exists = db.session.query(Docs.id).filter(Docs.email == form.email.data).scalar()
    if exists is not None:
        flash('Specified email already exists')
        form.email.data = ''
        return render_template('index.html', form=form)  # form=form
    
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
    return redirect(url_for('stamp_post'))
