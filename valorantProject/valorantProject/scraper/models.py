from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=4)
    region = models.CharField(max_length=4)

    def __str__(self):
        return self.shortName + " (" + self.name + ")"

# A Best-Of-3 Match
class MatchBO3(models.Model):
    # Teams that attended
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matchesAsTeam1BO3")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matchesAsTeam2BO3")

    # Date the match happened
    date = models.DateField()
    
    # Winner of Match
    matchWinner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matchWinnerBO3")
    
    # Map picks and bans
    mapBan1 = models.CharField(max_length=50)
    mapBan2 = models.CharField(max_length=50)
    mapPick1 = models.CharField(max_length=50)
    mapPick2 = models.CharField(max_length=50)
    mapBan3 = models.CharField(max_length=50)
    mapBan4 = models.CharField(max_length=50)
    mapPick3 = models.CharField(max_length=50)

    # Winners of each map
    team1Map1RoundsWon = models.IntegerField()
    team2Map1RoundsWon = models.IntegerField()
    map1Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map1WinnerBO3")
    
    team1Map2RoundsWon = models.IntegerField()
    team2Map2RoundsWon = models.IntegerField()
    map2Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map2WinnerBO3")
    
    team1Map3RoundsWon = models.IntegerField(null=True, blank=True)
    team2Map3RoundsWon = models.IntegerField(null=True, blank=True)
    map3Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map3WinnerBO3", null=True, blank=True)

    def __str__(self):
        return f"BO3 Match between {self.team1.shortName} and {self.team2.shortName} on {self.date}"

# A Best-Of-5 Match
class MatchBO5(models.Model):
    # Teams that attended
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matchesAsTeam1BO5")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matchesAsTeam2BO5")

    # Date the match happened
    date = models.DateField()
    
    # Winner of Match
    matchWinner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="matchWinnerBO5")
    
    # Map picks and bans
    mapBan1 = models.CharField(max_length=50)
    mapBan2 = models.CharField(max_length=50)
    mapPick1 = models.CharField(max_length=50)
    mapPick2 = models.CharField(max_length=50)
    mapPick3 = models.CharField(max_length=50)
    mapPick4 = models.CharField(max_length=50)
    mapPick5 = models.CharField(max_length=50)

    # Winners of each map
    team1Map1RoundsWon = models.IntegerField()
    team2Map1RoundsWon = models.IntegerField()
    map1Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map1WinnerBO5")
    
    team1Map2RoundsWon = models.IntegerField()
    team2Map2RoundsWon = models.IntegerField()
    map2Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map2WinnerBO5")
    
    team1Map3RoundsWon = models.IntegerField()
    team2Map3RoundsWon = models.IntegerField()
    map3Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map3WinnerBO5")
    
    team1Map4RoundsWon = models.IntegerField(null=True, blank=True)
    team2Map4RoundsWon = models.IntegerField(null=True, blank=True)
    map4Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map4WinnerBO5", null=True, blank=True)
    
    team1Map5RoundsWon = models.IntegerField(null=True, blank=True)
    team2Map5RoundsWon = models.IntegerField(null=True, blank=True)
    map5Winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="map5WinnerBO5", null=True, blank=True)

    def __str__(self):
        return f"BO5 Match between {self.team1.shortName} and {self.team2.shortName} on {self.date}"

class Player(models.Model):
    currentTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="playersCurrentTeam", null=True, blank=True)
    ign = models.CharField(max_length=250)
    name = models.CharField(max_length=500)
    isIgl = models.BooleanField() #Is in-game-leader
    isSub = models.BooleanField(default=False) #Is sub
    isInactive = models.BooleanField(default=False) #Is inactive

    matchesBO3 = models.ManyToManyField(MatchBO3, through="PlayerMatchBO3Connection", related_name="players")
    matchesBO5 = models.ManyToManyField(MatchBO5, through="PlayerMatchBO5Connection", related_name="players")
    teams = models.ManyToManyField(Team, through="PlayerTeamConnection", related_name="players")

    def __str__(self):
        return self.ign

class PlayerMatchBO3Connection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(MatchBO3, on_delete=models.CASCADE)

    # Player Stats
    rating = models.FloatField(null=True, blank=True) # VLR Rating
    acs = models.IntegerField() # ACS
    kills = models.IntegerField() # Kills
    deaths = models.IntegerField() # Deaths
    assists = models.IntegerField() # Assists
    kd = models.IntegerField() # Kills - Deaths
    kast = models.IntegerField(null=True, blank=True) # Kill, Assist, Trade, Survive %
    adr = models.IntegerField() # Average Damage Per Roung
    hsp = models.IntegerField() # Headshot Percentage
    fk = models.IntegerField() # First Kills
    fd = models.IntegerField() # First Deaths
    fkfd = models.IntegerField() # First Kills - First Deaths

    def __str__(self):
        return f"{self.player.ign} on match ({self.match})"
    
class PlayerMatchBO5Connection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(MatchBO5, on_delete=models.CASCADE)

    # Player Stats
    rating = models.FloatField(null=True, blank=True) # VLR Rating
    acs = models.IntegerField() # ACS
    kills = models.IntegerField() # Kills
    deaths = models.IntegerField() # Deaths
    assists = models.IntegerField() # Assists
    kd = models.IntegerField() # Kills - Deaths
    kast = models.IntegerField(null=True, blank=True) # Kill, Assist, Trade, Survive %
    adr = models.IntegerField() # Average Damage Per Roung
    hsp = models.IntegerField() # Headshot Percentage
    fk = models.IntegerField() # First Kills
    fd = models.IntegerField() # First Deaths
    fkfd = models.IntegerField() # First Kills - First Deaths

    def __str__(self):
        return f"{self.player.ign} on match ({self.match})"

class PlayerTeamConnection(models.Model):
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.team.shortName} {self.player.ign}" # type: ignore