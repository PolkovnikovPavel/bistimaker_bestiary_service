import redis

# Подключаемся к Redis, запущенному в контейнере
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Устанавливаем значение
redis_client.set('mykey', 'Hello, Redis!')

# Получаем значение
value = redis_client.get('mykey')
print(value.decode('utf-8'))  # Вывод: Hello, Redis!

redis_client.delete('mykey')
new_value = redis_client.get('mykey')
print(new_value)


all_keys = redis_client.keys('*')

# Вывод всех ключей
for key in all_keys:
    print(key.decode('utf-8'))


