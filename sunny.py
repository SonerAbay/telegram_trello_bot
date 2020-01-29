import re
import sqlite3
from playhouse.sqlite_ext import SqliteExtDatabase
import random
import json
from datetime import datetime

# logs the requests
def log_request(item):
	with open('requests.log', 'a') as f:
		f.write(str(item)+"\n\n")
	
def group_split(str):
	command = str.split()[0]
	text = " ".join(str.split()[1:])
	return (text, command)

def find_line(text):

	regex = re.compile("^[A-Za-z0-9 ]*$")
	text = "".join(filter(regex.search, text))

	if len(text) > 50 or len(text) < 2 or '  ' in text:
		return "Enter a normal line, you jabroni!!\nYou are being intervened for illiteracy:\nhttps://i.hizliresim.com/nb8NmM.gif"
	else:
		conn = None
		try:
			conn = sqlite3.connect("../db/subtitles.db")
		except sqlite3.Error as e:
			print(e)

		cur = conn.cursor()
		sql = "SELECT * from episode inner join lines on episode.episode_id = lines.episode_id WHERE text MATCH '{}' ORDER BY rank".format(text)
		cur.execute(sql)

		result = cur.fetchall()

		if len(result) == 0:
			return "Ooooh no I failed, I failed you. I couldn't find anything. Alright get me good, 3 lashes.\nhttp://pngimg.com/uploads/whip/whip_PNG24.png"
		else:
			print("here")
			minute = str(result[0][7]/60)
			sec = str(result[0][7]%60)
			if len(minute) == 1:
				minute = '0' + minute
			if len(sec) == 1:
				sec = '0' + sec
			time = minute+':'+sec
			return "\n''<i>{}</i>'' <b>@ {}</b>\n\n<b>Season {}, Episode {} - {}.</b>\n\nYou can watch it at:\n{}".format(result[0][6],time, result[0][1],result[0][3],result[0][2],result[0][4])

def list_episodes(text):
	if not text.isdigit() and int(text) < 1 or int(text) > 14:
		return "Enter a valid season number, you jabroni!\n Usage: /episodes SEASON-NUMBER"
	else:
		conn = None
		try:
			conn = sqlite3.connect("../db/subtitles.db")
		except sqlite3.Error as e:
			print(e)
		
		cur = conn.cursor()
		sql = "SELECT episode_number, episode_name FROM episode WHERE episode_season = {}".format(text)
		cur.execute(sql)

		result = cur.fetchall()

		if len(result) == 0:
			return "Enter a valid season number, you jabroni!\n Usage: /episodes SEASON-NUMBER"
		else:
			episode_list = ["%s - %s" % tuple for tuple in result]
			episode_list = '\n'.join(episode_list)
			return "<b>Season {} Episode List:</b>\n\n{}".format(text, episode_list)
		

def random_episode():
	
	episode = random.randint(1,153)
	conn = None
	try:
		conn = sqlite3.connect("../db/subtitles.db")
	except sqlite3.Error as e:
		print(e)
	
	cur = conn.cursor()
	sql = "SELECT episode_number, episode_name, episode_season, sezonluk_url FROM episode WHERE episode_id = {}".format(episode)
	cur.execute(sql)

	result = cur.fetchall()

	return "<b>Here is a random episode for you:</b>\n\nSeason {} x {} - {}\n\nYou can watch it at:\n{}".format(result[0][2],result[0][0],result[0][1], result[0][3])

def trivia():
	
	trivia = random.randint(1,60)
	conn = None
	try:
		conn = sqlite3.connect("../db/subtitles.db")
	except sqlite3.Error as e:
		print(e)

	cur = conn.cursor()
	sql = "SELECT text FROM trivia WHERE id = {}".format(trivia)

	cur.execute(sql)

	result = cur.fetchall()

	return "<b>Did you know?</b>\n\n" + result[0][0]

def help():

	return "<b>Command List:</b>\n\n<b>/line</b> - Enter a line from the show to find the episode.\n<b>Usage:</b>/line your line\n\n<b>/episodes</b> - Get the list of episodes from a season.\n<b>Usage:</b> /episodes season_number\n\n<b>/random</b> - Get a random episode from the show.\n<b>Usage:</b> /random\n\n<b>/trivia</b> Returns a trivia about the show.\n<b>Usage:</b> /trivia"

def text(input_text, item):
	print(item)
	if input_text.startswith("/"):
		log_request(item)
	text, command = group_split(input_text)
	if command == '/line':
		log_request(item)
		return find_line(text)
	if command == '/episodes':
		return list_episodes(text)
	if command == '/random':
		return random_episode()
	if command == '/sunny_help':
		return help()
	if command == '/trivia':
		return trivia()
		
