import requests
import datetime as dt
import os
Ntr_API_ID = os.environ.get("NRT_API_ID")
Ntr_API_Key = os.environ.get("NRT_API_KEY")
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")
GENDER = "male"
WEIGHT_KG = "your weight"
HEIGHT_CM = "Your height"
AGE = "age"

headers = {
    "x-app-id": Ntr_API_ID,
    "x-app-key": Ntr_API_Key,
}
params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
from requests.auth import HTTPBasicAuth
basic = HTTPBasicAuth(os.environ.get("auth_user_name"), os.environ.get("auth_user_pass"))
response = requests.post(exercise_endpoint,json=params, headers=headers)
nrt_data = response.json()
today_date = dt.datetime.now().strftime("%d/%m/%Y")
now_time = dt.datetime.now().strftime("%X")
sheet_endpoint = os.environ.get("sheet_endpoint")
for exercise in nrt_data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, auth=basic)

    print(sheet_response.text)
