import requests

# Get the two teams
print("What are the names of the two teams that you want to fight?")
team1 = input('Team 1: ')
team2 = input('Team 2: ')
boWhat = input('Best of what: ')

r = requests.get(f"http://localhost:8000/mlm/predict/?team1={team1}&team2={team2}&boWhat={boWhat}")

print(r.text)