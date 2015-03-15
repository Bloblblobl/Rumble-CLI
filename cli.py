"""
Command Line Interface for Rumble-Server
If you provide a username and password, it will log you into the server
If you provide a handle as well, it will register you to the server instead
"""
import argparse

def options():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--handle')

    return parser.parse_args()

def main():
    o = options()
    print o.user
    print o.password
    print o.handle

if __name__ == '__main__':
    main()