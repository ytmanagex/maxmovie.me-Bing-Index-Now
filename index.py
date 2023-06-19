import requests
import csv
import json
import os
import datetime

url = "https://www.bing.com/indexnow"

payload = {
    "host": "maxmovie.me",
    "key": "e2e437d2898a4be08d2edf2538614a45",
    "keyLocation": "https://maxmovie.me/e2e437d2898a4be08d2edf2538614a45.txt",
    "urlList": []
}

headers = {
    "Content-Type": "application/json; charset=utf-8"
}

# Read URLs from CSV file
with open("urls.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        payload["urlList"].append(row[0])  # Assuming the URLs are in the first column of the CSV

# Counter logic
counter_file = "counter.txt"

# Check if the counter file exists
if not os.path.exists(counter_file):
    # If it doesn't exist, initialize with a value of 0
    with open(counter_file, "w") as file:
        file.write("0")

# Read current counter value from the file
with open(counter_file, "r") as file:
    counter = int(file.read())

# Increment the counter
counter += 1

# Write the new counter value to the file
with open(counter_file, "w") as file:
    file.write(str(counter))

# Execute a URL based on the counter value
url_index = (counter - 1) % len(payload["urlList"])  # Calculate the index of the URL to execute

try:
    url_to_execute = payload["urlList"][url_index]

    # Send POST request for the selected URL
    payload["urlList"] = [url_to_execute]
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print response status code and URL
    print(f"URL: {url_to_execute}")
    print(f"Status Code: {response.status_code}")

    # Logging
    log_file = "log.txt"
    current_datetime = datetime.datetime.now()

    # Write log to the file
    with open(log_file, "a") as file:
        file.write(f"{current_datetime} - URL: {url_to_execute} - Status: {response.status_code}\n")

except IndexError:
    print("All URLs in the CSV file have been processed.")

# Display the current counter value
print("The script has been executed", counter, "times")
