import json
from modules import statistic
from utils import settings
from utils import oauth
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = settings.session_secret

@app.route('/')
def redir():
    return redirect('/index')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def authorize():
    session['instance'] = request.form['instance']
    session['client_id'], session['client_secret'] = oauth.make_app(session['instance'])
    return redirect(session['instance'] + '/oauth/authorize?client_id=' + session['client_id'] + '&redirect_uri=' + settings.host + '/r&response_type=code&scope=read')

@app.route('/r')
def calc():
    if request.args.get('error'):
        return redirect('/index')
    access_code = request.args.get('code')
    response = oauth.get_token(session['instance'], session['client_id'], session['client_secret'], access_code)
    session['token'] = response.json()['access_token']
    result = statistic.calculate(session['instance'], session['token'])
    oauth.revoke_token(session['instance'], session['client_id'], session['client_secret'], session['token'])
    return render_template('statpage.html', result = result, instance = session['instance'], host = settings.host)

@app.errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)