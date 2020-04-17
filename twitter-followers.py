import twitter
import pickle

from keys import *

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

api.VerifyCredentials()

def get_usernames(twitter_users):
    return [x.screen_name for x in twitter_users]

def update_data(followers, friends):
    data = {'friends': friends, 'followers': followers}
    pickle.dump( data, open( "save.p", "wb" ) )
    return True

state_complete = False
while not state_complete:
    followers_list = api.GetFollowers()
    friends_list = api.GetFriends()

    try: 
        data = pickle.load( open( "save.p", "rb" ) )
        print("Loaded previous data")

        friends, followers = get_usernames(friends_list), get_usernames(followers_list)
        new_followers = set(data['friends']) - set(friends)
        new_friends = set(data['followers']) - set(followers)

        old_followers = set(friends) - set(data['friends']) 
        old_friends = set(followers) - set(data['followers'])

        print("New Followers: ", ", ".join(new_followers), "\n")
        print("New Friends: ", ", ".join(new_friends), "\n")

        print("Unfollowed Friends: ", ", ".join(old_friends), "\n")
        print("Unfollowers: ", ", ".join(old_friends), "\n")

        ans = input("Would you like to save this as your new reference point? y/n: ")
        if ans.lower() == 'y':
            update_data(followers, friends)
        
        ans = input("Do you wish to continue? y/n: ")
        if ans.lower() == 'n':
            break
        else:
            continue

    except: #file not found
        ans = input("No prior data found, would you like to create a new reference point? y/n: ")
        if ans.lower() == 'y':

            friends, followers = get_usernames(friends_list), get_usernames(followers_list)
            update_data(followers, friends)
            print("Updated Successfully")
            
            ans = input("Do you wish to continue? y/n: ")
            if ans.lower() == 'n':
                break
            else:
                continue
        else:
            ans = input("Do you wish to continue? y/n: ")
            if ans.lower() == 'n':
                break
            else:
                continue