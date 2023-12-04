from app import db
from app.models import Users, Account
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

bp = Blueprint('user', __name__)


@bp.route('/invite', methods=['POST'])
@jwt_required()
def invite():
    data = request.get_json()

    attributes = data.get('data', {}).get('attributes', {})
    new_username = attributes.get('new_username')

    if not attributes or not new_username:
        return ({"errors": [{
            "status": "400",
            "detail": "Invalid syntax"
        }]}), 400

    if not current_user.is_owner:
        return ({"errors": [{
            "status": "403",
            "detail": "User must be an owner to invite other users"
        }]}), 403

    existing_user = Users.query.filter_by(username=new_username).first()
    if existing_user:
        return ({"errors": [{
            "status": "422",
            "detail": "User already exists"
        }]}), 422

    temp_password = Users.generate_temp_password()

    new_user = Users(username=new_username, account_id=current_user.account_id)
    new_user.set_password(temp_password)
    db.session.add(new_user)
    db.session.commit()

    return ({"data": {
        "new_username": new_username,
        "temporary_password": temp_password
    }}), 201


@bp.route('/get_info', methods=['GET'])
@jwt_required()
def get_info():
    account_name = Account.query.filter_by(account_id=current_user.account_id).first().account_name
    account_id = Account.query.filter_by(account_id=current_user.account_id).first().account_id
    return ({
        "data": {
            "type": "users",
            "id": current_user.user_id,
            "attributes": {
                "username": current_user.username,
                "account_name": account_name
            },
            "relationships": {
                "account": {
                    "data": {"type": "accounts", "name": account_id}
                }
            }
        }
    })
