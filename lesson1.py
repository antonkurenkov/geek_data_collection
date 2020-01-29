import requests
# from pprint import pprint
import json

main_url = 'https://api.github.com/'
user = 'antonkurenkov'

response = requests.get('https://api.github.com/users/' + user + '/repos')

if response.ok:
    for repo in response.json():
        # pprint(repo['name'])
        print(repo['name'])

with open(f'{user}_repos.json', 'w') as file:
    json.dump(response.json(), file)