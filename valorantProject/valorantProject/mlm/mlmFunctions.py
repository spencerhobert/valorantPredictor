from scraper.models import *
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from django_pandas.io import read_frame

def cleanPlayerStats():
    
    # BO3
    
    print(f"Before cleaning the data: {PlayerMatchBO3Connection.objects.filter(rating__isnull=True).count()} bo3 players have null values")
    
    # For null values, average their values with the data from around it
    
    print("Getting rid of null values in player bo3 stats")
    
    # List of player stat columns to fill
    statColumns = ['rating', 'acs', 'kills', 'deaths', 'assists', 'kd', 'kast', 'adr', 'hsp', 'fk', 'fd', 'fkfd']
    
    # Load data into pandas dataframe
    queryset = PlayerMatchBO3Connection.objects.all().values(
        'id',
        'player_id',
        'match__date',
        *statColumns
    )
    df = pd.DataFrame.from_records(queryset)
        
    # Sort by player and date
    df = df.sort_values(by=['player_id', 'match__date'])
    
    # Forward and backward fill each stat
    print("Before forward and backward")
    for stat in statColumns:
        # Create new columns filled stats
        df[f'{stat}_ffill'] = df.groupby('player_id')[stat].ffill()
        df[f'{stat}_bfill'] = df.groupby('player_id')[stat].bfill()
        
        # Calculate the average of the two nearest stats
        df[f'{stat}_filled'] = df[[f'{stat}_ffill', f'{stat}_bfill']].mean(axis=1)
        
        # Apply the average to the null stat
        df[stat] = df.apply(
            lambda row: row[f'{stat}_filled'] if pd.isnull(row[stat]) else row[stat], axis=1
        )
        
    # Replace remaining NaN values with zero
    df.fillna(0, inplace=True)
    
    # Update database with the filled values (by doing a bulk update)
    print("Before objs")
    objs = [
        PlayerMatchBO3Connection(
            id=row['id'],
            **{field: row[field] for field in statColumns}
        ) for index, row in df.iterrows()
    ]
    PlayerMatchBO3Connection.objects.bulk_update(objs, fields=statColumns)
    
    print(f"After cleaning the data: {PlayerMatchBO3Connection.objects.filter(rating__isnull=True).count()} bo3 players have null values")
    
    # BO5
    
    print(f"Before cleaning the data: {PlayerMatchBO5Connection.objects.filter(rating__isnull=True).count()} bo5 players have null values")
    
    # For null values, average their values with the data from around it
    
    print("Getting rid of null values in player bo5 stats")
    
    # List of player stat columns to fill
    statColumns = ['rating', 'acs', 'kills', 'deaths', 'assists', 'kd', 'kast', 'adr', 'hsp', 'fk', 'fd', 'fkfd']
    
    # Load data into pandas dataframe
    queryset = PlayerMatchBO5Connection.objects.all().values(
        'id',
        'player_id',
        'match__date',
        *statColumns
    )
    df = pd.DataFrame.from_records(queryset)
        
    # Sort by player and date
    df = df.sort_values(by=['player_id', 'match__date'])
    
    # Forward and backward fill each stat
    print("Before forward and backward")
    for stat in statColumns:
        # Create new columns filled stats
        df[f'{stat}_ffill'] = df.groupby('player_id')[stat].ffill()
        df[f'{stat}_bfill'] = df.groupby('player_id')[stat].bfill()
        
        # Calculate the average of the two nearest stats
        df[f'{stat}_filled'] = df[[f'{stat}_ffill', f'{stat}_bfill']].mean(axis=1)
        
        # Apply the average to the null stat
        df[stat] = df.apply(
            lambda row: row[f'{stat}_filled'] if pd.isnull(row[stat]) else row[stat], axis=1
        )
        
    # Replace remaining NaN values with zero
    df.fillna(0, inplace=True)
    
    # Update database with the filled values (by doing a bulk update)
    print("Before objs")
    objs = [
        PlayerMatchBO5Connection(
            id=row['id'],
            **{field: row[field] for field in statColumns}
        ) for index, row in df.iterrows()
    ]
    PlayerMatchBO5Connection.objects.bulk_update(objs, fields=statColumns)
    
    print(f"After cleaning the data: {PlayerMatchBO5Connection.objects.filter(rating__isnull=True).count()} bo5 players have null values")


def cleanMapData():
    


def cleanData():
    print("Cleaning the data")
    
    cleanPlayerStats()
    cleanMapData()


def moveDatabaseToPandas():
    print("Moving database to pandas dataframe")
    
    # Grab ALL VALORANT DATA from the database
    Teams = Team.objects.all().values()
    MatchBO3s = MatchBO3.objects.all().values()
    MatchBO5s = MatchBO5.objects.all().values()
    Players = Player.objects.all().values()
    PlayerMatchBO3Connections = PlayerMatchBO3Connection.objects.all().values()
    PlayerMatchBO5Connections = PlayerMatchBO5Connection.objects.all().values()
    PlayerTeamConnections = PlayerTeamConnection.objects.all().values()
    
    # Transfer to Pandas DataFrame
    df_teams = pd.DataFrame(list(Teams))
    df_matchBo3s = pd.DataFrame(list(MatchBO3s))
    df_matchBo5s = pd.DataFrame(list(MatchBO5s))
    df_players = pd.DataFrame(list(Players))
    df_playerMatchBo3 = pd.DataFrame(list(PlayerMatchBO3Connections))
    df_playerMatchBo5 = pd.DataFrame(list(PlayerMatchBO5Connections))
    df_playerTeam = pd.DataFrame(list(PlayerTeamConnections))
    
    # Merge matches with teams (Bo3 and Bo5)
    df_matchTeamsBo3 = df_matchBo3s.merge(df_teams, how='inner', left_on='team1_id', right_on='id', suffixes=('_team1', '_team2'))
    df_matchTeamsBo3 = df_matchTeamsBo3.merge(df_teams, how='inner', left_on='team2_id', right_on='id', suffixes=('_team1', '_team2'))
    df_matchTeamsBo5 = df_matchBo5s.merge(df_teams, how='inner', left_on='team1_id', right_on='id', suffixes=('_team1', '_team2'))
    df_matchTeamsBo5 = df_matchTeamsBo5.merge(df_teams, how='inner', left_on='team2_id', right_on='id', suffixes=('_team1', '_team2'))
    
    # Merge players with PlayerMatchConnection (Bo3 and Bo5)
    df_playerMatchBo3 = df_playerMatchBo3.merge(df_players, how='inner', left_on='player_id', right_on='id')
    df_playerMatchBo5 = df_playerMatchBo5.merge(df_players, how='inner', left_on='player_id', right_on='id')
    
    return df_matchTeamsBo3, df_matchTeamsBo5, df_playerMatchBo3, df_playerMatchBo5

def splitData(df_matchTeamsBo3, df_matchTeamsBo5, df_playerMatchBo3, df_playerMatchBo5):
    print("Splitting the data into features and labels")
    
    # Create target variable (who won the match)
    df_matchTeamsBo3['target'] = df_matchTeamsBo3.apply(
        lambda row: 1 if row['matchWinner_id'] == row['team1_id'] else 0, axis=1
    )
    df_matchTeamsBo5['target'] = df_matchTeamsBo5.apply(
        lambda row: 1 if row['matchWinner_id'] == row['team1_id'] else 0, axis=1
    )
    
    # Feature selection (pick relevant data for the model)
    x_bo3 = df_matchTeamsBo3[[
        'id',
        # Teams
        'team1_id',
        'team2_id',
        # Map Picks
        'mapPick1',
        'mapPick2',
        'mapPick3',
        # Rounds won
        'team1Map1RoundsWon',
        'team2Map1RoundsWon',
        'team1Map2RoundsWon',
        'team2Map2RoundsWon',
        'team1Map3RoundsWon',
        'team2Map3RoundsWon',
        # Map winners
        'map1Winner_id',
        'map2Winner_id',
        'map3Winner_id'
    ]]
    x_bo5 = df_matchTeamsBo5[[
        'id',
        # Teams
        'team1_id',
        'team2_id',
        # Map Picks
        'mapPick1',
        'mapPick2',
        'mapPick3',
        'mapPick4',
        'mapPick5',
        # Rounds Won
        'team1Map1RoundsWon',
        'team2Map1RoundsWon',
        'team1Map2RoundsWon',
        'team2Map2RoundsWon',
        'team1Map3RoundsWon',
        'team2Map3RoundsWon',
        'team1Map4RoundsWon',
        'team2Map4RoundsWon',
        'team1Map5RoundsWon',
        'team2Map5RoundsWon',
        # Map Winners
        'map1Winner_id',
        'map2Winner_id',
        'map3Winner_id',
        'map4Winner_id',
        'map5Winner_id'
    ]]
    
    # Aggregate player stats by match
    playerStatsAggBo3 = df_playerMatchBo3.groupby('match_id').agg({
        'rating': 'mean',
        'acs': 'mean',
        'kills': 'sum',
        'deaths': 'sum',
        'assists': 'sum',
        'kd': 'mean'
    })
    playerStatsAggBo5 = df_playerMatchBo5.groupby('match_id').agg({
        'rating': 'mean',
        'acs': 'mean',
        'kills': 'sum',
        'deaths': 'sum',
        'assists': 'sum',
        'kd': 'mean'
    })
    
    # Merge with match data
    x_bo3 = x_bo3.merge(playerStatsAggBo3, how='left', left_on='id', right_on='match_id')
    x_bo5 = x_bo5.merge(playerStatsAggBo5, how='left', left_on='id', right_on='match_id')

    # Remove 'id' (it isn't needed)
    x_bo3 = x_bo3.drop(columns=['id'])
    x_bo5 = x_bo5.drop(columns=['id'])
    
    # Define target variables
    y_bo3 = df_matchTeamsBo3['target']
    y_bo5 = df_matchTeamsBo5['target']
    
    # Split the data into training and testing sets
    x_TrainBo3, x_TestBo3, y_TrainBo3, y_TestBo3 = train_test_split(x_bo3, y_bo3, test_size=0.2, random_state=42, stratify=y_bo3)
    x_TrainBo5, x_TestBo5, y_TrainBo5, y_TestBo5 = train_test_split(x_bo5, y_bo5, test_size=0.2, random_state=42, stratify=y_bo5)
    
    return x_TrainBo3, x_TestBo3, y_TrainBo3, y_TestBo3, x_TrainBo5, x_TestBo5, y_TrainBo5, y_TestBo5

def trainModel(x_TrainBo3, y_TrainBo3, x_TrainBo5, y_TrainBo5):
    print("Training the models")
    
    labelEncoder = LabelEncoder()
    
    # Identify categorical columns
    categoricalColumnsBo3 = [
        'team1_id', 'team2_id',
        'mapPick1', 'mapPick2', 'mapPick3',
        'map1Winner_id', 'map2Winner_id', 'map3Winner_id'
    ]
    categoricalColumnsBo5 = [
        'team1_id', 'team2_id',
        'mapPick1', 'mapPick2', 'mapPick3', 'mapPick4', 'mapPick5',
        'map1Winner_id', 'map2Winner_id', 'map3Winner_id', 'map4Winner_id', 'map5Winner_id'
    ]
    
    # Apply label encoding for both Bo3 and Bo5
    for col in categoricalColumnsBo3:
        x_TrainBo3[col] = labelEncoder.fit_transform(x_TrainBo3[col])
    for col in categoricalColumnsBo5:
        x_TrainBo5[col] = labelEncoder.fit_transform(x_TrainBo5[col])
    
    # Create the full pipeline
    pipelineBo3 = Pipeline(steps=[
        ('classifier', LogisticRegression(max_iter=1000))
    ])
    pipelineBo5 = Pipeline(steps=[
        ('classifier', LogisticRegression(max_iter=1000))
    ])
    
    # Train the models
    modelBo3 = pipelineBo3.fit(x_TrainBo3, y_TrainBo3)
    modelBo5 = pipelineBo5.fit(x_TrainBo5, y_TrainBo5)
            
    return modelBo3, modelBo5

def evaluateModel(modelBo3, modelBo5, x_TestBo3, y_TestBo3, x_TestBo5, y_TestBo5):
    print("Evaluating models")
    
    # Predict and evaluate model performance on test data
    y_PredBo3 = modelBo3.predict(x_TestBo3)
    y_PredBo5 = modelBo5.predict(x_TestBo5)
    
    # Find accuracy
    accuracyBo3 = accuracy_score(y_TestBo3, y_PredBo3)
    accuracyBo5 = accuracy_score(y_TestBo5, y_PredBo5)
    
    print(f"Bo3 Model Accuracy: {accuracyBo3 * 100:.2f}%")
    print(f"Bo5 Model Accuracy: {accuracyBo5 * 100:.2f}%")
    
    return accuracyBo3, accuracyBo5

def saveModel(modelBo3, modelBo5):
    print("Saving trained models")
    
    # Save the models
    joblib.dump(modelBo3, 'valorantModelBo3.pkl')
    joblib.dump(modelBo5, 'valorantModelBo5.pkl')
    
    print("Models saved successfully")

def doModelStuff() -> bool:
    try:
        print("Starting the model stuff")
        
        # Clean up the data
        cleanData()
        
        # Move database to Pandas
        df_matchTeamsBo3, df_matchTeamsBo5, df_playerMatchBo3, df_playerMatchBo5 = moveDatabaseToPandas()
        
        # Split the data
        x_TrainBo3, x_TestBo3, y_TrainBo3, y_TestBo3, x_TrainBo5, x_TestBo5, y_TrainBo5, y_TestBo5 = splitData(
            df_matchTeamsBo3, df_matchTeamsBo5, df_playerMatchBo3, df_playerMatchBo5
        )
        
        # Train the model
        modelBo3, modelBo5 = trainModel(x_TrainBo3, y_TrainBo3, x_TrainBo5, y_TrainBo5)
        
        # Evaluate the model
        evaluateModel(modelBo3, modelBo5, x_TestBo3, y_TestBo3, x_TestBo5, y_TestBo5)
        
        # Save the model
        saveModel(modelBo3, modelBo5)
        
        print("Finished the model stuff")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False