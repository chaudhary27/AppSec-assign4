from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, SpellForm, logHistoryForm, queryHistoryForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Spell, TimeLog
from datetime import datetime
import subprocess

# Add administrator account
if User.query.filter_by(uname='admin').first() == None:
    admin_pass = open('/run/secrets/admin_pass', 'r').read().strip()
    admin.set_password('Administrator@1')	    admin_2fa = open('/run/secrets/admin_2fa', 'r').read().strip()
    admin = User(uname='admin', two_fa=admin_2fa, admin_role=True)
    admin.set_password(admin_pass)
    # admin = User(uname='admin', two_fa='12345678901', admin_role=True)
    # admin.set_password('Administrator@1')
    db.session.add(admin)
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    regResult = ''
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(uname=form.uname.data, two_fa=form.twoFA.data)
        user.set_password(form.pword.data)
        db.session.add(user)
        db.session.commit()
        regResult = 'success'
        flash(regResult)
        flash('You are now a registered user! Please login in.')
        return render_template('register.html', regResult=regResult, form=form)
    else:
        flash(regResult)
        regResult = 'failure'
        return render_template('register.html', regResult=regResult, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginResult = ''
    form = LoginForm()
    if form.validate_on_submit():
        username = form.uname.data
        user = User.query.filter_by(uname=username).first()
        print(user)
        if user is None or not user.check_password(form.pword.data):
            loginResult = 'Incorrect'
            flash('Invalid username or password')
            return render_template('login.html', loginResult=loginResult, form=form)
        if not user.two_fa == form.twoFA.data:
            loginResult = 'Two-factor failure'
            flash('Invalid two-factor number')
            return render_template('login.html', loginResult=loginResult, form=form)
        newLogin = TimeLog(uname=username, login_time=datetime.utcnow())
        db.session.add(newLogin)
        db.session.commit()
        loginResult = 'success'
        flash('You have logged in successfully!')
        login_user(user)
    return render_template('login.html', loginResult=loginResult, form=form)

@app.route('/logout')
def logout():
    currUser = current_user.uname
    updateLog = TimeLog.query.filter_by(uname=currUser, logout_time=None).first()
    updateLog.logout_time = datetime.utcnow()
    db.session.add(updateLog)
    db.session.commit()
    logout_user()
    flash('You have logged out successfully!')
    return redirect(url_for('index'))

@app.route('/login_history', methods=['GET', 'POST'])
@login_required
def login_history():
    form = logHistoryForm()
    currUser = current_user

    if currUser.admin_role == True:
        if form.validate_on_submit():
            inputtext = form.userid.data
            logUser = TimeLog.query.filter_by(uname=inputtext).first()
            if logUser != None:
                flash('Query is successful!')
                allHistory = TimeLog.query.filter_by(uname=inputtext).all()
                return render_template('login_history.html', allHistory=allHistory, form=form)
            else:
                flash('Login history is not available for user!')
    else:
        return "Unauthorized"
    return render_template('login_history.html',form=form)

@app.route('/spell_check', methods=['GET', 'POST'])
@login_required
def spellcheck():
    form = SpellForm()
    currUser = current_user.uname
    if form.validate_on_submit():
        inputtext = form.inputtext.data
        with open('userinput.txt', 'w') as file:
            file.write(form.inputtext.data)
            file.close()
        textoutput = subprocess.run(['./a.out', 'userinput.txt', 'wordlist.txt'], stdout=subprocess.PIPE, check=True, universal_newlines=True)
        textmisspell = textoutput.stdout.replace("\n", ", ")[:-2]
        if textmisspell == "":
            textmisspell = "No words were misspelled."

        entry = Spell(uname=currUser, query_text=inputtext, query_results=textmisspell)
        db.session.add(entry)
        db.session.commit()
        return render_template('spell_check.html', textoutput=textoutput.stdout, textmisspell=textmisspell, form=form)
    return render_template('spell_check.html', form=form)

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    form = queryHistoryForm()
    currUser = current_user

    if currUser.admin_role == True:
        if form.validate_on_submit():
            inputtext = form.userquery.data
            qUser = Spell.query.filter_by(uname=inputtext).first()
            if qUser != None:
                allHistory = Spell.query.filter_by(uname=inputtext).all()
                count = len(allHistory)
                return render_template('history.html', user=inputtext, allHistory=allHistory, count=count, form=form)
            else:
                flash('Spell history is not available for user!')
        return render_template('history.html', form=form)
    else: #not admin
        allHistory = Spell.query.filter_by(uname=currUser.uname).all()
        count = len(allHistory)
        return render_template('history.html',user=currUser.uname, count=count, allHistory=allHistory, form=form)

@app.route('/history/query<num>')
@login_required
def query(num):
    currUser = current_user
    qUser = Spell.query.filter_by(id=num).first()

    if currUser.admin_role == True:
        querydetail = Spell.query.filter_by(id=num).all()
        return render_template('query.html', querydetail=querydetail)
    elif currUser.uname == qUser.uname:
        querydetail = Spell.query.filter_by(id=num).all()
        return render_template('query.html', querydetail=querydetail)
    else:
        return "Unauthorized"
