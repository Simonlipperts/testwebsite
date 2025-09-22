from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import pymysql
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
#"C:\Users\simon\OneDrive\Documents\GitHub\testwebsite\test_website"
# gmail wachtwoord: tnsh ezxm ufxe hdlh
# capitant wachtwoord: trkw aiye xdqq jhct


# Flask app configuration
app = Flask(__name__)

# Database configuration
def get_db():
    db = pymysql.connect(
        host='localhost',
        user='root',
        database='trading_sim',
        password='CocacolC123!'
    )
    return db

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com' # of smtp.capitant.be
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
        cur.execute('SELECT * FROM INVESTORS WHERE first_name = %s AND last_name = %s AND \
                                                    age = %s AND study = %s AND email = %s AND \
                                                    password = %s AND repeat_password = %s', \
                                                    (first_name_signup, last_name_signup, int(age_signup), study_signup, \
                                                        email_signup, password_signup, repeat_password_signup))
        result = cur.fetchone()
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
            msg.html = render_template('email.html', first_name_signup, link) f"Hi {first_name_signup}, Great news, you are officially part of the Capitant community! Whether you are here to sharpen your investing skills \
                            or to take your very first steps in the stock market, we are excited to have you on board. Confirm your Email now to get instant access to \
                            howtopickastock.com and to begin your journey in the world of finance. Your confirmation link is: {link}. Happy investing, team Capitant."
            mail.send(msg)

            cur.execute('INSERT INTO INVESTORS (first_name, last_name, age, study, email, password, repeat_password) \
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
    cur.execute('UPDATE INVESTORS SET email_confirmed = %s WHERE email = %s', (True, email))
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
        first_name_login = request.form['first_name']
        last_name_login = request.form['last_name']
        password_login = request.form['password']

        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM INVESTORS WHERE first_name = %s AND last_name = %s AND password = %s',(first_name_login, last_name_login, password_login))
        result = cur.fetchone()
        if result:
            db.close()
            cur.close()
            return redirect('/simulation')
        else:
            return render_template('log_in.html', login_failed = True) #hier moet eigenlijk ook de data van de vorige keer onthouden worden en een bericht weergegeven worden met log_in failed
        
@app.route('/simulation')
def simulation():
    return render_template('simulation.html')

# FLASK_DEBUG=1
if __name__ == '__main__':
    app.run(debug=True)