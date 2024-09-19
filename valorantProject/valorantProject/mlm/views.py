from django.http import HttpResponse
from .fit import doModelFitStuff
from .predict import doModelPredictStuff

# Create your views here.

def fit(request):
    didModelWork = doModelFitStuff()
    
    # If the model didn't work
    if not didModelWork:
        return HttpResponse("The model didn't fit")
    
    return HttpResponse("The model fit!")

def predict(request):
    
    team1 = request.GET.get('team1', None)
    team2 = request.GET.get('team2', None)
    
    if not team1 or not team2:
        return HttpResponse("No teams input")
    
    print(f"{team1} vs {team2}")
    
    winner = doModelPredictStuff(team1, team2)
    
    if winner is None:
        return HttpResponse(f"{team1} or {team2} isn't a team")
    
    return HttpResponse(f"{winner} is the winner!")