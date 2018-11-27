import json, os, requests, datetime
from models import db, User, Challenge, Completion
from sqlalchemy.sql.expression import func, select
from flask import Flask, request
from flasgger import Swagger, swag_from


db_filename = "CHALLENGEME.db"
app = Flask(__name__)
swagger = Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# weirdly not working if the environ key was made in a different directory?
# GIPHY_API_KEY = os.environ['GIPHY_API_KEY']
GIPHY_API_KEY = 'Dp9D8D67rvtcpLqiMJQQZ02mxmIyuTZf'
GIPHY_SEARCH_URL = 'http://api.giphy.com/v1/gifs/search'

TIME_DELAYS = {
    "one_day": (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp(),
    "six_hours": (datetime.datetime.now() + datetime.timedelta(hours=6)).timestamp(),
    "five_minutes": (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp(),
}

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/challenges/', methods = ['GET'])
@swag_from('../../docs/get_all_challenges.yml')
def get_all_challenges():
    challenges = Challenge.query.all()
    res = {'success': True, 'data':[challenge.serialize() for challenge in challenges] }
    return json.dumps(res), 200


@app.route('/api/challenges/<int:challenge_id>/', methods=['GET'])
@swag_from('../../docs/get_challenge_by_id.yml')
def get_challenge_by_id(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    # invalid challenge id
    print (challenge)
    if challenge is None:
        return json.dumps({'success': False, 'error': 'Invalid challenge ID! Cannot get challenge'}), 404 
        # only if this is a valid challenge ID
    else:
        return json.dumps({'success': True, 'data': challenge.serialize()}), 200
        

@app.route('/api/challenges/', methods=['POST'])
@swag_from('../../docs/create_challenge.yml')
def create_challenge():

    dat = json.loads(request.data)

    text = dat.get("text")

    GIPHY_SEARCH_PARAMETERS = {
        'api_key': GIPHY_API_KEY,
        'limit': 1,
        # default 
        'q': text
    }

    giphy_dat = requests.get(GIPHY_SEARCH_URL, params=GIPHY_SEARCH_PARAMETERS).json()
    
    challenge = Challenge(
        text = text,
        imgURL = giphy_dat['data'][0]['embed_url'],
        timeToFinish = dat.get("timeToFinish")
    )

    db.session.add(challenge)
    db.session.commit()

    res = {
        'success': True,
        'data': challenge.serialize()
    }

    return json.dumps(res), 201

@app.route('/api/challenges/search/<string:q>', methods=['GET'])
@swag_from('../../docs/search_challenges.yml')
def search_challenges(q):
    results = Challenge.query.filter(Challenge.text.like("%"+q+"%")).all()

    res = {
        'success': True,
        'data': [result.serialize() for result in results] 
    }

    return json.dumps(res), 200


@app.route('/api/challenges/<int:challenge_id>/', methods=['DELETE'])
@swag_from('../../docs/delete_challenge_by_id.yml')
def delete_challenge_by_id(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    # only if this is a valid challenge ID
    if challenge is not None:
        db.session.delete(challenge)
        db.session.commit()
        return json.dumps({'success': True, 'data': challenge.serialize()}), 200
    # invalid challenge id
    else:
        return json.dumps({'success': False, 'error': 'Invalid challenge ID! Cannot delete challenge'}), 404 

    

@app.route('/api/challenges/random/', methods=['GET'])
@swag_from('../../docs/get_random_challenge.yml')
def get_random_challenge():
    r = Challenge.query.order_by(func.random()).limit(1).all()
    return json.dumps({'success': True, 'data': r[0].serialize()}), 200

# @app.route('/api/challenges/completed_challenges/', methods=['GET'])
# def show_popular_challenges():



@app.route('/api/users/', methods = ['GET'])
@swag_from('../../docs/get_all_users.yml')
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data':[user.serialize() for user in users] }
    return json.dumps(res), 200


@app.route('/api/users/signup/', methods=['POST'])
@swag_from('../../docs/new_signup.yml')
def new_signup():
    dat = json.loads(request.data)

    user = User(
        username = dat.get("username"),
        password = dat.get("password")
    )

    db.session.add(user)
    db.session.commit()

    res = {
        'success': True,
        'data': user.serialize()
    }
    return json.dumps(res), 201


@app.route('/api/users/login/', methods=['POST'])
@swag_from('../../docs/login_user.yml')
def login_user():
    dat = json.loads(request.data)
    
    q = User.query.filter_by(username = dat.get("username")).filter_by(password = dat.get("password")).first()
    
    if q is not None:
        res = {
            'success': True,
            'data': q.serialize()
        }
        return json.dumps(res), 200
    else:
        return json.dumps({'success': False, 'error': 'Incorrect login'}), 404 


@app.route('/api/users/completions/', methods = ['GET'])
@swag_from('../../docs/get_all_completions.yml')
def get_all_completions():
    completions = Completion.query.all()
    res = {'success': True, 'data':[completion.serialize() for completion in completions] }
    return json.dumps(res), 200


@app.route('/api/users/start_challenge/', methods=['POST'])
@swag_from('../../docs/start_challenge.yml')
def start_challenge():

    dat = json.loads(request.data)
    
    user_id = dat.get("user_id")
    challenge_id = dat.get("challenge_id")

    challenge = Challenge.query.filter_by(id = challenge_id).first()

    completed = Completion(
        #these are all in float timestamps
        startTime = datetime.datetime.now().timestamp(),
        #keep track of the time the challenge must be completed by
        toFinishTime = TIME_DELAYS[challenge.timeToFinish],
        #to be stamped when the user actually finishes
        endFinishTime = "NONE",
        user_id = user_id,
        challenge_id = challenge_id,
    )

    db.session.add(completed)
    db.session.commit()

    res = {
        'success': True,
        "data": completed.serialize()
    }

    return json.dumps(res), 201


@app.route('/api/users/complete_challenge/', methods=['POST'])
@swag_from('../../docs/complete_challenge.yml')
def complete_challenge():
    dat = json.loads(request.data)
    user_id = dat.get("user_id")
    challenge_id = dat.get("challenge_id")
    
    user = User.query.filter_by(id = user_id).first()
    completed = Completion.query.filter_by(user_id = user_id).filter_by(challenge_id = challenge_id).first()
    
    # finish the challenge 
    completed.endFinishTime = datetime.datetime.now().timestamp()
    
    #kinda not needed, fix later
    completed.completed = True

    #will need to have an order by with this to make it such that you can do the same challenge multiple times
    last_completed_challenge = Completion.query.filter_by(id = user.last_completed_challenge).first()

    #if you've never completed a challenge before, auto increment streak
    if last_completed_challenge is None:
        user.streak += 1
    #check if it has been more than 24hrs since last completion, then determine streak increment
    else:
        endFinish = datetime.datetime.utcfromtimestamp(float(last_completed_challenge.endFinishTime)) 
        current_time = datetime.datetime.utcnow()
        one_day_away = (endFinish + datetime.timedelta(hours=1))
        
        if current_time > one_day_away:
            user.streak += 1

    # update users last completed challenge to this one every time
    user.last_completed_challenge = challenge_id

    db.session.commit()

    return json.dumps({'success': True, 'data': completed.serialize()}), 200


@app.route('/api/users/completed_challenges/', methods=['POST'])
@swag_from('../../docs/get_user_completed_challenges.yml')
def get_user_completed_challenges():

    dat = json.loads(request.data)
    user_id = dat.get("user_id")
    # session, cookies? 
    # Leveraging the users ID from the User table so need some way of storing
    
    # completions = Completion.query.filter_by(user_id=user_id)

    # print (completions)
    # user_completions = completions.filter(completions, Completion.challenge_id == Challenge.id)
    # print (user_completions)
    # q = "select * from Challenges join Completions.challenge_id on Challenges.id where Completions.user_id = {0}".format(user_id)
    q = "select * from Challenges inner join Completions on Challenges.id = Completions.challenge_id where Completions.user_id = {0} ".format(user_id)
    user_completions = db.engine.execute(q)
    # user_completions = session.query(Completion).join(Challenge, Completion.user_id==Challenge.id)
    print(user_completions)
    
    serialized= []
    for row in user_completions:
        serialized.append(
            {
                "text": row.text,
                "imgURL": row.imgURL,
                "timeToFinish": row.timeToFinish
            }
        )

    if serialized is not None:
        res = {
            'success': True,
            'data': serialized
        }
        return json.dumps(res), 200
    else:
        return json.dumps({'success': False, 'error': 'No Completed Challenges'}), 404 

@app.route('/api/users/count_completed_challenges/', methods=['POST'])
@swag_from('../../docs/get_user_completed_challenges.yml')
def get_count_user_completed_challenges():
    dat = json.loads(request.data)
    user_id = dat.get("user_id")
    # session, cookies? 
    # Leveraging the users ID from the User table so need some way of storing
    
    completions = Completion.query.filter_by(user_id=user_id).filter_by(completed=True).all()
    print (completions)
    print (len(completions))
    

    if completions is not None:
        res = {
            'success': True,
            'data': len(completions)
        }
        return json.dumps(res), 200
    else:
        return json.dumps({'success': False, 'error': 'No Completed Challenges'}), 404 

# def user_unfinished_challenges


