"""
Command Line Interface for Rumble-Server
If you provide a username and password, it will log you into the server
If you provide a handle as well, it will register you to the server instead
"""
import argparse
import json
import time
import os
import sys
from datetime import datetime, timedelta
from rumble_client.client import Client




def options():
    # --user a --password a --server-url http://localhost:5555
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--server-url', default='http://rumble.pythonanywhere.com')
    parser.add_argument('--handle')

    return parser.parse_args()

def startup():
    if os.path.isfile('config.json'):
        config = open('config.json').read()
        config = json.loads(config)
        return config['user'], config['password'], config['handle'], config['server_url']

    print 'Rumble-CLI'
    user = raw_input('Username: ')
    password = raw_input('Password: ')
    handle = raw_input('Handle: ')
    server_url = raw_input('Server URL: ')

    s = json.dumps(dict(user=user, password=password, handle=handle, server_url=server_url))
    open('config.json', 'w').write(s)

    return user, password, handle, server_url


def main(username, password, handle, server_url):
    client = Client(server_url)
    commands = {'q': sys.exit,
                'help': help,
                'register': client.register,
                'login': client.login,
                'join': client.join_room,
                'gtrms': client.get_rooms,
                'gtmmbrs': client.get_room_members,
                'create': client.create_room}
    if handle:
        client.register(username, password, handle)
    user = client.login(username, password)

    #select room
    print client.get_rooms()
    room = 'room0'
    time = datetime.utcnow().replace(microsecond=0)
    start = time - timedelta(days=1)
    end = time + timedelta(days=1)
    print client.join_room(room)

    while True:
        print '==============LINE=BREAK=============='
        user_input = raw_input('> ')
        parse_input(user_input, client, room, commands)
        messages = client.get_messages(room, start, end)
        os.system('cls')
        for m in messages["result"]:
            print "[{}:{}] {}".format(m[1], m[0], m[2])

def parse_input(input, client, room, commands):
    # check to see if input is command
    if input.startswith('!'):
        args = input[1:].split(' ')
        command = args[0]
        args = args[1:]
        commands[command](*args)
    # if not treat it as a message, send the message
    else:
        print client.send_message(room, input)

def help():
    help_file = open('README.md')
    for line in help_file:
        print(line)
    raw_input('PRESS ANY KEY TO CONTINUE')

if __name__ == '__main__':
    user, password, handle, server_url = startup()
    main(user, password, handle, server_url)