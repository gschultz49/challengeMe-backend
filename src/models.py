import hashlib, binascii, os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    streak = db.Column(db.Integer, default=0)
    count_completed_challenges = db.Column(db.Integer, default=0)
    last_completed_challenge = db.Column(db.Integer, default = -1)
    pic = db.Column(db.String, default = False)


    def __init__ (self, **kwargs):
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')
        self.streak = kwargs.get('streak', 0)
        self.count_completed_challenges = kwargs.get('count_completed_challenges', 0)
        self.last_completed_challenge = kwargs.get('last_completed_challenge', -1)
        self.pic = kwargs.get('pic', -1)
    
    def serialize (self):
        return {
            'id': self.id,
            'username': self.username,
            "password": self.password,
            'streak': self.streak,
            'count_completed_challenges': self.count_completed_challenges,
            'last_completed_challenge': self.last_completed_challenge,
            'pic': self.pic
        }
    
    def hash_password(password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
 
    def verify_password(stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

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

    def __init__ (self, **kwargs):
        self.startTime = kwargs.get('startTime')
        self.toFinishTime = kwargs.get('toFinishTime')
        self.endFinishTime = kwargs.get('endFinishTime')

        self.user_id = kwargs.get('user_id')
        self.challenge_id = kwargs.get('challenge_id')

    def serialize (self):
        return {
            'id' : self.id,
            'startTime': self.startTime,
            'toFinishTime': self.toFinishTime,
            'endFinishTime': self.endFinishTime,
            # dont serialize the foreign key
        }