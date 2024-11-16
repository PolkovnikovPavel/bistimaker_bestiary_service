from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import app.api.api_v1 as api_v1
import app.api.api_debug as api_debug
from app.api.including_ligging import init_loger

# Создаем основное приложение FastAPI
app = FastAPI(root_path='/bestiaries-service/api',
              docs_url=None,
              redoc_url=None,
              )
logger = init_loger(app, 'main', is_statistics=False)


@app.on_event("startup")
async def startup_event():
    logger.warning('=================================')
    logger.warning("Приложение запущено!")
    logger.warning('=================================\n\n')
    # Здесь можно выполнить какие-то действия, например, подключение к базе данных


@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("Приложение остановлено!\n\n")
    # Здесь можно выполнить какие-то действия, например, закрытие соединения с базой данных


# Включаем маршруты
app.mount("/v1", api_v1.app_v1)
app.mount("/debug", api_debug.app_debug)
