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

def run():
    state_complete = False
    while not state_complete:
        followers_list = api.GetFollowers()
        friends_list = api.GetFriends()

        try: 
            data = pickle.load( open( "save.p", "rb" ) )
            print("Loaded previous data")

            friends, followers = get_usernames(friends_list), get_usernames(followers_list)
            unfollowed = set(data['friends']) - set(friends)
            un_followers = set(data['followers']) - set(followers)

            new_following = set(friends) - set(data['friends']) 
            new_followers = set(followers) - set(data['followers'])

            print("New Following: ", ", ".join(new_following), "\n")
            print("New Followers: ", ", ".join(new_followers), "\n")

            print("Unfollowers: ", ", ".join(un_followers), "\n")
            print("Un Followed: ", ", ".join(unfollowed), "\n")

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

if __name__ == "__main__":
    run()