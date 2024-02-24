from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "admin"
}

@auth.verify_password
def verify_password(username, password):
    if not username:
        return 'guest'  # Identifica a un usuario no autenticado
    return username if username in users and users[username] == password else None
