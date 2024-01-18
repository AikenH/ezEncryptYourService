from flask import Flask, request, jsonify, redirect, render_template, make_response
import jwt
import os
import datetime
import secrets
from gevent import pywsgi
from dotenv import load_dotenv


# Load Environment Variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Use a strong secret key

# @app.route('/')
# def home():
#     # Check if user is already logged in
#     token = request.cookies.get('token')
#     if token:
#         try:
#             jwt.decode(token, app.secret_key, algorithms=['HS256'])
#             return redirect('/')  # Redirect to service1 if already logged in
#         except:
#             pass  # If token is invalid, proceed to login page

#     return render_template('login.html')  # Simple login interface

@app.route('/login', methods=['POST', 'GET'])
def login():
    count = update_visit_count()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate credentials (use a secure method in production)
        if username == os.getenv('chat_username') and password == os.getenv('password'):
            token = jwt.encode({
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.secret_key, algorithm='HS256')

            response = make_response(redirect('/'))
            response.set_cookie('token', token, max_age=1800)  # Keep login status for 30 mins
            return response
        
        error = 'Invalid credentials'
        return render_template('login.html', error=error, count=count), 401
    
    # Show login page
    return render_template('login.html',count=count)

def token_required(f):
    def decorator(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            print('token is none')
            return redirect('/login')
        try:
            jwt.decode(token, app.secret_key, algorithms=['HS256'])
        except:
            print('token is invalid')
            return redirect('/login')
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

# @app.route('/chat/')
# @token_required
# def service():
#     # If token is valid, the user can access the service
#     return redirect('/chat/')

@app.route('/verify_token')
def verify_token():
    token = request.cookies.get('token')
    if not token:
        return 'Access Denied', 401

    try:
        jwt.decode(token, app.secret_key, algorithms=['HS256'])
        return 'Authorized', 200
    except:
        return 'Access Denied', 401
    
# Function to generate a new secret key and write it to the .env file
def update_secret_key_in_env():
    env_file_path = '.env'
    secret_key = f'SECRET_KEY={secrets.token_urlsafe(32)}'
    last_updated = f'LAST_UPDATED={datetime.datetime.now().strftime("%Y-%m-%d")}'
    key_updated = False

    # Check if .env file exists and read the content
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as file:
            lines = file.readlines()

        # Update or add SECRET_KEY and LAST_UPDATED
        for i, line in enumerate(lines):
            if 'LAST_UPDATED' in line:
                last_updated_date = line.strip().split('=')[1]
                if last_updated_date != datetime.datetime.now().strftime("%Y-%m-%d"):
                    lines[i] = last_updated + '\n'
                    key_updated = True
            elif 'SECRET_KEY' in line:
                if key_updated is True:
                    lines[i] = secret_key + '\n'
                else:
                    print("no need to update the secret key today")
                key_updated = True

        # If SECRET_KEY or LAST_UPDATED are not found, add them
        if not key_updated:
            lines.append(last_updated + '\n')
            lines.append(secret_key + '\n')
            key_updated = True

        # Write back to .env file
        with open(env_file_path, 'w') as file:
            file.writelines(lines)

    else: # If .env file doesn't exist, create one
        with open(env_file_path, 'w') as file:
            file.writelines([last_updated + '\n', secret_key + '\n'])
        key_updated = True

    if key_updated:
        print("Secret key and last updated date added/updated in .env file.")
    else:
        print("No update required for today.")


def update_visit_count():
    try:
        with open("visit_count.txt", "r") as file:
            count = int(file.read())
        with open("visit_count.txt", "w") as file:
            count += 1
            file.write(str(count))
        return count
    except IOError:
        return "Error"


if __name__ == '__main__':
    update_secret_key_in_env()
    server = pywsgi.WSGIServer(('::', 5000), app)
    server.serve_forever()
    # app.run(debug=True, host="::")
