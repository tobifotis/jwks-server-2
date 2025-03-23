import datetime
import jwt
import base64
from flask import Blueprint, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa
from app.db import save_private_key, fetch_key
from cryptography.hazmat.primitives import serialization

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/generate-keys', methods=['POST'])
def generate_keys():
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    valid_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    expired_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    save_private_key(valid_key, now + 3600)      # Valid 1 hour
    save_private_key(expired_key, now - 3600)    # Expired 1 hour ago

    return jsonify({"message": "Keys generated"}), 201

@auth_bp.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    expired = request.args.get('expired', 'false').lower() == 'true'
    kid, private_key = fetch_key(expired)

    if not private_key:
        return jsonify({'error': 'No key available'}), 404

    payload = {
        'sub': data['username'],
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30) if not expired else datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=30)
    }

    token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': str(kid)})
    return jsonify({'token': token})

@auth_bp.route('/.well-known/jwks.json', methods=['GET'])
def get_jwks():
    import sqlite3
    from app.db import DB_NAME

    keys = []
    now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT kid, key FROM keys WHERE exp > ?", (now,))

    for kid, pem_key in cursor.fetchall():
        private_key = serialization.load_pem_private_key(pem_key, password=None)
        public_key = private_key.public_key()
        public_numbers = public_key.public_numbers()

        n = base64.urlsafe_b64encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, 'big')).decode('utf-8').rstrip('=')
        e = base64.urlsafe_b64encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, 'big')).decode('utf-8').rstrip('=')

        keys.append({
            "kid": str(kid),
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig",
            "n": n,
            "e": e
        })

    connection.close()
    return jsonify({'keys': keys})
