from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests

AZURE_ML_URL = "http://7454dda5-a2e7-4655-aac9-509ff1b69bdf.westeurope.azurecontainer.io/score"
AZURE_API_KEY = "JwdYDRkxboFElALUsKmD0jWVhvghfjGk"

def predict_home(request):
    return render(request, 'app/predict.html')

class PlayerPredictionView(View):
    def post(self, request):
        try:
            team = request.POST.get('team')
            position = request.POST.get('position')
            age = float(request.POST.get('age'))
            goals = float(request.POST.get('goals'))
            assists = float(request.POST.get('assists'))
            yellow_cards = float(request.POST.get('yellow_cards'))
            second_yellow_cards = float(request.POST.get('second_yellow_cards'))
            red_cards = float(request.POST.get('red_cards'))
            goals_conceded = float(request.POST.get('goals_conceded'))
            clean_sheets = float(request.POST.get('clean_sheets'))
            minutes_played = float(request.POST.get('minutes_played'))
            days_injured = float(request.POST.get('days_injured'))
            games_injured = float(request.POST.get('games_injured'))
            award = request.POST.get('award')
            highest_value = float(request.POST.get('highest_value'))
            position_encoded = int(request.POST.get('position_encoded'))
            winger = request.POST.get('winger')

            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {AZURE_API_KEY}'}
            data = {
                "Inputs": {
                    "input1": [
                        {
                            "team": team,
                            "position": position,
                            "age": age,
                            "goals": goals,
                            "assists": assists,
                            "yellow_cards": yellow_cards,
                            "second_yellow_cards": second_yellow_cards,
                            "red_cards": red_cards,
                            "goals_conceded": goals_conceded,
                            "clean_sheets": clean_sheets,
                            "minutes_played": minutes_played,
                            "days_injured": days_injured,
                            "games_injured": games_injured,
                            "award": award,
                            "highest_value": highest_value,
                            "position_encoded": position_encoded,
                            "winger": winger
                        }
                    ]
                }
            }

            response = requests.post(AZURE_ML_URL, json=data, headers=headers)
            prediction = response.json().get("Results", {}).get("output1", [{}])[0].get("Scored Labels", "N/A")

            return render(request, 'app/predict.html', {"predicted_price": prediction})

        except Exception as e:
            return render(request, 'app/predict.html', {"error": str(e)})
