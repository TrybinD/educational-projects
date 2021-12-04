import requests

token = '1e1bb4b71e1bb4b71e1bb4b7d11e6e7a3a11e1b1e1bb4b741edb3cc17e4eb88438a3d76'


response = requests.get('https://api.vk.com/method/wall.get',
                        params={
                            'access_token': token,
                            'v': '5.126',
                            'domain': 'boyz_haiku',
                            'offset': 1801,
                            'count': 100
                        })
#Здесь мы смотрим что есть после парсинга в прямом эфире
# for i in response.json()['response']['items']:
#     print(i['text'])
#     print('****')

#Пишем хоку в файл

with open('Непрактичные проекты/haiku_corpus_dirt.txt', 'a', encoding='utf-8') as file:
    for i in response.json()['response']['items']:
        file.write(i['text'])
        file.write('\n***\n')