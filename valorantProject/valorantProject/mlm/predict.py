from scraper.models import Team
import joblib
import numpy as np

def findTeamIDs(team1Name, team2Name):
    print("Finding team ID's")
    
    # Find the first team
    try:
        team1 = Team.objects.get(name=team1Name)
    except:
        try:
            team1 = Team.objects.get(shortName=team1Name)
        except:
            return team1Name, team2Name, False
        
    # Find the second team
    try:
        team2 = Team.objects.get(name=team2Name)
    except:
        try:
            team2 = Team.objects.get(shortName=team2Name)
        except:
            return team1Name, team2Name, False
    
    return team1.id, team2.id, True

def loadModels():
    print("Loading saved models and encoder")
    
    modelBo3 = joblib.load('valorantModelBo3.pkl')
    modelBo5 = joblib.load('valorantModelBo5.pkl')
    encoder = joblib.load('oneHotEncoder.pkl')
    
    print("Models and encoder finished loading")
    return modelBo3, modelBo5, encoder

def predictWinner(model, team1ID, team2ID, encoder):
    print("Starting the prediction")
    
    # Convert team id's to encoded id's so it can be given to the model
    team1Encoded = encoder.transform(np.array(team1ID).reshape(-1,1))
    team2Encoded = encoder.transform(np.array(team2ID).reshape(-1,1))
    
    # Concatenate the encoded teams
    matchInput = np.hstack([team1Encoded, team2Encoded])
    
    # Make a prediction
    prediction = model.predict(matchInput)
    
    return prediction

def doModelPredictStuff(team1, team2) -> str:
    
    team1ID, team2ID, didItWork = findTeamIDs(team1, team2)
    if not didItWork:
        return None
    
    modelBo3, modelBo5, encoder = loadModels()
    predictedWinnerBo3 = predictWinner(modelBo3, team1ID, team2ID, encoder)
    
    if predictedWinnerBo3 == team1ID:
        return team1
    else:
        return team2