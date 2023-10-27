# routes for the flask app

from app import app, db
from app.models import Address
from app.forms import ContactForm
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


@app.route('/address')
def get_addresses():
    # get all addresses
    address = Address.query.all()
    result = [a.to_dict() for a in address]
    return result

@app.route('/address/<address_id>')
def get_address_by_id(address_id):
    address  = db.session.get(Address, address_id)

    if not address:
        return {'error': f"Address with this ID {address_id} can't be found"}, 404
    else:
        return address.to_dict()
    
@app.route('/address/add', methods=['POST'])
def add_new_address():

    # checking if data payload is json
    if not request.is_json:
        return {'error': "Data passed ,ust be of type JSON"}, 400
    
    data = request.json
    # checking for missing fields
    requiredFields = ['first_name', 'last_name', 'phone_number', 'address']
    missingFields = []
    for key in requiredFields:
        if key not in data:
            missingFields.append(key)
    if missingFields:
        return f"Some fields are required... please enter these fields: {','.join(missingFields)}", 400
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone = data.get("phone_number")
    address = data.get("address")
    print(address, first_name, last_name, phone)

    # check if phone number already exists
    result = db.session.execute(db.select(Address).where(Address.phone_number==phone)).scalars().all()

    if result:
        return {'error': 'This phone number is already being used'}, 403
    
    new_address = Address(first_name=first_name, last_name=last_name, phone_number = phone, address=address)
    print(new_address)

    db.session.add(new_address)
    db.session.commit()

    return {'message': f"New address id {new_address.id} has been created"}
