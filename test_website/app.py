from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import pymysql
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from dotenv import load_dotenv
import threading
from flask_socketio import SocketIO
from websocket import create_connection

#laptop: "C:\Users\simon\Documents\GitHub\testwebsite\test_website"
#pc: Users
# gmail wachtwoord: tnsh ezxm ufxe hdlh
# capitant wachtwoord: trkw aiye xdqq jhct

load_dotenv()

# Flask app configuration
app = Flask(__name__)
app.secret_key = 'CocacolC123!'

# Database configuration
def get_db():
    db = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=int(os.getenv('POSTGRES_PORT', 6543)),
        database=os.getenv('POSTGRES_DATABASE'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return db

############################################################
############################################################
current_ticker = 'NASDAQ:AAPL'
last_price = None  # Variabele om de laatste prijs op te slaan
ws = None  # Houd de WebSocket-verbinding bij

def fetch_live_price():
    global ws, current_ticker, last_price
    socket = 'wss://widgetdata.tradingview.com/socket.io/websocket'
    ws = create_connection(socket)
    session_id = "qs_session_live"
    
    def create_msg(ws, fun, arg):
        ms = json.dumps({"m": fun, "p": arg})
        msg = '~m~' + str(len(ms)) + '~m~' + ms
        ws.send(msg)

    create_msg(ws, 'quote_create_session', [session_id])
    create_msg(ws, 'quote_set_fields', [session_id, "lp"])
    create_msg(ws, 'quote_add_symbols', [session_id, f"{current_ticker}"])

    while True:
        try:
            res = ws.recv()
            print(res)
            
            if '~h~' in res:
                ws.send(res)
                print('Pong sent!')
                continue
            
            if 'lp' in res:
                price_match = re.search(r'"lp":([\d.]+)', res)
                if price_match:
                    last_price = float(price_match.group(1))  # Sla de laatste prijs op
                    print(f"Laatste prijs opgeslagen: {last_price}")
                    #socketio.emit('price_update', {'price': last_price})
        except Exception as e:
            print(f"WebSocket error: {e}")
            break

@socketio.on('change_ticker')
def change_ticker(data):
    global current_ticker, ws
    current_ticker = data['ticker']  # Update de ticker
    print(f"Ticker gewijzigd naar: {current_ticker}")
    
    # Update de ticker in de bestaande WebSocket-verbinding
    session_id = "qs_session_live"
    def create_msg(ws, fun, arg):
        ms = json.dumps({"m": fun, "p": arg})
        msg = '~m~' + str(len(ms)) + '~m~' + ms
        ws.send(msg)

    create_msg(ws, 'quote_add_symbols', [session_id, f"{current_ticker}"])

@socketio.on('get_last_price')
def send_last_price():
    global last_price
    if last_price is not None:
        socketio.emit('price_update', {'price': last_price})
    else:
        socketio.emit('price_update', {'price': 'No price available'})

# Run WebSocket in a separate thread
threading.Thread(target=fetch_live_price).start()
############################################################
############################################################

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'simon.lipperts@capitant.be' 
app.config['MAIL_PASSWORD'] = 'trkw aiye xdqq jhct'
mail = Mail(app)

# Flask routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/sign_up', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')
    else:
        first_name_signup = request.form['voornaam'] #is gekoppeld aan het name attribuut in input tag
        last_name_signup = request.form['last_name']
        age_signup = request.form['age']
        study_signup = request.form['study']
        email_signup = request.form['email']
        password_signup = request.form['password']
        repeat_password_signup = request.form['repeat_password']

        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM investors WHERE first_name = %s AND last_name = %s AND \
                                                    age = %s AND study = %s AND email = %s AND \
                                                    password = %s AND repeat_password = %s', \
                                                    (first_name_signup, last_name_signup, int(age_signup), study_signup, \
                                                        email_signup, password_signup, repeat_password_signup))
        result = cur.fetchone()
        #hier kan ik better enkel de email ophalen en dan zeggen, als je die al in de database zit dan kun niet meer registreren
        if result:
            return 'Error (You already have an account!)'
        elif password_signup != repeat_password_signup:
            return "Error (Your passwords don't match!)"
        elif len(password_signup) > 25:
            return 'Error (your password is too long!)'
        elif len(age_signup) > 2:
            return 'Error (Unfeasible age!)'
        elif len(first_name_signup) > 15 or len(last_name_signup) > 15:
            return 'Error (One of your names is too long!)'
        elif len(study_signup) > 50 or len(email_signup) > 50:
            return 'Error (your email or field of study is too long!)'
        else:
            s = URLSafeTimedSerializer('ThisIsASecret!')
            token = s.dumps(email_signup, salt = 'email-confirm')
            msg = Message('Confirm your Email', sender=('Capitant Team', 'simon.lipperts@capitant.be'), recipients=[email_signup])
            link = url_for('confirm_email', token=token, _external=True)
            msg.html = render_template('email.html', first_name_signup=first_name_signup, link=link) 
            mail.send(msg)

            cur.execute('INSERT INTO investors (first_name, last_name, age, study, email, password, repeat_password) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s)',(first_name_signup, last_name_signup, age_signup, study_signup, \
                                                                email_signup, password_signup, repeat_password_signup))
            db.commit()
            db.close()
            cur.close()
            return redirect('/log_in')
        
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        s = URLSafeTimedSerializer('ThisIsASecret!')
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return 'Error (The confirmation link has expired!)'
    except:
        return 'Error (Invalid confirmation link!)'
    
    db = get_db()
    cur = db.cursor()
    cur.execute('UPDATE investors SET email_confirmed = %s WHERE email = %s', (True, email))
    db.commit()
    cur.close()
    db.close()
    return redirect('/log_in')

#waarschijnlijk is het niet goed om dezelfde tag names te gebruiken voor de login als voor de signup
@app.route('/log_in', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
@app.route('/sign_in', methods=['GET', 'POST'])
@app.route('/signin', methods=['GET', 'POST'])
def log_in():
    if request.method == 'GET':
        return render_template('log_in.html')
    else:
        #dit moet veranderd worden in email
        first_name_login = request.form['first_name']
        last_name_login = request.form['last_name']
        password_login = request.form['password']

        session['first_name_login'] = first_name_login
        #session['last_name_login'] = last_name_login
        #session['password_login'] = password_login

        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM investors WHERE first_name = %s AND last_name = %s AND password = %s',(first_name_login, last_name_login, password_login))
        result = cur.fetchone()
        if result:
            session['first_name_login'] = first_name_login

            db.close()
            cur.close()
            return redirect('/chart')
        else:
            return render_template('log_in.html', login_failed = True) #hier moet eigenlijk ook de data van de vorige keer onthouden worden en een bericht weergegeven worden met log_in failed
        
@app.route('/chart')
def simulation():
    if 'first_name_login' in session:
        first_name_login = session['first_name_login']
        return render_template('chart.html')
    else:
        return redirect('/log_in')

# FLASK_DEBUG=1
if __name__ == '__main__':
    app.run(debug=True)