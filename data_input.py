import json
import re
from os import path
from getpass import getpass


def add_credentials():
    if path.exists('credentials.json'):
        print('Change credentials for MS Teams:')
    else:
        print('Input credentials for MS Teams:\n')
    email = input('Email: ')
    passwd = getpass('Password: ')
    cred = {'email': email,
            'passwd': passwd}
    with open('credentials.json', 'w') as out_file:
        json.dump(cred, out_file)


def add_timetable():
    if path.exists('timetable.json'):
        print('Change timetable:')
        mode = input('Choose (a) for add event, (r) renew. (a/r):').casefold()
        if mode == 'a':
            with open('timetable.json') as in_file:
                timetable = json.load(in_file)
            print('Input new events in the format: {day_of_week} {class_name} {start_time} {end_time}')
            print('e.g. Monday Math 12:40 14:05')
            print('\nWARNING: Input is CASE SENSITIVE!')
    pass


def add_names():
    team_names = {}
    if path.exists('timetable.json'):
        with open('timetable.json') as in_file:
            data = json.load(in_file)
        classes = set([d['class'] for d in data])
        for c in classes:
            print('Input corresponding team names:\nWARNING: Input is CASE SENSITIVE!')
            team_names[c] = input(f'{c} -> ')
        print(f'Team names updated.')
        with open('team_names.json', 'w') as out_file:
            json.dump(team_names, out_file)
    else:
        print('Timetable not found!\nCannot input team names. Please input timetable.')