from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import app.api.api_v1 as api_v1
import app.api.api_debug as api_debug

# Создаем основное приложение FastAPI
app = FastAPI(title='Бестиарии')

# Включаем маршруты
app.mount("/bestiaries-service/api/v1", api_v1.app_v1)
app.mount("/bestiaries-service/api/debug", api_debug.app_debug)
