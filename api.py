from contextlib import asynccontextmanager

import fastapi
import fastapi.staticfiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

import configuration
import operations.seeders

rabbitmq_config = configuration.Config().rabbitmq

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s - %(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": "logs/error.log",
        },
        "access": {
            "formatter": "access",
            "class": "logging.FileHandler",
            "filename": "logs/access.log",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}


@asynccontextmanager
async def startup_shutdown_lifespan(app: fastapi.FastAPI):
    operations.seeders.seed_default_user()
    connection = operations.messages.get_connection()
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_config.queue_names.generate_processing, durable=True)
    channel.queue_declare(queue=rabbitmq_config.queue_names.model_processing, durable=True)
    yield
    channel.close()
    connection.close()

cors_config = configuration.CorsSettings()
app = fastapi.FastAPI(docs_url='/api/docs', redoc_url='/api/redoc', lifespan=startup_shutdown_lifespan)
app.add_middleware(CORSMiddleware, allow_origins=cors_config.origins, allow_headers=cors_config.headers, allow_methods=cors_config.methods)

# app.include_router(routers.roles.roles_router, prefix='/api/roles')
# app.include_router(routers.users.users_router, prefix='/api/users')

app.mount('/api/media', fastapi.staticfiles.StaticFiles(directory=configuration.MEDIA_PATH))

if __name__ == '__main__':
    uvicorn.run("api:app", workers=1, port=8001, host='0.0.0.0', log_config=logging_config)
