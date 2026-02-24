import os
import requests
from twilio.rest import  Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = os.environ.get("OPEN_OWM_API_KEY")
account_sid = "AC8ca630870f598d7dadf9943f1558ea0b"
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": -21.176630,
    "lon": -47.820839,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_Endpoint, params= weather_params)
response.raise_for_status()

# print(f"Status code: {response.status_code}")
data = response.json()
need_umbrella = False
for hour in data["list"]:
    if int(hour["weather"][0]["id"]) < 700:
        need_umbrella = True

if need_umbrella:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        from_= 'whatsapp:+14155238886',
        to='whatsapp:+19515501344',
        body="It's going to rain today. Remember to bring an ☂️"
    )
    print(message.status)
