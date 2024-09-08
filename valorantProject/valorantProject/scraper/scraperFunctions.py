import requests
from bs4 import BeautifulSoup
from .models import *
import datetime

# Make it so if it can't find the player, it asks for the players information (like hiro)

def getAllMatchPages() -> list:
    interestedTeams = [
        # Americas
        '100 thieves',
        'cloud9',
        'evil geniuses',
        'furia',
        'krü esports',
        'leviatán',
        'loud',
        'mibr',
        'nrg esports',
        'sentinels',
        'g2 esports',
        
        # CN
        'all gamers',
        'bilibili gaming',
        'edward gaming',
        'funplus phoenix',
        'jdg esports',
        'nova esports',
        'titan esports club',
        'trace esports',
        'tyloo',
        'wolves esports',
        'dragon ranger gaming',
        
        # EMEA
        'bbl esports',
        'fnatic',
        'fut esports',
        'karmine corp',
        'koi',
        'natus vincere',
        'team heretics',
        'team liquid',
        'team vitality',
        'gentle mates',
        'giantx',
        
        # Pacific
        'detonation focusme',
        'drx',
        'gen.g',
        'global esports',
        'paper rex',
        'rex regum qeon',
        't1',
        'talon esports',
        'team secret',
        'zeta division',
        'bleed'
    ]
    baseResultsWebpage = "https://www.vlr.gg/matches/results"
    resultsWebpage = ""
    columnClass = "col mod-1"
    cardClass = "wf-card"
    containerClassName = "match-item-vs-team"
    teamClassName = "text-of"
    frontWebsiteURL = "https://www.vlr.gg"
    allMatchPages = []
    endingPage = 10
    
    # Go through all the cards to find the a tags
    for page in range(1, endingPage + 1):
        
        if page == 1:
            resultsWebpage = baseResultsWebpage
        else:
            resultsWebpage = baseResultsWebpage + f"/?page={page}"
        
        print(f"Results webpage: {resultsWebpage}")
        
        # Get the webpage and clean it up
        r = requests.get(resultsWebpage)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Funnel the search down by column and cards
        column = soup.find('div', class_=columnClass)
        cards = column.find_all('div', class_=cardClass)
        
        for i in cards:
            matches = i.find_all('a')
            
            # Check if the match is between two interested teams
            for match in matches:
                if not match: # If there isn't a match, continue
                    continue
                
                # Reset team1 and team2
                teams = []
                bigContainer = match.find_all('div', class_=containerClassName)
                for team in bigContainer:
                    smallContainer = team.find('div', class_=teamClassName)
                    
                    teams.append(smallContainer.get_text(strip=True))
                
                # If two teams weren't grabbed, continue
                if len(teams) != 2:
                    continue
                
                # Grab the winning team's name
                team1 = teams[0]
                team2 = teams[1]
                
                # If team1 or team2 isn't an interested team, move onto the next match
                if (not team1 or not team2) or (team1.lower() not in interestedTeams or team2.lower() not in interestedTeams):
                    continue
                
                # Ensure team1 and team2 are different
                if team1 == team2:
                    print(f"Warning: Identical teams detected: {team1} vs {team2}")
                    continue
                
                # Output the grabbed match
                print(f"Grabbed {team1} vs {team2}")
                
                # If you made it this far, both teams are an interested team, so grab their href
                href = frontWebsiteURL + match.get('href')
                allMatchPages.append(href)
    
    return allMatchPages

# Find the correct region based off country
# Returns the teams 'short' name
def findShortRegion(region) -> str:
    EMEA = ['turkey', 'europe', 'united kingdom', 'france', 'spain', 'ukraine', 'netherlands']
    AMER = ['brazil', 'united states', 'argentina', 'chile']
    
    if region.lower() in EMEA: #EMEA
        return "EMEA"
    elif region.lower() in AMER: #Americas
        return "AMER"
    elif region.lower() == "china": #China
        return "CN"
    else: #Pacific
        return "PAC"

# Adds the players on a team to the database
# Returns True if successful, False if unsuccessful
def addPlayersToDatabase(theTeam, teamName, soup) -> bool:
    #Class names
    bigContainerClassName = "team-summary-container-1"
    mediumContainerClassName = "wf-card"
    smallContainerStyleName = "display: flex; flex-wrap: wrap;"
    playerContainerClassName = "team-roster-item"
    playerIgnClassName = "team-roster-item-name-alias"
    playerNameClassName = "team-roster-item-name-real"
    starClassName = "fa fa-star"
    statusClassName = "wf-tag mod-light team-roster-item-name-role"
    
    #Filter down to smallest container possible 
    container = soup.find('div', class_=bigContainerClassName)
    container = container.find('div', class_=mediumContainerClassName)
    #There are two of these, but I'm just grabbing the first one
    container = container.find('div', attrs={'style': smallContainerStyleName})
    cards = container.find_all('div', class_=playerContainerClassName)
    
    for card in cards:
        #Find their in-game-name, name, if they're the IGL, if they're a sub, and if they're inactive
    
        #Find their in-game-name
        ign = card.find('div', class_=playerIgnClassName)
        if ign is None:
            print(f"Couldn't find {teamName}'s player IGN")
            return False
        ign = ign.get_text(strip=True)
        
        #Find their name
        name = card.find('div', class_=playerNameClassName)
        if name is None:
            print(f"Couldn't find {teamName}'s {ign} player name")
            return False
        name = name.get_text(strip=True)
        
        #Find if they're the IGL
        isIgl = False
        star = card.find('i', class_=starClassName)
        if star: #If we found the star
            isIgl = True
        
        #Find if they're a sub or inactive
        isSub = False
        isInactive = False
        text = card.find('div', class_=statusClassName)
        if text: #If the text is there
            text = text.get_text(strip=True).lower()
            if text == "sub":
                isSub = True
            elif text == "inactive":
                isInactive = True
            else:
                print(f"Found {teamName} {ign} status text, but the text is invalid.")
                return False
        
        #Add the player to the database
        thePlayer = Player.objects.create(currentTeam=theTeam, ign=ign, name=name, isIgl=isIgl, isSub=isSub, isInactive=isInactive)
        thePlayer.save()
        print(f"Added the player {theTeam.shortName} {ign} to the database: Igl? {isIgl}, Sub? {isSub}, Inactive? {isInactive}")
        
    return True

# Adds a team to the database
# Returns True if successful, False if unsuccessful
def addTeamToDatabase(teamName, soup, isTeam1) -> bool:
    # Class names
    frontWebsiteURL = "https://www.vlr.gg"
    anchorClassName = ""
    if isTeam1 == True:
        anchorClassName = "match-header-link wf-link-hover mod-1"
    else:
        anchorClassName = "match-header-link wf-link-hover mod-2"
    containerClassName = "team-header-desc"
    shortNameClassName = "wf-title team-header-tag"
    regionClassName = "team-header-country"
    
    # Get the team's website
    anchorClass = soup.find('a', class_=anchorClassName)
    teamWebsite = frontWebsiteURL + anchorClass.get('href')
    
    # Get the teams website
    r = requests.get(teamWebsite)
    teamSoup = BeautifulSoup(r.content, 'html.parser')
    
    # Get all the information needed for database (shortName, region. Name is already found)
    container = teamSoup.find('div', class_=containerClassName)
    if container is None:
        print(f"{teamName} short name container not found")
        return False
    
    # Short names exception box
    shortNameExceptions = ["DRX", "MIBR", "KOI", "T1"]
    
    # Find their short name
    shortName = container.find('h2', class_=shortNameClassName)
    if shortName is None:
        if teamName in shortNameExceptions:
            # Put it inside BeautifulSoup so no error is thrown
            shortName = BeautifulSoup(f"<h2>{teamName}</h2>", 'html.parser')
        else:
            print(f"{teamName} short name not found")
            return False
    shortName = shortName.get_text(strip=True)
    
    # Find their region
    region = container.find('div', class_=regionClassName)
    if region is None:
        print(f"{teamName} region not found")
        return False
    region = region.get_text(strip=True)
    shortRegion = findShortRegion(region) # Find the region's short name
    
    # Put the team into the database
    theTeam = Team.objects.create(name=teamName, shortName=shortName, region=shortRegion)
    theTeam.save()
    print(f"Added the team {teamName} to the database: {shortName}, {shortRegion}")
    
    # Add players to the database
    if not addPlayersToDatabase(theTeam, teamName, teamSoup): #If adding players to the database failed
        print(f"Adding {teamName}'s players to the database failed.")
        return False
    
    return True

# Grabs the names of both team1 and team2, and adds them to the database if not recognized
def getTeamNames(soup):
    # Class names
    team1ContainerClassName = "match-header-link-name mod-1"
    team2ContainerClassName = "match-header-link-name mod-2"
    possibleClassName1 = "wf-title-med"
    possibleClassName2 = "wf-title-med mod-single"
    
    # Grab the container of team1
    team1Container = soup.find('div', class_=team1ContainerClassName)
    if team1Container is None:
        print ("Error. Couldn't find team 1 container")
        return None
    
    # Grab the name of team1
    team1 = team1Container.find('div', class_=possibleClassName1)
    if team1 is None: # If the team name doesn't come up
        team1 = team1Container.find('div', class_=possibleClassName2)
        if team1 is None:
            print("Error. Couldn't find team 1")
            return None
            
    # Grab the container of team2
    team2Container = soup.find('div', class_=team2ContainerClassName)
    if team2Container is None:
        print("Error. Couldn't find team 2 container")
        return None
    
    # Grab the name of team2
    team2 = team2Container.find('div', class_=possibleClassName1)
    if team2 is None: # If the team name doesn't come up
        team2 = team2Container.find('div', class_=possibleClassName2)
        if team2 is None:
            print("Error. Couldn't find team 2")
            return None
    
    # Clean up the team names
    team1Name = team1.get_text(strip=True)
    team2Name = team2.get_text(strip=True)
    
    # If team isn't in database, add it
    if not Team.objects.filter(name=team1Name).exists():
        if not addTeamToDatabase(team1Name, soup, True):
            print(f"Couldn't add {team1Name} to database")
    if not Team.objects.filter(name=team2Name).exists(): 
        if not addTeamToDatabase(team2Name, soup, False):
            print(f"Couldn't add {team2Name} to database")
    
    return (team1Name, team2Name)

def addPlayerToDatabase(teamShortName, ign, playerUrl):
    # Class Names
    playerHeaderContainerClassName = "player-header"
    playerNameClassName = "player-real-name ge-text-light"
    
    # Grab the players website and clean it up
    r = requests.get(playerUrl)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    # Grab the players real name
    playerHeaderContainer = soup.find('div', class_=playerHeaderContainerClassName)
    name = playerHeaderContainer.find('h2', class_=playerNameClassName) # type: ignore
    if name is None:
        print("Couldn't find players name")
    name = name.get_text(strip=True)
    
    # Save the player to the database
    theTeam = Team.objects.get(shortName=teamShortName)
    thePlayer = Player.objects.create(
        currentTeam = None,
        ign = ign,
        name = name,
        isIgl = False
    )
    thePlayer.save()
    
    #Connect the player to their old team
    
    # Save the player team connection to the database
    thePlayerTeamConnection = PlayerTeamConnection.objects.create(
        player = thePlayer,
        team = theTeam
    )
    thePlayerTeamConnection.save()
    
    # Django automatically connects the player team connection to the player, so I'm
    # saving it now to make sure it gets updated
    thePlayer.save()
    
    print(f"Added the player {teamShortName} {ign} to the database")

# Grabs the stats of the players in a match and connects them to the match in the database
# Return True if successful, False if unsuccessful
def addPlayerMatchConnectionToDatabase(theMatch, isBo3, soup) -> bool:
    #Class names
    mapCardsContainerClassName = "vm-stats-container"
    matchCardClassName = "vm-stats-game mod-active"
    teamTableClassName = "wf-table-inset mod-overview"
    playerNameContainerClassName = "mod-player"
    playerNameClassName = "text-of"
    playerStatsContainerClassName = "mod-stat"
    playerStatsClassName = "mod-both"
    
    #Grab each players stats and connect it to the match
    
    #Grab the stats of each player
    cards = soup.find('div', class_=mapCardsContainerClassName)
    card = cards.find('div', class_=matchCardClassName)
    tables = card.find_all('table', class_=teamTableClassName)
        
    for team in tables:
        rows = team.find('tbody')
        rows = rows.find_all('tr')
        for player in rows:
            # Find the players name
            nameContainer = player.find('td', class_=playerNameContainerClassName)
            ign = nameContainer.find('div', class_=playerNameClassName)
            if ign is None:
                return False
            ign = ign.get_text(strip=True)
            
            # Find the players stats
            statList = []
            stats = player.find_all('td', class_=playerStatsContainerClassName)
            for stat in stats:
                statList.append(stat.find('span', class_=playerStatsClassName).get_text(strip=True))
            
            # Clean up data
            if statList[5][0] == "+":
                statList[5] = statList[5].lstrip('+')
            if len(statList[6]) == 2:
                statList[6] = statList[6][0]
            else:
                statList[6] = statList[6][0:2]
            if len(statList[8]) == 2:
                statList[8] = statList[8][0]
            else:
                statList[8] = statList[8][0:2]
            if statList[11][0] == "+":
                statList[11] = statList[11].lstrip('+')
            
            # Add the stuff to the database
            print(f"ign: {ign}")
            
            # Try to find the player. If it doesn't exist, ask for players URL
            try:
                player = Player.objects.get(ign=ign)
            except Player.DoesNotExist:
                # Find the team's short name
                teamShortNameClassName = "ge-text-light"
                teamShortName = nameContainer.find('div', class_=teamShortNameClassName).get_text(strip=True)
                
                # Ask for their URL
                playerUrl = input(f"What's {teamShortName} {ign}'s URL?")
                
                # Add the player to the database
                addPlayerToDatabase(teamShortName, ign, playerUrl)
                
                player = Player.objects.get(ign=ign)
                
            if isBo3: # If it's a Bo3
                theConnection = PlayerMatchBO3Connection.objects.create(
                    player=player,
                    match=theMatch,
                    rating=float(statList[0]) if statList[0] != '' else None,
                    acs=int(statList[1]),
                    kills=int(statList[2]),
                    deaths=int(statList[3]),
                    assists=int(statList[4]),
                    kd=int(statList[5]),
                    kast=int(statList[6]) if statList[6] != '' else None,
                    adr=int(statList[7]),
                    hsp=int(statList[8]),
                    fk=int(statList[9]),
                    fd=int(statList[10]),
                    fkfd=int(statList[11])
                )
                theConnection.save()
            else: # If it's a Bo5
                theConnection = PlayerMatchBO5Connection.objects.create(
                    player=player,
                    match=theMatch,
                    rating=float(statList[0]) if statList[0] != '' else None,
                    acs=int(statList[1]),
                    kills=int(statList[2]),
                    deaths=int(statList[3]),
                    assists=int(statList[4]),
                    kd=int(statList[5]),
                    kast=int(statList[6]) if statList[6] != '' else None,
                    adr=int(statList[7]),
                    hsp=int(statList[8]),
                    fk=int(statList[9]),
                    fd=int(statList[10]),
                    fkfd=int(statList[11])
                )
                theConnection.save()
            print(f"Added a connection between {player.currentTeam.shortName if player.currentTeam else ""} {player.ign} and {theMatch.team1.shortName} vs {theMatch.team2.shortName} on {theMatch.date}")
            
    return True

# Adds a match to the database
# Return True if successful, returns False if unsuccessful
def addMatchToDatabase(team1Name, team2Name, date, isBo3, soup):
    #Class names
    scoreContainerClassName = "js-spoiler"
    scoreWinnerClassName = "match-header-vs-score-winner"
    mapPicksAndBansClassName = "match-header-note"
    mapCardsContainerClassName = "vm-stats-container"
    mapCardsClassName = "vm-stats-game"
    team1ScoreContainer = "team"
    team2ScoreContainer = "team mod-right"
    scores1ClassName = "score"
    scores2ClassName = "score mod-win"
    
    #Get the match winner, what maps were picked, and who won each map
    
    #Grab the match winner
    # Filter down to the scores
    scores = soup.find('div', class_=scoreContainerClassName)
    scores = scores.find_all('span')
    
    # Find the score that is the winner
    matchWinnerIndex = -1
    for matchWinnerIndex in range(len(scores)):
        if scores[matchWinnerIndex].get('class') == scoreWinnerClassName:
            break
    
    # If the first number in the list is the winner, then it's team1, and so on
    if matchWinnerIndex == 0: #If team1 won
        winner = Team.objects.get(name=team1Name)
    else: #If team2 won
        winner = Team.objects.get(name=team2Name)
    
    #Grab what maps were picked
    picksAndBansString = soup.find('div', class_=mapPicksAndBansClassName)
    if picksAndBansString is None:
        return False
    picksAndBansString = picksAndBansString.get_text(strip=True)
    
    # Initialize the variables
    bannedMaps = []
    pickedMaps = []
    
    # Split the string by semicolon
    actions = picksAndBansString.split(';')
    
    # Go through every 'action' to find the picks and bans
    for action in actions:
        action = action.strip() # Get rid of the spaces that might be around it
        
        # Find whether it's a pick of a ban
        if "ban" in action: # If it's a map ban
            # Extract the map name after 'ban'
            mapName = action.split('ban')[-1].strip()
            bannedMaps.append(mapName)
        elif "pick" in action: # If it's a map pick
            # Extract the map name after 'pick'
            mapName = action.split('pick')[-1].strip()
            pickedMaps.append(mapName)
        elif "remain" in action: # If it's the last map (still technically a 'pick')
            # Extract the map name before 'remain'
            mapName = action.split('remain')[0].strip()
            pickedMaps.append(mapName)
        
    #Grab who won each map and their scores
    cards = soup.find('div', class_=mapCardsContainerClassName)
    cards = cards.find_all('div', class_=mapCardsClassName)
    for i in cards: #find_all grabs some classes that aren't an exact match. This deletes those
        if len(i.get('class')) != 1:
            cards.remove(i)
    
    # Loop through every card to find who won each map
    whoWonEachMap = [] # The name of a team who won the map
    scoresOfEachMap = [] # A 2D list that contains the scores of each team per map
    for card in cards:
        team1Container = card.find('div', class_=team1ScoreContainer)
        team2Container = card.find('div', class_=team2ScoreContainer)
        team1Score = team1Container.find('div', class_=scores1ClassName)
        if team1Score is None:
            team1Score = team1Container.find('div', class_=scores2ClassName)
        team2Score = team2Container.find('div', class_=scores1ClassName)
        if team2Score is None:
            team2Score = team1Container.find('div', class_=scores2ClassName)
        
        # Assign the score to the correct team
        team1Score = int(team1Score.get_text(strip=True))
        team2Score = int(team2Score.get_text(strip=True))
        
        # Find which team won
        scoresOfEachMap.append([team1Score, team2Score])
        if team1Score > team2Score: # If team 1 won
            whoWonEachMap.append(team1Name)
        else: # If team2 won
            whoWonEachMap.append(team2Name)
    
    # If all maps weren't played, make the ones that weren't played null
    if isBo3 and len(whoWonEachMap) < 3: # If the game was a Bo3, and less than 3 maps were played
        #If the games aren't equal to three, the last game wasn't played. Make it null.
        for i in range(len(whoWonEachMap), 3):
            whoWonEachMap.append("null")
            scoresOfEachMap.append([-1, -1])
    elif not isBo3 and len(whoWonEachMap) < 5: # If the game was a Bo5, and less than 5 maps were played
        #If the games aren't equal to five, the last couple games may not have been played. Make the ones that don't exist equal null.
        for i in range(len(whoWonEachMap), 5):
            whoWonEachMap.append("null")
            scoresOfEachMap.append([-1, -1])
    
    #Add the match to the database
    if isBo3: #If the match was a Bo3
        theMatch = MatchBO3.objects.create(
            team1 = Team.objects.get(name=team1Name),
            team2 = Team.objects.get(name=team2Name),
            date = date,
            matchWinner = winner,
            mapBan1 = bannedMaps[0],
            mapBan2 = bannedMaps[1],
            mapPick1 = pickedMaps[0],
            mapPick2 = pickedMaps[1],
            mapBan3 = bannedMaps[2],
            mapBan4 = bannedMaps[3],
            mapPick3 = pickedMaps[2],
            team1Map1RoundsWon = scoresOfEachMap[0][0],
            team2Map1RoundsWon = scoresOfEachMap[0][1],
            map1Winner = Team.objects.get(name=whoWonEachMap[0]),
            team1Map2RoundsWon = scoresOfEachMap[1][0],
            team2Map2RoundsWon = scoresOfEachMap[1][1],
            map2Winner = Team.objects.get(name=whoWonEachMap[1]),
            team1Map3RoundsWon = scoresOfEachMap[2][0] if scoresOfEachMap[2][0] != -1 else None,
            team2Map3RoundsWon = scoresOfEachMap[2][1] if scoresOfEachMap[2][1] != -1 else None,
            map3Winner = Team.objects.get(name=whoWonEachMap[2]) if whoWonEachMap[2] != "null" else None
        )
        theMatch.save()
        print(f"Added the Bo3 Match {team1Name} vs {team2Name} to the database")
    else: #If the match was a Bo5
        theMatch = MatchBO5.objects.create(
            team1 = Team.objects.get(name=team1Name),
            team2 = Team.objects.get(name=team2Name),
            date = date,
            matchWinner = winner,
            mapBan1 = bannedMaps[0],
            mapBan2 = bannedMaps[1],
            mapPick1 = pickedMaps[0],
            mapPick2 = pickedMaps[1],
            mapPick3 = pickedMaps[2],
            mapPick4 = pickedMaps[3],
            mapPick5 = pickedMaps[4],
            team1Map1RoundsWon = scoresOfEachMap[0][0],
            team2Map1RoundsWon = scoresOfEachMap[0][1],
            map1Winner = Team.objects.get(name=whoWonEachMap[0]),
            team1Map2RoundsWon = scoresOfEachMap[1][0],
            team2Map2RoundsWon = scoresOfEachMap[1][1],
            map2Winner = Team.objects.get(name=whoWonEachMap[1]),
            team1Map3RoundsWon = scoresOfEachMap[2][0],
            team2Map3RoundsWon = scoresOfEachMap[2][1],
            map3Winner = Team.objects.get(name=whoWonEachMap[2]),
            team1Map4RoundsWon = scoresOfEachMap[3][0] if scoresOfEachMap[3][0] != -1 else None,
            team2Map4RoundsWon = scoresOfEachMap[3][1] if scoresOfEachMap[3][1] != -1 else None,
            map4Winner = Team.objects.get(name=whoWonEachMap[3]) if whoWonEachMap[3] != "null" else None,
            team1Map5RoundsWon = scoresOfEachMap[4][0] if scoresOfEachMap[4][0] != -1 else None,
            team2Map5RoundsWon = scoresOfEachMap[4][1] if scoresOfEachMap[4][1] != -1 else None,
            map5Winner = Team.objects.get(name=whoWonEachMap[4]) if whoWonEachMap[4] != "null" else None
        )
        theMatch.save()
        print(f"Added the Bo5 Match {team1Name} vs {team2Name} to the database")
        
    
    #Connect the players to the match
    if not addPlayerMatchConnectionToDatabase(theMatch, isBo3, soup):
        return False
    
    return True

# Gets the scores of a match, and adds them to the database if not recognized
def getMatchScores(soup, team1Name, team2Name):
    # Class names
    containerClassName = "match-header-vs-score"
    spoilerClassName = "js-spoiler"
    bestOfWhatClassName = "match-header-vs-note"
    dateContainerClassName = "match-header-date"
    dateClassName = "moment-tz-convert"
    
    # Find the scores
    scores = soup.find('div', class_=containerClassName)
    scores = scores.find('div', class_=spoilerClassName)
    scores = scores.find_all('span')
    
    # Get rid of the : and grab the text, not the entire line of code
    realScores = []
    for score in scores:
        if not (score.get_text(strip=True) == ":"):
            realScores.append(score.get_text(strip=True))
        
    # Find the day the game was played
    date = soup.find('div', class_=dateContainerClassName)
    date = date.find('div', class_=dateClassName)
    if date is None:
        print(f"{team1Name} vs {team2Name} date couldn't be found")
        return None
    date = date.get('data-utc-ts') #Get the date in its unchanged format
    date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])) #year, month, day
    
    # Find if it's a Bo3 or Bo5
    bestOfWhat = soup.find('div', class_=containerClassName)
    bestOfWhat = bestOfWhat.find_all('div', class_=bestOfWhatClassName)
    isBo3 = False
    if bestOfWhat[1].get_text(strip=True).lower() == "bo3":
        isBo3 = True
    
    # Adds the match to the database
    if isBo3: #If it's a Bo3
        #If the game doesn't exist (checks based off team1, team2, and the date)
        if not MatchBO3.objects.filter(team1=Team.objects.get(name=team1Name),
                                       team2=Team.objects.get(name=team2Name),
                                       date=date).exists():
            if not addMatchToDatabase(team1Name, team2Name, date, isBo3, soup):
                print(f"Couldn't add the match {team1Name} vs {team2Name} on {date} to the database")
                return None
    else: #If it's a Bo5
        #If the game doesn't exist (checks based off team1, team2, and the date)
        if not MatchBO5.objects.filter(team1=Team.objects.get(name=team1Name),
                                       team2=Team.objects.get(name=team2Name),
                                       date=date).exists():
            if not addMatchToDatabase(team1Name, team2Name, date, isBo3, soup):
                print(f"Couldn't add the match {team1Name} vs {team2Name} on {date} to the database")
                return None
    
    return tuple(realScores)

