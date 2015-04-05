"""
Command Line Interface for Rumble-Server
If you provide a username and password, it will log you into the server
If you provide a handle as well, it will register you to the server instead
"""
import argparse
import time
import os
from datetime import datetime, timedelta
from rumble_client.client import Client

def options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--server-url', default='http://rumble.pythonanywhere.com')
    parser.add_argument('--handle')

    return parser.parse_args()

def main():
    o = options()
    print o.user
    print o.password
    print o.handle
    client = Client(o.server_url)
    if o.handle is not None:
        client.register(o.user, o.password, o.handle)
    user = client.login(o.user, o.password)

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
        parse_input(user_input, client, room)
        # clear the screen
        messages = client.get_messages(room, start, end)
        for m in messages["result"]:
            print "[{}:{}] {}".format(m[1], m[0], m[2])

def parse_input(input, client, room):
    # check to see if input is command
    if input.startswith('!'):
        return
    # if not treat it as a message, send the message
    print client.send_message(room, input)


if __name__ == '__main__':
    main()