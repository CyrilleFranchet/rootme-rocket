#!/usr/bin/env python
# coding : utf-8
from __future__ import print_function
import requests
import json
import sys

rocket_api_user = ''
rocket_api_token = ''
rocket_channel = ''
rocket_avatar = ''
rocket_host = 'https://'
rocket_api_channels_list = '/api/v1/channels.list'
rocket_api_chat_postmessage = '/api/v1/chat.postMessage'
rootme_halloffame = ''

def main():
    dict_old_json = {}
    dict_new_json = {}
    
    # Load the actual file
    with open('users.json', 'r') as f:
        dict_old_json = json.load(f)

    # We need to download the JSON file
    r = requests.get(rootme_halloffame)
    if r.status_code == 200:
        if r.text:
            with open('users.json', 'w') as f:
                f.write(r.text)
            dict_new_json = r.json()
    
    if not dict_old_json or not dict_new_json:
        sys.exit(1)

    dict_scoring = {}

    # Parse the new user
    for user in dict_new_json['users']:
        username_r = user['username_r']
        username = user['username']
        points = int(user['points'])

        for u in dict_old_json['users']:
            if username == u['username'] and points > int(u['points']):
                dict_scoring[username_r] = points-int(u['points'])

    if dict_scoring:
        # We need to list the channels from Rocket
        url = rocket_host + rocket_api_channels_list
        headers = {'X-Auth-Token': rocket_api_token, 'X-User-Id': rocket_api_user}

        r = requests.get(url,headers=headers)
        
        channel_id = None
        for channel in r.json()['channels']:
            if channel['name'] == rocket_channel:
                channel_id = channel['_id']
        
        if channel_id:
            # We can post messages to the channel
            url = rocket_host + rocket_api_chat_postmessage
            for user in dict_scoring:
                data = {}
                data['roomId'] = channel_id
                data['channel'] = '#' + rocket_channel
                data['text'] = 'Well done ' + user + '. You won ' + str(dict_scoring[user]) + ' points.'
                data['alias'] = 'Root-Me'
                data['avatar'] = rocket_avatar
                
                r = requests.post(url, headers=headers, data=data)

if  __name__ == "__main__":
    main()
