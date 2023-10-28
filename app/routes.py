# routes for the flask app

from app import app, db
from app.models import Address
from app.forms import ContactForm, RegisterForm, LoginForm
from flask import render_template, redirect, url_for, flash, request

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
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone_number.data
        address = form.address.data
        print(address, first_name, last_name, phone)

        # check if phone number already exists
        result = db.session.execute(db.select(Address).where(Address.phone_number==phone)).scalars().all()

        if result:
            flash("This number is already being used.")
            return redirect(url_for('contact'))
        
        new_address = Address(first_name=first_name, last_name=last_name, phone_number = phone, address=address)
        print(new_address)

        db.session.add(new_address)
        db.session.commit()
        flash("New Address has been created")
        # prints out the data dict from form class
        # for data, value in form.data.items():
        #     print(f'{data} {value}')
        return redirect(url_for('index'))
    return render_template('addcontact.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        print(form.data)
        return redirect(url_for('index'))

    return render_template('register.html', form=form )

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        print(form.data)
        return redirect(url_for('index'))

    return render_template('login.html', form=form )