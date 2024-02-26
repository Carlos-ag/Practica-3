from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "admin"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return True
    return False
