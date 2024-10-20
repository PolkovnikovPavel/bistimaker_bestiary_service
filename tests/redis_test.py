import redis

# Подключаемся к Redis, запущенному в контейнере
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Устанавливаем значение
redis_client.set('mykey', 'Hello, Redis!')

# Получаем значение
value = redis_client.get('mykey')
print(value.decode('utf-8'))  # Вывод: Hello, Redis!
