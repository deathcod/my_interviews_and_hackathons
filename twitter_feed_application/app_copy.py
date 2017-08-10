from flask import Flask, request, redirect, url_for, session, g, flash, \
     render_template
from flask_oauth import OAuth

import twitter as tw
 
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
 
# configuration
SECRET_KEY = 'development key'
DEBUG = True
 
# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()


CONSUMER_KEY = 'ElEMDidkpEFVXpcXDiBXXpWHt'
CONSUMER_SECRET = 'iLfLYTvP6Z6JxpXgpqGCm5MzpgFgWbIBUksuPoCAGkCc2KRjd9'
OAUTH_TOKEN = ''
OAUTH_SECRET_TOKEN = ''

print OAUTH_TOKEN, OAUTH_SECRET_TOKEN

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1.1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authorize',
    # the consumer keys from the twitter application registry.
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET
)
 
 
@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')
 
@app.route('/')
def index():
    access_token = session.get('access_token')
    print access_token
    if access_token is None:
        return redirect(url_for('login'))
 
    access_token = access_token[0]
 
    return render_template('index.html')
 
@app.route('/login')
def login():

    # return twitter.authorize(callback=url_for('oauth_authorized',
    #     next=request.args.get('next') or request.referrer or None))

    return twitter.authorize(callback=url_for('oauth_authorized'))
 
 
@app.route('/logout')
def logout():
    session.clear()
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))
 
 
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
 
    OAUTH_TOKEN = resp['oauth_token']
    OAUTH_SECRET_TOKEN = resp['oauth_token_secret']
    session['OAUTH_TOKEN'] = OAUTH_TOKEN
    session['OAUTH_SECRET_TOKEN'] = OAUTH_SECRET_TOKEN

    session['access_token'] = OAUTH_TOKEN
    session['screen_name'] = resp['screen_name']
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    #print OAUTH_TOKEN, OAUTH_SECRET_TOKEN, CONSUMER_KEY, CONSUMER_SECRET

    auth = tw.oauth.OAuth(OAUTH_TOKEN , OAUTH_SECRET_TOKEN , CONSUMER_KEY , CONSUMER_SECRET)
    twitter_api = tw.Twitter(auth =auth)
    #print (twitter_api)


    return redirect(url_for('index'))
 
 
if __name__ == '__main__':
    app.run()