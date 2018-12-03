import requests
import datetime 
import json

class Seeder(object):
    def __init__(self):
        self.LOCAL_URL = 'http://localhost:5000'
        self.TIME_DELAYS = {
            "one_day": (datetime.datetime.now() + datetime.timedelta(days=1)).timestamp(),
            "six_hours": (datetime.datetime.now() + datetime.timedelta(hours=6)).timestamp(),
            "five_minutes": (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp(),
        }
        self.user_seeds = [
            {
                'username': "Mindy",
                "password": "12345" 
            },
            {
                "username": "Young",
                "password": "1865"
            },
            {
                "username": "Kevin",
                "password": "applesauce"
            },
        ]

        self.challenge_seeds = [ 
            {
             'text': "Start a conversation with a stranger",
             'timeToFinish': "five_minutes"
            },
            {
             'text': "Call Your Parents",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Spend 5 Minutes Reading",
             'timeToFinish': 'five_minutes'
            },
            {
             'text': "Learn the Heimlich Manuever",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Learn to Tie a Square Knot",
             'timeToFinish': 'five_minutes'
            },
            {
             'text': "Learn a Card Trick",
             'timeToFinish': 'one_day'
            },
            {
             'text': "Write a Letter to your Future Self",
             'timeToFinish': 'one_day'
            },
            {
             'text': "Find out the Meaning of your Name",
             'timeToFinish': 'one_day'
            },
            {
             'text': "Learn a Word in a Different Language",
             'timeToFinish': 'five_minutes'
            },
            {
             'text': "Listen to a Song/Genre you Never Heard Before",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Tell Someone You Appreciate Them",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Stay Off Social Media for the Day",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Learn to do a Perfect Push up",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Learn to Make a Paper Airplane",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Learn to Solve a Rubiks Cube",
             'timeToFinish': 'six_hours'
            },
            {
             'text': "Meditate for 5 minutes",
             'timeToFinish': 'five_minutes'
            },
            {
             'text': "Make a Bucket List",
             'timeToFinish': 'five_minutes'
            },
            {
             'text': "Try a New Food",
             'timeToFinish': 'one_day'
            },
            {
             'text': "Call Someone you Haven't Talked to in a While",
             'timeToFinish': 'one_day'
            },
            {
             'text': "Volunteer/Sign Up to Volunteer for Something",
             'timeToFinish': 'one_day'
            },
            {
             'text': "Do a Cartwheel",
             'timeToFinish': 'one_day'
            },
        ]

        self.seed_challenges(self.challenge_seeds)
        self.seed_users(self.user_seeds)
        self.seed_completions()

    def seed_challenges(self, challenges):
        for c in challenges:
            requests.post(self.LOCAL_URL + '/api/challenges/', data=json.dumps(c))
    def seed_users (self, users):
        for u in users:
            requests.post(self.LOCAL_URL + '/api/users/signup/', data=json.dumps(u))
    def seed_completions(self):
        #setup challenges
        greg_start_second_challenge = {
            "user_id": 1,
            "challenge_id": 2,
        }
        martha_start_first_challenge = {
            'user_id': 2,
            'challenge_id': 1
        }
        greg_start_third_challenge = {
            "user_id": 1,
            "challenge_id": 3,
        }
        greg_start_fifth_challenge = {
            "user_id": 1,
            "challenge_id": 5,
        }
        #start challenges
        requests.post(self.LOCAL_URL + '/api/users/start_challenge/', data=json.dumps(greg_start_second_challenge))
        requests.post(self.LOCAL_URL + '/api/users/start_challenge/', data=json.dumps(martha_start_first_challenge))
        requests.post(self.LOCAL_URL + '/api/users/start_challenge/', data=json.dumps(greg_start_third_challenge))
        requests.post(self.LOCAL_URL + '/api/users/start_challenge/', data=json.dumps(greg_start_fifth_challenge))

        #finish challenges, streak should also update, 1 for both greg and martha because under 24hrs
        requests.post(self.LOCAL_URL + '/api/users/complete_challenge/', data=json.dumps(greg_start_second_challenge))
        requests.post(self.LOCAL_URL + '/api/users/complete_challenge/', data=json.dumps(martha_start_first_challenge))
        requests.post(self.LOCAL_URL + '/api/users/complete_challenge/', data=json.dumps(greg_start_third_challenge))
        requests.post(self.LOCAL_URL + '/api/users/complete_challenge/', data=json.dumps(greg_start_fifth_challenge))

if __name__ == '__main__':
    Seeder()
