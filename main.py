import requests
from datetime import datetime
import smtplib
import time

MY_LAT = "YOUR LATITUDE"
MY_LONG = "YOUR LONGITUDE"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1][: 2])
sunset = int(data["results"]["sunset"].split("T")[1][: 2])


def is_dark():
    if current_time > sunset or current_time < sunrise:
        return True


time_now = datetime.now().hour
current_time = time_now
# time = str(time_now.time())[:2]
# current_time = int(time) - 5

# If the ISS is close to my current position
min_lat = int(MY_LAT) - 5
max_lat = int(MY_LAT) + 5

min_long = int(MY_LONG) - 5
max_long = int(MY_LONG) + 5
while True:
    time.sleep(60)
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
    # if int(iss_latitude) in range(min_lat, max_lat) and int(iss_longitude) in range(min_long, max_long):
        print("pass")
        if is_dark():
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user="example@xyz.com", password="password")
                connection.sendmail(
                    from_addr="example@xyz.com",
                    to_addrs="to_mail_id",
                    msg="subject: Look up \n\n Look up in the sky the ISS is flying over your head...!"
                )
            print("***")
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
