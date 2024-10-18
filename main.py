from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import app.api.api_v1 as api_v1
import app.api.api_debug as api_debug

# Создаем основное приложение FastAPI
app = FastAPI(root_path='/bestiaries-service/api',
              docs_url=None,
              redoc_url=None,
              )

# Включаем маршруты
app.mount("/v1", api_v1.app_v1)
app.mount("/debug", api_debug.app_debug)
