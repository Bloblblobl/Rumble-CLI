"""
Command Line Interface for Rumble-Server
If you provide a username and password, it will log you into the server
If you provide a handle as well, it will register you to the server instead
"""
import argparse
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
    while True:
        user_input = raw_input('> ')
        print user_input



if __name__ == '__main__':
    main()