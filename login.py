import constants
import oauth2
import urllib.parse as urlparse
import json

#create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to indentify our app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

#use client to perform a request for the request token
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
if response.status != 200:
    print("An error occurred getting the request token from Twitter!")

#get the request token parsing a query string returned
resquest_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

#aks the user to authorize the our app and give us the pin code
print("Go to the following site in your browser: ")
print(f"{constants.AUTHORIZATION_URL}?oauth_token={resquest_token['oauth_token']}")

oauth_verifier = input("Whats the PIN? ")

#create a Token object which contains the request token, and the verifier
token = oauth2.Token(resquest_token['oauth_token'], resquest_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)

#create a client with our consumer  (our app) and the newly created (and verified) token
client = oauth2.Client(consumer, token)

#ask twitter for an access token, and Twitter knows it should give us it because we've verified
#the request token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)

#create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

#make twitter API calls
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=computers+filter:images', 'GET')
if response.status != 200:
    print("An error occurred when searching")

tweets = json.loads((content.decode('utf-8')))

for tweet in tweets['statuses']:
    print(tweet['text'])
