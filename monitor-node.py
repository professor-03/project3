import requests
import time
import smtplib
from email.mime.text import MIMEText

# Monitoring Configuration
NODE_URL = 'http://localhost:8545'
CHECK_INTERVAL = 300  # Every 5 minutes

# Email Configuration
SMTP_SERVER = 'divyamgouda114@gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'divyamgouda114@gmail.com'
EMAIL_PASSWORD = '12345678'  # Consider using environment variables
ALERT_RECIPIENT = 'divyamgouda24@gmail.com'

def send_alert():
    msg = MIMEText('Alert: Your blockchain node is down!')
    msg['Subject'] = 'Blockchain Node Alert'
    msg['From'] =  divyamgouda114@gmail.com
    msg['To'] = divyamgouda24@gmail.com

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send alert email: {e}")

def check_node():
    try:
        response = requests.post(NODE_URL, json={
            "jsonrpc": "2.0",
            "method": "web3_clientVersion",
            "params": [],
            "id": 1
        }, timeout=10)
        if response.status_code == 200:
            print("Node is up and running.")
        else:
            print(f"Unexpected status code: {response.status_code}")
            send_alert()
    except requests.exceptions.RequestException as e:
        print(f"Node is down: {e}")
        send_alert()

if __name__ == "__main__":
    while True:
        check_node()
        time.sleep(CHECK_INTERVAL)
