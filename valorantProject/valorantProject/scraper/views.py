from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import *
from .scraperFunctions import getAllMatchPages, getTeamNames, getMatchScores

# Create your views here.

# The scraper
def scraper(request):
    print("Scarting Scraper...")
    
    # Grab all the matches webpages from vlr.gg/matches/results
    matches = getAllMatchPages()
    
    output = ""
    counter = 1
    matchDataList = []
    for matchURL in matches:
        # Make the GET request
        r = requests.get(matchURL)

        # Parse the HTML
        soup = BeautifulSoup(r.content, 'html.parser')

        # Get all the team names
        teamNames = getTeamNames(soup)
        if teamNames is None:
            return HttpResponse("Team names not found")
        
        team1Name = teamNames[0] # Get the first team name
        if team1Name is None: # Error check
            return HttpResponse("Team 1 Name not found")
        
        team2Name = teamNames[1] # Get the second team name
        if team2Name is None: # Error check
            return HttpResponse("Team 2 Name not found")

        # Store the team names and their corresponding soups
        matchDataList.append({
            'teamNames': teamNames,
            'soup': soup
        })
    
    for matchData in matchDataList:
        teamNames = matchData['teamNames']
        soup = matchData['soup']
        
        team1Name = teamNames[0]
        team2Name = teamNames[1]
        
        # Grab the score
        teamScore = getMatchScores(soup, team1Name, team2Name)
        if teamScore is None:
            print("Couldn't find team score")
            continue
        team1Score = teamScore[0] # Get the first team score
        if team1Score is None:
            return HttpResponse("Team 1 Score not found")
        team2Score = teamScore[1] # Get the second team score
        if team2Score is None:
            return HttpResponse("Team 2 Score not found")        
        
        # Put it into the output
        output = f"{output}{counter}. {team1Name} vs {team2Name}: {team1Score} to {team2Score}\n"
        counter = counter + 1
    
    print("Scraping completed")
    
    return HttpResponse(output)
