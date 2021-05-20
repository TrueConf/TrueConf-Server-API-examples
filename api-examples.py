# =================================
# Examples to start work with TrueConf Server API
# 
# API documentation: https://developers.trueconf.com/api/server/
# 
# To use this examples, you need to:
# 1. Install Python 3.7+: https://www.python.org/downloads/
# 2. Upgrade pip (if needed): https://pip.pypa.io/en/stable/installing/
# 3. Install required packeges via pip:
#    >> pip install requests pyexcel pyexcel-xls pyexcel-xlsx
# 
# WARNING!
# Default value for the "verify" parameter in the data.json file is True
# If you are using a self-signed certificate, you may need to set this value to path to your ca.crt file
# For example: "verify":"C:/Program Files/TrueConf Server/httpconf/ssl/ca.crt"
# more info: https://stackoverflow.com/questions/30405867/how-to-get-python-requests-to-trust-a-self-signed-ssl-certificate
# =================================

import requests
import sys
import time
import os
from requests.exceptions import HTTPError
from datetime import datetime
import pyexcel
import json

# some params used in the program
API_PARAMS = {
		"server":"",
		"client_id":"",
		"client_secret":"",
		"access_token":"",
		"new_users_file":"",
		"verify": True
	}

# some answers types
REQUEST_RESULT = {
	"success": 0,
	"error_dublicate": 1,
	"error_not_found": 2,
	"other_error": 3
}

SERVER_DATA_FILE = "data.json"

GROUPS_COLUMN = "groups"

AVATAR_COLUMN = "avatar"

APP_STRINGS = {
	"invalid_selection": "Select the correct task\n",
	"incorrect_value": "Select the correct value (y or n)!",
	"success_read_server_data": F"Data from '{SERVER_DATA_FILE}' was successfully read.",
	"error_read_server_data": F"ERROR! Can't read data from '{SERVER_DATA_FILE}'.",
	"use_secret_key": "Use the server secret key (y - yes, n - no)?",
	"use_tags":"Use tags to filter conferences (y - yes, n - no)?",
	"enter_ip": "Enter the TrueConf Server IP address or FQDN:",
	"enter_tag": "Enter the tag:",
	"enter_app_secret": "Enter the OAuth Secret key:",
	"enter_app_id": "Enter OAuth Application ID:",
	"enter_secret_key": "Enter the server secret key:",
	"use_server_data_file": F"Read data from a file '{SERVER_DATA_FILE}' (y - yes, n - no)?",
	"use_excel_file": "Do you want to enter the correct Excel file path manually (y - yes, n - no)?",
	"enter_excel_file_path": "Enter the file path:",
	"error_read_users_file": "Error! Failed to read users data.",
	"server":"Server: ",
	"error_http":"HTTP error: ",
	"error_api":"API error: ",
	"error_get_token":"ERROR: failed to receive access token! Please try again.",
	"error":"Error: ",
	"token":"Your access token is ",
	"conferences_deleted":"conferences were deleted",
	"days_count":"Enter the number of days above which you want to delete ended scheduled conferences:",
	"start_task":"=== Task is in progress ===",
	"added":"was added",
	"deleted":"was deleted",
	"edited":"was successfully edited",
	"users_added":" server users were added",
	"users_deleted":" server users were deleted",
	"quit_message":"Thank you for using TrueConf solutions!",
	"error_dublicate": "Data already exists on the server\n======",
	"error_not_found": "Object not found\n======",
	"adding_users": "=== Start adding users ===",
	"adding_user": "Adding user ",
	"adding_groups": "=== Start edding groups ===",
	"adding_user_to_group": "Adding user to the group ",
	"adding_group": "Adding group ",
	"groups_deleted":"groups were deleted",
	"groups_added":"groups were added",
	"deleting_group": "Deleting group",
	"deleting_user": "Deleting user",
	"user_added_to_group": "was added to groups",
	"file_not_found": "File not found: ",
	"no_users": "The list of users is empty",
	"no_groups": "The list of groups is empty"
}

# ================
# menu functions
# ================
def exec_menu(selected_item):
	if selected_item == '':
		menu_actions['main_menu']()
	else:
		try:
			menu_actions[selected_item]()
		except KeyError:
			print(APP_STRINGS['invalid_selection'])
			menu_actions['main_menu']()
	return

def quit():
	print(APP_STRINGS['quit_message'])
	time.sleep(1.5)
	sys.exit(0)

def get_yes_no():
	correct_value = False
	while not correct_value:
		answer = input(">> ").lower()
		if answer == "y":
			return True
		elif answer == "n":
			return False
		else:
			print(APP_STRINGS['incorrect_value'])

def read_server_data_from_file():
	API_PARAMS["access_token"] = ""
	try:
		with open(SERVER_DATA_FILE) as data_file:
			data = json.load(data_file)
			for key, value in data.items():
				API_PARAMS[key] = value

		API_PARAMS["server"] = check_https(API_PARAMS["server"])
		print(APP_STRINGS['success_read_server_data'] + ' ' + APP_STRINGS['server'] + API_PARAMS['server'])
		return True
	except:
		print(APP_STRINGS['error_read_server_data'])
		return False

def main_menu():
	print("==========================\nSelect the task:")
	print("S - read the server data (address, OAuth access token or Application ID and Secret key)")
	print("E - delete old ended scheduled conferences")
	print(F"N - add server users from Excel file")
	print(F"D - delete server users listed in Excel file")
	print("Q - quit")

	selected_item = input(">> ").lower()
	# print(F"=====\nselected={selected_item}")

	exec_menu(selected_item)
# ================
# end of menu functions
# ================


# ================
# Helper functions
# ================

def init_api_params(page_size, timeouts):
	API_PARAMS['page_size'] = page_size
	API_PARAMS['timeouts'] = timeouts

# simple check server url, so you can type IP or FQDN with or without https prefix
def check_https(url):
	if url.startswith("https://"):
		return url
	elif url.startswith("http://"):
		return url.replace("http://", "https://")
	else:
		return "https://" + url

def get_data_manually():
	print(APP_STRINGS['enter_ip'])
	API_PARAMS['server'] = check_https(input(">> "))

	print(APP_STRINGS['enter_app_id'])
	client_id = input(">> ")
	print(APP_STRINGS['enter_app_secret'])
	client_secret = input(">> ")
	return get_token()

# Get the TrueConf server address, client ID and client secret for your OAuth app. 
# If you know the server secret key, you may use it
# More info https://docs.trueconf.com/server/admin/web-config#web-security
def get_server_data():
	print(APP_STRINGS['use_server_data_file'])
	try_manual = False
	answer = get_yes_no()
	if answer:
		API_PARAMS['verify'] = True

		if read_server_data_from_file():
			if API_PARAMS["access_token"] == "":
				result = get_token()
				if result == False:
					# print(APP_STRINGS['error_read_server_data'])
					try_manual = True
		else:
			try_manual = True
	else:
		try_manual = True

	if try_manual:
		if not get_data_manually():
			print(APP_STRINGS['error_get_token'])

	main_menu()

def get_file_manually():
	print(APP_STRINGS['use_excel_file'])
	answer = get_yes_no()
	if answer:
		print(APP_STRINGS['enter_excel_file_path'])
		API_PARAMS["new_users_file"] = input(">> ")

def read_new_users_groups():
	users = list()
	groups = set()
	if os.path.exists(API_PARAMS['new_users_file']):
		try:
			users = pyexcel.get_records(file_name=API_PARAMS['new_users_file'])
			for user in users:
				for key, value in user.items():
					user[key] = str(value)
				if 'display_name' not in user:
					user['display_name'] = user['first_name'] + ' ' + user['last_name']

			if len(users) > 0 and GROUPS_COLUMN in users[0]:
				for user in users:
					groups.update(user[GROUPS_COLUMN].split(','))
			return users, groups, True
		except:
			print(APP_STRINGS['error_read_users_file'])
			return users, groups, False
	else:
		print(APP_STRINGS['file_not_found'] + "'" + API_PARAMS['new_users_file'] + "'")
		return users, groups, False

# ================
# end of helper functions
# ================


# ================
# TrueConf API functions
# ================

def get_token():
	access_token = get_access_token(API_PARAMS["client_id"], API_PARAMS["client_secret"])
	if not access_token:
		return False
	API_PARAMS['access_token'] = access_token
	print(APP_STRINGS['token'] + API_PARAMS['access_token'])
	return True

def exec_request(url, request_type, body_encoding = "json", body_content = "", files = ""):
	try:
		if(request_type == "GET"):
			response = requests.request(request_type, url, timeout=API_PARAMS['timeouts'], verify=API_PARAMS['verify'])
		else:
			if files:
				headers = ""
			else:
				headers = {
				'Content-Type': "application/" + body_encoding
				}
			response = requests.request(request_type, url, headers=headers, data=body_content, files = files, timeout=API_PARAMS['timeouts'], verify=API_PARAMS['verify'])
		response.raise_for_status()
	except HTTPError as http_err:
		response_obj = response.json()
		# custom message for dublicates
		if response_obj['error']['errors'][0]['reason'] == 'uniqueValueAlreadyInUse':
			print(APP_STRINGS['error_dublicate'])
			return REQUEST_RESULT['error_dublicate'], {}
		# custom message for the "not found" API error
		elif response_obj['error']['message'] == 'Not Found':
			print(APP_STRINGS['error_not_found'])
			return REQUEST_RESULT['error_not_found'], {}
		else:
			print(F"{APP_STRINGS['error_http']}{http_err}")
			print(F"{APP_STRINGS['error_api']}{response_obj['error']['errors'][0]['message']}")
			return REQUEST_RESULT['other_error'], {}
	except Exception as err:
		print(F"{APP_STRINGS['error']}{err}.")
		return REQUEST_RESULT['other_error'], {}
	else:
		return REQUEST_RESULT['success'], response.json()

def get_access_token(client_id, client_secret):
	url = API_PARAMS['server'] + "/oauth2/v1/token"
	data = json.dumps(dict({"grant_type":"client_credentials","client_id":client_id,"client_secret":client_secret}))
	result, json_data = exec_request(url, "POST", "json", data)
	if result == REQUEST_RESULT["success"]:
		return json_data["access_token"]
	else:
		return False

def get_conferences_list(conferences_count, **options):
	conferences = []
	url = F"{API_PARAMS['server']}/api/v3.3/conferences?access_token={API_PARAMS['access_token']}"
	for option, value in options.items():
		url += F"&{option}={value}"
	result, json_data = exec_request(url, "GET")

	if result == REQUEST_RESULT["success"]:
		conferences = json_data["conferences"]
		if conferences_count == 0:
			conferences_count = json_data["cnt"]
		if conferences_count > API_PARAMS['page_size']:
			conferences_count = conferences_count - API_PARAMS['page_size']
			options["page_id"] = options["page_id"] + 1
			conferences = conferences + get_conferences_list(conferences_count, **options)

	return conferences

def delete_conference(id):
	url = F"{API_PARAMS['server']}/api/v3.3/conferences/{id}?access_token={API_PARAMS['access_token']}"
	result, json_data = exec_request(url, "DELETE")
	return result == REQUEST_RESULT["success"]

# specify tag if you want to delete only conferences with this tag
def delete_conferences(timestamp_to_delete, tag = ""):
	conferences = get_conferences_list(0, page_size=API_PARAMS['page_size'], tag=tag, state='stopped', page_id=1)
	if not conferences:
		return False

	result = True
	index = 0
	print(APP_STRINGS['start_task'])
	for conference in conferences:
		schedule = conference['schedule']
		if schedule['type'] == 1:
			end_time = schedule['start_time'] + schedule['duration']
			if end_time < timestamp_to_delete:
				new_result =  bool(delete_conference(conference['id']))
				result = result and new_result
				if new_result:
					index += 1
					print(F"Conference ID = {conference['id']} deleted, start_time = {datetime.fromtimestamp(schedule['start_time'])}, end_time = {datetime.fromtimestamp(end_time)}")
	print(F"{index} {APP_STRINGS['conferences_deleted']}")
	return result

def delete_old_conferences():
	print(APP_STRINGS['days_count'])
	correct_value = False

	while not correct_value:
		answer = input(">> ").lower()
		try:
			# number of days to remove a conference, how many days have passed since the end date
			days_to_delete = float(answer)

			# we need to convert current time to Unix timestamp, more info: https://www.unixtimestamp.com/
			timestamp_to_delete = datetime.timestamp(datetime.now()) - int(days_to_delete * 24 * 60 * 60)
			correct_value = True
		except ValueError:
			print(APP_STRINGS['incorrect_value'])

	print(APP_STRINGS['use_tags'])
	result = True

	answer = get_yes_no()
	if answer == True:
		print(APP_STRINGS['enter_tag'])
		tag = input(">> ")
		result = delete_conferences(timestamp_to_delete, tag)
	else:
		result = delete_conferences(timestamp_to_delete)

	main_menu()

def add_user(user):
	url = F"{API_PARAMS['server']}/api/v3.3/users?access_token={API_PARAMS['access_token']}"

	data = json.dumps(user)

	result, json_data = exec_request(url, "POST", "json", data)
	# try to edit user data if user already exists
	if result == REQUEST_RESULT["error_dublicate"]:
		result, json_data = edit_user(user)
		if result == REQUEST_RESULT["success"]:
			print(F"{user['login_name']} {APP_STRINGS['edited']}")
	elif result == REQUEST_RESULT["success"]:
		print(F"{user['login_name']} {APP_STRINGS['added']}")

def add_avatar(user_id, file_path):
	try:
		url = F"{API_PARAMS['server']}/api/v3.3/users/{user_id}/avatar?access_token={API_PARAMS['access_token']}"
		file_name = file_path.split('/')[-1]
		file_ext = file_path.split('.')[-1]
		files=[('image',(file_name,open(file_path,'rb'),'image/' + file_ext))]
		result, json_data = exec_request(url, "POST", "multipart/form-data", "", files)
		return result == REQUEST_RESULT["success"]
	except FileNotFoundError:
		print(F"{APP_STRINGS['file_not_found']} {file_path}")
		return False

def edit_user(user):
	url = F"{API_PARAMS['server']}/api/v3.3/users/{user['login_name']}?access_token={API_PARAMS['access_token']}"

	data = json.dumps(user)

	return exec_request(url, "PUT", "json", data)

def delete_user(user_id):
	url = F"{API_PARAMS['server']}/api/v3.3/users/{user_id}?access_token={API_PARAMS['access_token']}"

	result, json_data = exec_request(url, "DELETE")
	return result == REQUEST_RESULT["success"]

def delete_group(group_id):
	url = F"{API_PARAMS['server']}/api/v3.3/groups/{group_id}?access_token={API_PARAMS['access_token']}"

	result, json_data = exec_request(url, "DELETE")
	return result == REQUEST_RESULT["success"]

def add_group(group):
	url = F"{API_PARAMS['server']}/api/v3.3/groups?access_token={API_PARAMS['access_token']}"

	data = json.dumps(group)

	result, json_data = exec_request(url, "POST", "json", data)
	return result == REQUEST_RESULT["success"]

def add_groups(groups):
	print(APP_STRINGS['adding_groups'])
	count = 0
	for group in groups:
		group_name = group['display_name']
		if group_name.strip():
			print(F"{APP_STRINGS['adding_group']}{group_name}")
			if add_group(group):
				print(F"{group_name} {APP_STRINGS['added']}")
				count += 1
	print(F"=== {count} {APP_STRINGS['groups_added']} ===\n")

def add_user_to_group(user_name, group_id):
	url = F"{API_PARAMS['server']}/api/v3.3/groups/{group_id}/users?access_token={API_PARAMS['access_token']}"

	data = json.dumps({"user_id": user_name})

	result, json_data = exec_request(url, "POST", "json", data)
	return result == REQUEST_RESULT["success"]

def get_server_groups(**options):
	groups = []
	url = F"{API_PARAMS['server']}/api/v3.3/groups?access_token={API_PARAMS['access_token']}"
	for option, value in options.items():
		url += F"&{option}={value}"
	# print(F"url = {url}")
	result, json_data = exec_request(url, "GET")
	if result == REQUEST_RESULT["success"]:
		# check the next page id and continue for the next page if needed (next_page_id > 0)
		next_page_id = json_data["next_page_id"]

		groups = json_data["groups"]

		if next_page_id > 0:
			options["page_id"] = next_page_id
			groups = groups + get_server_groups(**options)

	return groups

def add_user_to_groups(user, groups, groups_list):
	added_groups = ""

	# if user is admin add to all groups from the list
	if not('is_admin' in user and user['is_admin']):
		groups = user[GROUPS_COLUMN].split(',')
	# print(groups)
	for group_name in groups:
		# print(group)

		# get group id by name
		if group_name:
			for group in groups_list:
				if group['display_name'] == group_name:
					group_id = group['id']
					print(F"{APP_STRINGS['adding_user_to_group']}{group_name}")
					if add_user_to_group(user['login_name'], group_id):
						added_groups = added_groups + group_name + ', '
					break
	# print("added_groups: '" + added_groups + "'")
	return added_groups[:-2]

def add_users():
	users, groups, result = read_new_users_groups()
	if not result:
		get_file_manually()
		main_menu()
		return

	no_users = not users or len(users) == 0
	no_groups = not groups or len(groups) == 0

	if no_users:
		print(APP_STRINGS['no_users'])
	if no_groups:
		print(APP_STRINGS['no_groups'])
	if not no_groups and not no_users:
		groups_list = [dict(display_name = group) for group in groups]

		if not no_groups:
			add_groups(groups_list)
			groups_list = get_server_groups()

		print(APP_STRINGS['adding_users'])
		count = 0
		for user in users:
			print(F"{APP_STRINGS['adding_user']}{user['login_name']}")
			if add_user(user):
				count += 1

			if AVATAR_COLUMN in user and user[AVATAR_COLUMN]:
				add_avatar(user['login_name'], user[AVATAR_COLUMN])

			if not no_groups:
				user_groups = add_user_to_groups(user, groups, groups_list)
				if user_groups:
					print(F"{user['login_name']} {APP_STRINGS['user_added_to_group']} {user_groups}\n=======")

		print(F"=== {count} {APP_STRINGS['users_added']} ===\n")

	main_menu()

def delete_users(users):
	print(APP_STRINGS['start_task'])
	count = 0
	for user in users:
		print(F"{APP_STRINGS['deleting_user']} {user['login_name']}")
		if delete_user(user['login_name']):
			print(F"{user['login_name']} {APP_STRINGS['deleted']}")
			count += 1
	print(F"=== {count} {APP_STRINGS['users_deleted']} ===\n")

def delete_groups(groups):
	print(APP_STRINGS['start_task'])
	groups_list = get_server_groups()

	count = 0
	for group_name in groups:
		# print(group)

		# get group id by name
		if group_name:
			for group in groups_list:
				if group['display_name'] == group_name:
					group_id = group['id']
					print(F"{APP_STRINGS['deleting_group']} {group_name}")
					if delete_group(group_id):
						print(F"group_name {APP_STRINGS['deleted']}")
						count += 1
					break
	print(F"=== {count} {APP_STRINGS['groups_deleted']} ===\n")
	main_menu()

def delete_users_groups():
	users, groups, result = read_new_users_groups()
	if not result:
		get_file_manually()
		main_menu()
		return

	if not users or len(users) == 0:
		print(APP_STRINGS['no_users'])
		main_menu()
		return

	delete_users(users)

	if not groups or len(groups) == 0:
		print(APP_STRINGS['no_groups'])
		main_menu()
		return

	delete_groups(groups)
	main_menu()

# ================
# End of API functions
# ================

# Menu definition
menu_actions = {
	'main_menu': main_menu,
	's': get_server_data,
	'e': delete_old_conferences,
	'n': add_users,
	'd': delete_users_groups,
	'q': quit
}

if __name__ == "__main__":

	# the first element is a connect timeout (the time it allows for the client to establish a connection to the server);
	# the second is a read timeout (the time it will wait on a response once your client has established a connection) 
	timeouts = (3, 5)

	# custom page size to receive the conferences list
	page_size = 100

	init_api_params(page_size, timeouts)

	main_menu()