# routes for the flask app

from app import app, db
from app.models import Address, User
from app.forms import ContactForm, RegisterForm, LoginForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user

# index or home route
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# contact route
@app.route('/contact', methods=['GET', 'POST'])
@login_required
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
            return redirect(url_for('dashboard'))
        
        new_address = Address(first_name=first_name, last_name=last_name, phone_number = phone, address=address, user_id=current_user.user_id)
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
        first_name = form.data.get('first_name')
        last_name = form.data.get('last_name')
        email = form.data.get('email')
        password = form.data.get('password')
        image_url = form.data.get('image_url', None)

        # check if user already has this email
        emails = db.session.execute(db.select(User).where(User.email==email)).scalars().all()

        if emails:
            flash(f'email: {email} has already been used... Try another email')
            return redirect(url_for('register'))
        
        # print(User.default_image_url)
        
        # now creating a new user
        if image_url:
            new_user = User(first_name=first_name, last_name=last_name,email=email, password=password, image_url=image_url)
        else:
            new_user = User(first_name=first_name, last_name=last_name,email=email, password=password)

        # adding new user
        db.session.add(new_user)
        db.session.commit()
        print(form.data)
        return redirect(url_for('login'))

    return render_template('register.html', form=form )

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        print(form.data)
        email = form.data.get('email')
        password = form.data.get('password')
        remmeber_me = form.data.get('remember_me')

        # check if email exists
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user is not None and user.check_password(password):
            flash("Welcome! You have logged in!")
            login_user(user, remember=remmeber_me)

        return redirect(url_for('dashboard'))

    return render_template('login.html', form=form )


@app.route('/dashboard')
@login_required
def dashboard():

    user = current_user
    addresses = user.addresses
    return render_template('dashboard.html', addresses=addresses)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have just logged out")
    return redirect(url_for('index'))


@app.route('/contact/edit/<contact_id>', methods=['GET', 'POST'])
@login_required
def edit_contact(contact_id):
    contact = db.session.get(Address, contact_id)

    # check if this is for the current user
    if current_user != contact.addresses:
        flash("This id is not yours")
        return redirect(url_for('dashboard'))

    if not contact:
        flash("This dont exist")
        return redirect(url_for('dashboard'))
    data_dict = {
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "phone_number": contact.phone_number,
        "address": contact.address
    }
    form = ContactForm(data=data_dict)

    if form.validate_on_submit():
        contact.first_name = form.data.get('first_name')
        contact.last_name = form.data.get('last_name')
        contact.phone_number = form.data.get('phone_number')
        contact.address = form.data.get('address')

        db.session.commit()
        flash("Contact Has been updated!")
        return redirect(url_for('dashboard'))
    
    return render_template('editContact.html', form=form)

@app.route('/contact/delete/<contact_id>')
@login_required
def delete_contact(contact_id):
    address = db.session.get(Address, contact_id)

    # check if address is existing
    if not address:
        flash("This Item dont exist")
        return redirect(url_for('dashboard'))
    
    if current_user != address.addresses:
        flash("You dont have access to delete this item")
        return redirect(url_for('dashboard'))
    
    # deleteing contact now
    db.session.delete(address)
    # dont forget to commit changes
    db.session.commit()
    flash("Address has been Deleted")
    return redirect(url_for("dashboard"))
