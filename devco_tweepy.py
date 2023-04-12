#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

#Credentials to access Twitter API 
access_token = "971748248179404800-WC10QDiDO8NbZsZ3tvZFnygCeGTO92T"
access_token_secret = "1bIewSjjiHQnU6dJDmAVH5jmNbzrUEaAL8TfNrPlB1h67"
consumer_key = "xDAwEvTTD9PyEyuiOQEGiVhsi"
consumer_secret = "7SuT2lrxWxg1KgWjwweNU1CMAdTkCmC8xaF4X4z4tGCbmI4DUa"

#Google Sheet Credentials
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#Open Sheet
sheet = client.open("data store").sheet1

#Listener with Filter
class StdOutListener(StreamListener):

	def on_data(self, data):
		#Load JSON and retrieve some variables
		try:
			all_data	=	json.loads(data)
			username = str(all_data["user"]["screen_name"])
			desc = str(all_data["user"]["description"])
			followers_count = all_data["user"]["followers_count"]
		except:
			print("Could not load streaming data into JSON effectively. UnicodeError. ")
		try:
			row = [username, desc, followers_count]
			sheet.append_row(row)
		except:
			print("Could not insert into GSheets!")
		#String Concatenation for console display (Can be improved for special characters like Japanese and Chinese letters)
		try:
			twit_username = "Username: " + str(username)
			twit_bio = "Description: " + str(desc)
			twit_follow = "Number of Followers: " + str(followers_count)
		except:
			print("Could not format result string.")
		
		#Print Results
		try:
			print(twit_username)
			print(twit_bio)
			print(twit_follow)
			print("---------------------------------------------------")
		except:
			print("Could not print to screen 1.")
		return True

	def on_error(self, status):
		try:
			print(status)
		except:
			print("Could not print to screen 2.")
		
if __name__ == '__main__': 
	try:
		hashtag_input = input("Please provide the hashtags separated with a comma and no spaces: ").split(",")
		print(hashtag_input)
		l = StdOutListener()
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
	except:
		print("App Could not authenticate")
	try:
		stream = Stream(auth, l)
		stream.filter(track=hashtag_input)
	except:
		print("Stream Aborted!")