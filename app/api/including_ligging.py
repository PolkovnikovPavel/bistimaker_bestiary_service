import logging.handlers
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


def init_loger(app, name, is_statistics=True):
    class ErrorLoggingMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            start_time = time.time()
            client_ip = request.client.host
            method = request.method
            url = request.url.path
            query_params = dict(request.query_params)

            try:
                response = await call_next(request)
            except Exception as e:
                logger.error('=================================')
                logger.error(f"Exception occurred: {e}", exc_info=True)
                logger.error('=================================\n')
                raise e
            finally:
                process_time = time.time() - start_time
                logger.info(
                    f"Request completed: IP={client_ip}, ProcessTime={process_time:.4f}s, Method={method}, StatusCode={response.status_code}, URL={url}, QueryParams={query_params}\n")

            return response

    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Формат сообщения
        handlers=[
            # Файловый обработчик
            logging.handlers.RotatingFileHandler("app/logs/bestiary_service.log", maxBytes=100*1024, backupCount=5, encoding='utf-8'),
            logging.StreamHandler()  # Обработчик для вывода в консоль (опционально)
        ]
    )
    logger = logging.getLogger(name)

    # Создание нового обработчика для сообщений уровня WARNING и выше
    warning_handler = logging.handlers.RotatingFileHandler("app/logs/bestiary_service_errors.log", maxBytes=100 * 1024,
                                                           backupCount=5, encoding='utf-8')
    warning_handler.setLevel(logging.WARNING)  # Установка уровня логирования для этого обработчика

    warning_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    warning_handler.setFormatter(warning_formatter)

    # Добавление нового обработчика к логгеру
    logger.addHandler(warning_handler)

    if is_statistics:
        app.add_middleware(ErrorLoggingMiddleware)
    return logger



