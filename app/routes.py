# routes for the flask app

from app import app
from app.forms import ContactForm
from flask import render_template, redirect, url_for


# index or home route
@app.route('/')
def index():
    return render_template('index.html')

# contact route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # creating a form instance to be used
    form = ContactForm()

    # this will check that the form was submitted succesfully
    # when validation checks are run against the input
    if form.validate_on_submit():
        # prints out the data dict from form class
        for data, value in form.data.items():
            print(f'{data} {value}')
        return redirect(url_for('index'))
    return render_template('addcontact.html', form=form)