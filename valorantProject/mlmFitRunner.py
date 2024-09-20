import requests

print("1. RandomForestClassifier")
print("2. LogisticRegression")
print("3. SVC")
print("4. GradientBoostingClassifier")
print("5. KNeighborsClassifier")
print("6. XGBClassifier")
whichModel = int(input("Which model do you want to use: "))

if whichModel == 1:
    whichModel = "RandomForestClassifier".lower()
elif whichModel == 2:
    whichModel = "LogisticRegression".lower()
elif whichModel == 3:
    whichModel = "SVC".lower()
elif whichModel == 4:
    whichModel = "GradientBoostingClassifier".lower()
elif whichModel == 5:
    whichModel = "KNeighborsClassifier".lower()
elif whichModel == 6:
    whichModel = "XGBClassifier".lower()

r = requests.get(f"http://localhost:8000/mlm/fit?model={whichModel}")

print(r.text)