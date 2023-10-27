from api import api
from models import Address
from app import db
from flask import request

print(api.name)

@api.route('/address')
def get_addresses():
    # get all addresses
    address = Address.query.all()
    result = [a.to_dict() for a in address]
    return result

@api.route('/address/<address_id>')
def get_address_by_id(address_id):
    address  = db.session.get(Address, address_id)

    if not address:
        return {'error': f"Address with this ID {address_id} can't be found"}, 404
    else:
        return address.to_dict()
    
@api.route('/address/add', methods=['POST'])
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
