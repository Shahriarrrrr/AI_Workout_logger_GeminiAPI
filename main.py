import requests
import datetime
import google.generativeai as genai
import os

GOOGLE_API_KEY = os.getenv("Gemini_API_key")
NUTRONIX_ID = "c3210aad"
NUTRONIX_KEY = os.getenv("Nutronix_apikey")
GENDER = "male"
WEIGHT_KG = 88
HEIGHT_CM = 14.986
AGE = 24
SHEET_PROJECT_NAME = "Workout Tracking"
SHEET_USERNAME = "Shahriar Khan"
SHEET_NAME = "sheet1"
SHEETY_ENDPOINT = "https://api.sheety.co/f9e277e0740db956afdbb9ca3df18b30/workoutTracking/sheet1"
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Which exercise did you do?")
model = genai.GenerativeModel("gemini-1.5-flash")


headers = {
    "x-app-id": NUTRONIX_ID,
    "x-app-key": NUTRONIX_KEY
}

parameters_nut = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response= requests.post(url=exercise_endpoint,json=parameters_nut,headers=headers)
result = response.json()
# result = {'exercises': [{'tag_id': 100, 'user_input': 'walked', 'duration_min': 1999.95, 'met': 3.5, 'nf_calories': 10266.41, 'photo': {'highres': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/100_highres.jpg', 'thumb': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/100_thumb.jpg', 'is_user_uploaded': False}, 'compendium_code': 17190, 'name': 'walking', 'description': None, 'benefits': None}, {'tag_id': 63, 'user_input': 'swam', 'duration_min': 4399.88, 'met': 6, 'nf_calories': 38718.94, 'photo': {'highres': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise//63_highres.jpg', 'thumb': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise//63_thumb.jpg', 'is_user_uploaded': False}, 'compendium_code': 18310, 'name': 'swimming', 'description': None, 'benefits': None}]}




#Collective data
for exercise in result["exercises"]:
    print(exercise)
    exercise_date = datetime.date.today().strftime("%Y-%m-%d")
    now_time = datetime.datetime.now()
    exercise_time = now_time.strftime(("%H:%M:%S"))
    exercise_duration = exercise["duration_min"]
    exercise_name = exercise["user_input"]
    exercise_calories_burnt = exercise['nf_calories']
    gemini_response = model.generate_content(f"Write a 1 sentence motivative comment on my {exercise_text} and {exercise_calories_burnt}.")
    comment = gemini_response.text
    # SHEETY REQUEST
    sheety_params = {
        f"{SHEET_NAME}": {
            "date": f"{exercise_date}",
            "time": f"{exercise_time}",
            "exercise": f"{exercise_name.title()}",
            "duration": f"{exercise_duration}",
            "calories": f"{exercise_calories_burnt}",
            "comments" : f"{comment}"

        }
    }
    sheety_response = requests.post(url="https://api.sheety.co/f9e277e0740db956afdbb9ca3df18b30/workoutTracking/sheet1",
                                    json=sheety_params)
    print(sheety_response.text)




