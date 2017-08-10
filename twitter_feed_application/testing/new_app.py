from flask import Flask, request, redirect, url_for, session, flash, g, \
     render_template
from flask_oauth import OAuth
import json
from database import database
import twitter as twt

db = database('local')

# configuration
SECRET_KEY = 'development key'
DEBUG = True

# setup flask
app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()
CONSUMER_KEY='xBeXxg9lyElUgwZT6AZ0A'
CONSUMER_SECRET='aawnSpNTOVuDCjx7HMh6uSXetjNN8zWLpZwCEU4LBrk'

# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET
)
def db_update(id, data):

    if id == "1":
        return db.update_views(data)

    if id == "2":
        return db.update_votes(data)

    pass


def get_tweet(page_no):
    auth = twt.oauth.OAuth(g.user['OAUTH_TOKEN'], g.user['OAUTH_SECRET_TOKEN'], CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twt.Twitter(auth=auth)

    page_no = int(page_no)
    print page_no

    if page_no==1:
        session_data = {}
        session_data['data'] = json.dumps(twitter_api.statuses.home_timeline(count=40))
        session_data['user_id'] = session['user_id']
        db.update_user(session_data=session_data)
        g.user['session_data'] = session_data['data']
        pass

    g.user['session_data'] = json.loads(g.user['session_data'])
    #print g.user['session_data']
    return json.dumps({"remark": "successful", "data": db.get_vote_status(g.user['session_data'][(page_no-1)*5 : page_no*5], session['user_id'])})

    #return json.dumps({"remark": "successful", "data": "{}"})

@app.route('/query', methods=['POST'])
def query():
    try:
        if not request.data:
            return '{"remark":"json data expected"}'

        data = request.data
        data = json.loads(data)

        if 'main_id' not in data:
            return '{"remark":"main_id expected"}'
        main_id = data['main_id']

        if not main_id.isdigit():
            return '{"remark": "invalid main id"}'

        # insert
        if int(main_id) == 1:
            if 'id' not in data:
                return '{"remark":"id expected"}'
            id = data['id']

            if 'data' not in data:
                return '{"remark":"data expected"}'

            input_data = data['data']
            #return db_insert(id, input_data)

        # query
        if int(main_id) == 2:

            if 'page_no' not in data:
                return '{"remark":"page_no expected"}'

            page_no = data['page_no']

            return get_tweet(page_no)

        # update
        if int(main_id) == 3:
            if 'id' not in data:
                return '{"remark":"id expected"}'
            id = data['id']

            if 'data' not in data:
                return '{"remark":"data expected"}'

            input_data = data['data']
            return db_update(id, input_data)

        else:
            return '{"remark": "invalid main id"}'
    except Exception as e:
        return '{"remark": "APP :: %s"}' % str(e)
    pass

@app.route('/tweet/<tweet_id>')
def tweet(tweet_id):
    g.user['session_data'] = json.loads(g.user['session_data'])
    for i in g.user['session_data']:
        if i['id_str'] == tweet_id:
            tweet_data = i
            break
        pass
    tweet_data = db.count_for_tweet(tweet_data)
    return render_template('tweet_page.html', tweet_data=tweet_data)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = db.get_user(user_id=session['user_id'])
        #print g.user


@twitter.tokengetter
def get_twitter_token():
    """This is used by the API to look for the auth token and secret
    it should use for API calls.  During the authorization handshake
    a temporary set of token and secret is used, but afterwards this
    function has to return the token and secret.  If you don't want
    to store this in the database, consider putting it into the
    session instead.
    """
    user = g.user
    if user is not None:
        return user['OAUTH_TOKEN'], user['OAUTH_SECRET_TOKEN']


@app.route('/')
def index():
    tweets = None
    if g.user is not None:
        return render_template('main_page.html', user_id=session['user_id'])

    return render_template('index.html', tweets=tweets)


@app.route('/login')
def login():
    """Calling into authorize will cause the OpenID auth machinery to kick
    in.  When all worked out as expected, the remote application will
    redirect back to the callback URL provided.
    """
    if g.user is None:
        return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))
    else:
        return render_template('main_page.html', user_id=session['user_id'])


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    """Called after authorization.  After this function finished handling,
    the OAuth information is removed from the session again.  When this
    happened, the tokengetter from above is used to retrieve the oauth
    token and secret.
    Because the remote application could have re-authorized the application
    it is necessary to update the values in the database.
    If the application redirected back after denying, the response passed
    to the function will be `None`.  Otherwise a dictionary with the values
    the application submitted.  Note that Twitter itself does not really
    redirect back unless the user clicks on the application name.
    """
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    user = db.get_user(user_name=resp['screen_name'])

    # user never signed on
    if user is None:
        db.store_user(resp)
    # in any case we update the authenciation token in the db
    # In case the user temporarily revoked access we will have
    # new tokens here.
    else:
        db.update_user(resp)


    session['user_id'] = user['_id']
    flash('You were signed in')
    return redirect(next_url)


if __name__ == '__main__':
    app.run()