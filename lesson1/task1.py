# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

user_name = 'jkamalt'
url = f'https://api.github.com/users/{user_name}/repos'

# Запрос на получение списка репозиториев заданного пользователя
response = requests.get(url)

# Запись результата в файл
with open('repos.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f)
