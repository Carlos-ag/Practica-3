from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {
    "admin": "admin"
}

@auth.verify_password
def verify_password(username, password):
    if username == "guest":
        #print("PASA GUEST")
        return True
    if username in users and users[username] == password:
        #print("PASA OK")
        return True
    else:
        #print("PASA NO OK")
        return False
