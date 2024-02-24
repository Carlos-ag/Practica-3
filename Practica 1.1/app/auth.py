from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "secret"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
