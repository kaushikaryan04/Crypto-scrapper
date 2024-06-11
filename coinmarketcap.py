import requests

class CoinMarketCap:
    def __init__(self) :
        self.baseUrl = "http://localhost:8000/api/taskmanager/start_scraping/"

    def start_scrapping(self, coins) :
        payload = {
            "coins": coins
        }
        url = self.baseUrl + "/start_scraping"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  # Assuming the response contains the job_id
        else:
            return {"error": response.text}


    def get_response(self, job_id) :

        url = self.baseUrl + "scraping_status/" + job_id

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
