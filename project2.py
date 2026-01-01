# 1. Import required modules: requests, smtplib, email, schedule, time
import requests
import smtplib
import schedule
import time
from email.message import EmailMessage

# 2. Define your OpenWeatherMap API key (use placeholder for security)
api_key = 'Enter Your Api_Key'

# 3. Define email credentials: sender, app password, recipient, SMTP server
sender = 'Enter Your Email'
app_password = 'Enter Your App Password'
recipient = 'Enter Recipient Email'
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# 4. Create a list of Egyptian cities to monitor
cities = ['Cairo', 'Alexandria', 'Giza', 'Shubra El-Kheima', 'Port Said']

# 5. Create a function to fetch current weather data for a city using OpenWeather API
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed
    return response.json()

# 6. Extract temperature (in Celsius) from the API response
def get_temperature(city):
    data = fetch_weather_data(city)
    return data['main']['temp']

# 7. Create a function to check if temperature exceeds 40°C
def check_temperature(city):
    temp = get_temperature(city)
    return temp > 40

# 8. Create a function to send weather alert email
def send_email_alert(city):
    temp = get_temperature(city)
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient  # ← Fixed: was "resiver"
    msg['Subject'] = 'High Temperature Alert'
    msg.set_content(f"The temperature in {city} has reached {temp}°C, which is dangerously high!")

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, app_password)
        server.send_message(msg)
    print(f"Alert sent for {city}")

# 9. Create main job function: loop through cities, check temp, send alert if needed
def main_job():
    print(f"Checking weather at {time.strftime('%Y-%m-%d %H:%M')}")
    for city in cities:
        try:
            if check_temperature(city):
                send_email_alert(city)
            else:
                print(f"The temperature in {city} is normal.")
        except Exception as e:
            print(f"Error checking {city}: {e}")

# 10. Schedule the job to run every 6 hours
schedule.every(6).hours.do(main_job)

# 11. Run the scheduler and keep the script alive
if __name__ == "__main__":
    # Run once at start
    main_job()
    # Then run on schedule
    while True:
        schedule.run_pending()
        time.sleep(60)