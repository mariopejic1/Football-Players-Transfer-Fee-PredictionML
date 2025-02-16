from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests, json

AZURE_ML_URL = "http://7454dda5-a2e7-4655-aac9-509ff1b69bdf.westeurope.azurecontainer.io/score"
AZURE_API_KEY = "JwdYDRkxboFElALUsKmD0jWVhvghfjGk"

def predict_home(request):
    return render(request, 'app/predict.html')

class PlayerPredictionView(View):
    def post(self, request):
            team = request.POST.get('team')
            position = request.POST.get('position')
            age = request.POST.get('age')
            appearance = request.POST.get('appearance')
            goals = request.POST.get('goals')
            assists = request.POST.get('assists')
            yellow_cards = request.POST.get('yellow cards')  
            second_yellow_cards = request.POST.get('second yellow cards')
            red_cards = request.POST.get('red cards')  
            goals_conceded = request.POST.get('goals conceded')  
            clean_sheets = request.POST.get('clean sheets')  
            minutes_played = request.POST.get('minutes played')  
            days_injured = request.POST.get('days_injured')
            games_injured = request.POST.get('games_injured')
            award = request.POST.get('award')
            highest_value = request.POST.get('highest_value')
            position_encoded = request.POST.get('position_encoded')
            winger = request.POST.get('winger')

            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {AZURE_API_KEY}'}
            data = {
                "Inputs": {
                    "input1": [
                        {
                            "team": team,
                            "position": position,
                            "age": age,
                            "appearance": appearance,  
                            "goals": goals,
                            "assists": assists,
                            "yellow cards": yellow_cards, 
                            "second yellow cards": second_yellow_cards,  
                            "red cards": red_cards,  
                            "goals conceded": goals_conceded,  
                            "clean sheets": clean_sheets,  
                            "minutes played": minutes_played,  
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
      
            if response.status_code == 200:
                result = response.content.decode('utf-8')
                json_obj = json.loads(result)

                print("API Response:", json_obj)  

                try:
                    prediction = json_obj['Results']['WebServiceOutput0'][0]['Scored Labels']
                    return render(request, 'app/predict.html', {"predicted_price": prediction})
                except KeyError as e:
                    return render(request, 'app/predict.html', {}) 
            else:
                return render(request, 'app/predict.html', {})

