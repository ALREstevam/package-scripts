#!/usr/bin/python3

from collections import OrderedDict
from json import JSONDecoder
from colorama import Fore, Back, Style
import os
import json
import sys
import inquirer
import subprocess
from inquirer.themes import GreenPassion
import pyperclip
from colorama import init
init()

customdecoder = JSONDecoder(object_pairs_hook=OrderedDict)

path = os.getcwd()
file_path = path + '/package.json'
code_path = os.path.dirname(sys.argv[0])

base_run_command = 'yarn'

with open(code_path + '/config.json') as file:
    configs = json.load(file)
    base_run_command = ' '.join(
        [configs['packageManager'], configs['runCommand']]).strip()


if os.path.isfile(file_path):
    questions = []
    scripts = []
    commands = []

    with open(file_path) as file:
        data = json.loads(file.read())

        if "-r" not in sys.argv and "--raw" not in sys.argv:
            print(f'{Style.BRIGHT}{Back.WHITE}{Fore.BLUE}')
            print('\t' * 2, end='')
            title = f' {data["name"]} '
            print(f'{title:^50s}', end='')
            print(f'{Style.RESET_ALL}')
            print('\n')

        for i, (script, command) in enumerate(data['scripts'].items(), 1):
            scripts.append(script)
            commands.append(command)

            emoji = ''

            with open(code_path + '/emojist.json') as file:
                emojis = json.loads(file.read(), object_pairs_hook=OrderedDict)

                for key, value in emojis["emojis"].items():
                    if key in script:
                        emoji = value
                        break

                if emoji == '':
                    emoji = emojis['default']

            formatted = f'{i:2} │ {emoji:2s}{Style.BRIGHT}{Fore.MAGENTA} {base_run_command}' +\
                f'{Style.BRIGHT}{Fore.GREEN} {script:20s}' +\
                f' :{Fore.BLUE}{Style.DIM}{Style.NORMAL}  {command}'

            questions.append(formatted)

        if "-l" in sys.argv or "--list" in sys.argv:

            for el in questions:
                print(el)

        elif "-r" in sys.argv or "--raw" in sys.argv:
            print(json.dumps(list(zip(
                list(map(lambda script: f'{base_run_command} {script}' ,scripts)), commands))))

        else:
            try:
                # Inquirer
                inquirerQuestions = [inquirer.List(
                    'Script',  message="Script to run", choices=questions)]

                answers = inquirer.prompt(
                    inquirerQuestions,  theme=GreenPassion())

                index = questions.index(answers['Script'])

                print('')
                print('> Complete the arguments if needed then hit enter:')
                print('')

                params = input(
                    f'{Style.BRIGHT}{Fore.MAGENTA}yarn {Style.BRIGHT}{Fore.GREEN}{scripts[index]}{Style.RESET_ALL} ')

                command = f"{base_run_command} {scripts[index]} {params}"

                print(command)

                if "-c" in sys.argv or "--clipboard" in sys.argv:
                    pyperclip.copy(command)
                    print('\nCommand copied to the clipboard.')

                else:
                    subprocess.run(f'cd {path}; {command}', shell=True)

            except KeyboardInterrupt:
                print('\nExiting...')

else:
    print("There is no file called `package.json` in the current path: " + path)
