from django.http import HttpResponse
from .fit import doModelFitStuff
from .predict import doModelPredictStuff

# Create your views here.

def fit(request):
    
    # Grab what model they want to use
    whichModel = request.GET.get('model', None).lower()
    
    if whichModel is None:
        whichModel = "randomforestclassifier"
    
    # Fit the model
    didModelWork = doModelFitStuff(whichModel)
    
    # If the model didn't work
    if not didModelWork:
        return HttpResponse("The model didn't fit")
    
    return HttpResponse("The model fit!")

def predict(request):
    
    # Get the team names
    try:
        boWhat = int(request.GET.get('boWhat', None))
    except:
        return HttpResponse("boWhat is not an integer")
    team1 = request.GET.get('team1', None)
    team2 = request.GET.get('team2', None)
    
    # If the team names are null, don't continue
    if not team1 or not team2:
        return HttpResponse("No teams input")
    
    # If 3 or 5 wasn't input, don't continue
    if boWhat != 3 and boWhat != 5:
        if boWhat is None:
            boWhat = 3
        else:
            return HttpResponse("Bad boWhat input")
    
    # Say the matchup
    print(f"{team1} vs {team2}")
    
    # Grab the winner
    winner = doModelPredictStuff(team1, team2, boWhat)
    
    # Check if the two are teams
    if winner is None:
        return HttpResponse(f"{team1} or {team2} isn't a team")
    
    return HttpResponse(f"{winner} is the winner!")