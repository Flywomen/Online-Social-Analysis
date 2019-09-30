"""
collect.py
collect data used in analysis for the people's evaluation of iPhone X by twitter.
"""
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI

consumer_key = '7LNrKejx44Sv13og0ea8STF8m'
consumer_secret = 'vzsd2pa6HxpHj8pi51ZkqINWqav5CbXZ1MDHDJNggAlyq97ski'
access_token = '905483226852024320-XbqgfwhsBwgBug9o82U3MQJhf8lW6KE'
access_token_secret = '9gDhnAGDPdNlBSwSQPZcnjdCqGS8WS1jaKYtUscbWVxrC'


# This method is done for you.
def get_twitter():
    
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.
    >>> read_screen_names('candidates4a4.txt')
    ['devinwenig', 'MichaelDell', 'JeffBezos', 'MarkZuckerbergF', 'satyanadella', 'tim_cook', 'sundarpichai', 'BillGates']
    """
    ###TODO
    file = open("candidates4a4.txt")
    line = []
    for i in file:
        line.append(str(i.rstrip('\n')))
    
    return line


def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    """
    ###TODO
    users = []
    for i in screen_names:
        request = robust_request(twitter, 'users/lookup', {'screen_name': i}, max_tries=5)
        user = [i for i in request]
        friends=[]
        request= robust_request(twitter, 'friends/ids', {'screen_name': i, 'count': 5000}, max_tries=5)
        friends = sorted([str(i) for i in request])
        req = {'screen_name': user[0]['screen_name'],
             'id': user[0]['id'],
             'friends_id': friends}
        users.append(req)
   
    return users



def get_friends(twitter, screen_name):
   
    ###TODO
    friends = []
    request = robust_request(twitter, 'friends/ids', {'screen_name': screen_name, 'count': 5000}, max_tries=5)
    friends = sorted([i for i in request])
    
    return friends


def add_all_friends(twitter, users):
    ###TODO
    for user in users:
        user['friends']=get_friends(twitter,user['screen_name'])
    





    
def outputusers(users):
    text_file = open("users.txt", "w")
    for i in sorted(users, key=lambda x: x['screen_name']):
        for j in i['friends']:
            text_file.write('%s\t%d\n' % (i['screen_name'], j))
    text_file.close()

def gettwitters(keyword):
    text_file = open("twitters.txt", "w")
    twitter = get_twitter()
    screen_name = [keyword]
    tweets = []
    for i in robust_request(twitter, 'search/tweets', {'q': screen_name, 'lang': 'en', 'count': 100}):
        tweets.append(i)
    for i in range(len(tweets)):
        text_file.write('%s\n' % str(tweets[i]['text']))
    text_file.close()


    


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates4a4.txt')
    print('Established connection successfully!')
    print('screen names:\n%s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    add_all_friends(twitter, users)
    
    outputusers(users)
    gettwitters('iPhone X')
    
    


if __name__ == '__main__':
    main()
    
