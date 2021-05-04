#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import setting
import json
from flask import Flask, jsonify, abort, make_response, request, render_template, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import flask_login




app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = setting.secret_key


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {
    setting.basicauth_user: setting.basicauth_pass
}

# Our mock database.
form_users = {}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in form_users:
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in form_users:
        return

    user = User()
    user.id = username

    user.is_authenticated = request.form['password'] == users[username]['password']
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    if check_auth(username, password) == 0:
        global form_users
        user = User()
        user.id = username
        flask_login.login_user(user)
        form_users = {username: {
            'password':password
        }}
        return redirect(url_for('index'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('logout.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


def create_messageheader(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = from_addr
    msg['Date'] = formatdate()
    return msg

def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP(${smtpserver}, 587) #STARTTLS前提のコード
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(flask_login.current_user.id + '@' + ${mailserver_domain}, form_users[flask_login.current_user.id]['password'])
    smtpobj.sendmail(from_addr, to_addr, body_msg.as_string())

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def convert_num_to_name(num, namelist):
    return namelist[str(num)]

def check_auth(username, password):
    smtpobj = smtplib.SMTP(${smtpserver}, 587) #STARTTLS前提のコード
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    try:
        smtpobj.login(username + '@' + ${mailserver_domain}, password)
    except smtplib.SMTPAuthenticationError:
        return 1
    else:
        return 0

def create_body(numlist):
    absent_studentsname = []
    absent_students = ""

    namelist = load_json("./namelist.json")
    for num in numlist:
        absent_studentsname.append(convert_num_to_name(num, namelist))

    for i in range(len(numlist)):
        absent_students += "\n" + str(numlist[i]) + "番　" + absent_studentsname[i]
        if(i != len(numlist) - 1):
            absent_students += '，'

    absents = absent_students + "\nが欠席しました．" if len(numlist) != 0 else "誰も欠席しませんでした．"
    body = "今日は" + absents
    return body


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None


@app.route('/', methods=['GET'])
@auth.login_required
@flask_login.login_required
def index():
    return render_template("index.html", login_name = flask_login.current_user.id + "でログインしています．")

@app.route('/api', methods=['POST'])
@auth.login_required
@flask_login.login_required
def post_app():
    from_addr = flask_login.current_user.id + "@" + ${mailserver_domain}
    to_addr = setting.to_addr

    payload = request.json
    token = payload.get("token")
    numlist = list(payload.get("numlist"))


    if token != setting.token:
        result = {
            "status":"401",
            "about":"wrong token"
        }
        return jsonify(result), 401
    
    for num in numlist:
        if num not in range(1,${classmembernum}):
            result = {
            "status":"400",
            "about":"wrong number."
        }
            return jsonify(result), 400
            
    msg = (create_messageheader(from_addr, to_addr, "本日の欠席者", create_body(numlist)))

    try:
        send_mail(from_addr, to_addr, msg)
    except smtplib.SMTPAuthenticationError:
        print("SMTPAuthenticationError")
        exit(1)

    result = {
        "status": "200"
    }
    return jsonify(result), 200

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    response = jsonify({ 
                          "error": {
                            "type": error.name, 
                            "message": error.description 
                          }
                      })
    return response, error.code



def test():
    print("Login Successfully!" if check_auth(${username}, ${password}) == 0  else "Error!")

if __name__ == '__main__':
    app.run(threaded=True)
    #test()
