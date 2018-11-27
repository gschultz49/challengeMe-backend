from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    # name = db.Column(db.String, nullable = False)
    # email = db.Column(db.String, nullable = False)
    # imgUrl = db.Column(db.String)
    # might not be necessary with the completions table
    # totalFinishedChallenges = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_completed_challenge = db.Column(db.Integer, default = -1)



    def __init__ (self, **kwargs):
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')
        # self.name = kwargs.get('name', 'Anonymous')
        # self.email = kwargs.get('name', '')
        # self.imgURL = kwargs.get('imgURL', '')
        # self.totalFinishedChallenges = kwargs.get('totalFinishedChallenges', 0)
        self.streak = kwargs.get('streak', 0)
        self.last_completed_challenge = kwargs.get('last_completed_challenge', -1)
    
    def serialize (self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            # 'name': self.name,
            # 'email': self.email,
            # 'imgURL': self.imgURL,
            # 'totalFinishedChallenges': self.totalFinishedChallenges,
            'streak': self.streak,
            'last_completed_challenge': self.last_completed_challenge
        }

class Challenge(db.Model):
    __tablename__ = "Challenges"

    id = db.Column(db.Integer, primary_key= True)
    text = db.Column(db.String, nullable = False)
    imgURL = db.Column(db.String)
    timeToFinish = db.Column(db.String)


    def __init__ (self, **kwargs):
        self.text = kwargs.get('text', 'N/A')
        self.imgURL = kwargs.get('imgURL', '')
        self.timeToFinish = kwargs.get('timeToFinish')
    
    def serialize (self):
        return {
            'id': self.id,
            'text': self.text,
            'imgURL': self.imgURL,
            'timeToFinish': self.timeToFinish,
        }

class Completion(db.Model):
    __tablename__ = 'Completions'

    id = db.Column(db.Integer, primary_key=True)
    startTime = db.Column(db.String)
    toFinishTime = db.Column(db.String)
    endFinishTime = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('Challenges.id'), nullable = False)
    completed = db.Column(db.Boolean)

    def __init__ (self, **kwargs):
        self.startTime = kwargs.get('startTime')
        self.toFinishTime = kwargs.get('toFinishTime')
        self.endFinishTime = kwargs.get('endFinishTime')

        self.user_id = kwargs.get('user_id')
        self.challenge_id = kwargs.get('challenge_id')
        self.completed = kwargs.get('completed', False)

    def serialize (self):
        return {
            'id' : self.id,
            'startTime': self.startTime,
            'toFinishTime': self.toFinishTime,
            'endFinishTime': self.endFinishTime
            # dont serialize the foreign key
        }