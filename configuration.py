"""Configuration module"""
import dataclasses

import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib
from pydantic import BaseModel, model_validator
from typing import Optional, List, Any

_module_path = pathlib.Path(__file__).resolve()
ROOT_PATH = _module_path.parent
MEDIA_PATH = ROOT_PATH / 'media'
MEDIA_PATH.mkdir(exist_ok=True)
IMAGES_PATH = MEDIA_PATH / 'images'
IMAGES_PATH.mkdir(exist_ok=True)

_ENV_FILES_PATHS = (
    pathlib.Path(f"{ROOT_PATH}/.env.template"),
    pathlib.Path(f"{ROOT_PATH}/.env"),
)

AVATAR_IMAGE_FORMAT = 'jpeg'

@dataclasses.dataclass
class QueueNames:
    model_processing: str = 'process.models.normal'
    generate_processing: str = 'process.generate.normal'


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILES_PATHS,
        validate_default=True,
        case_sensitive=False,
        env_nested_delimiter='_',
        extra='ignore',
    )


class SqliteConfig(BaseModel):
    """SQLite configuration"""

    filename: Optional[str] = None

    @property
    def connection_string(self) -> str:
        """Get connection string"""
        return f"sqlite:///{self.filename if self.filename else ':memory:'}"

    @property
    def is_in_memory(self) -> bool:
        """Check if sqlite is running in memory"""
        return not self.filename


class CorsSettings(CustomBaseSettings):
    """CORSMiddleware settings"""

    origins: List[str]
    methods: List[str]
    headers: List[str]


class PostgresConfig(BaseModel):
    """PostgreSQL configuration"""

    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None

    @property
    def connection_string(self) -> str:
        """Get connection string"""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def are_all_fields_populated(self):
        """Check if all fields are populated"""
        return self.host and self.port and self.user and self.password and self.database


class RabbitMQ(CustomBaseSettings):
    """RabbitMQ configuration"""
    host: str = pydantic.Field(alias='RABBITMQ_HOST', default='localhost')
    username: str = pydantic.Field(alias='RABBITMQ_DEFAULT_USER')
    password: str = pydantic.Field(alias='RABBITMQ_DEFAULT_PASS')
    queue_names: QueueNames = pydantic.Field(default_factory=QueueNames)


class Amazon(CustomBaseSettings):
    """Amazon"""
    access_key_id: str = pydantic.Field(alias='AWS_ACCESS_KEY_ID')
    secret_access_key: str = pydantic.Field(alias='AWS_SECRET_ACCESS_KEY')
    s3_bucket: str = pydantic.Field(alias='AWS_S3_BUCKET')


class Config(CustomBaseSettings):
    """Base configurations"""

    context: str
    api_url: str
    database: str
    log_queries: bool = False
    sqlite: SqliteConfig
    postgres: PostgresConfig
    rabbitmq: RabbitMQ
    aws: Amazon

    @property
    def connection_string(self):
        if self.database == 'postgres':
            return self.postgres.connection_string
        return self.sqlite.connection_string

    @model_validator(mode="after")
    def validate_db_configuration(self):
        if self.database == 'postgres' and not self.postgres.are_all_fields_populated:
            raise ValueError("You have selected postgres as database but did not provide its configuration")
        return self


class DefaultUser(CustomBaseSettings):
    first_name: str
    last_name: str
    email: str
    phone_number: int
    password: str


class JWT(CustomBaseSettings):
    key: str = pydantic.Field(alias='JWT_KEY')
    algorithm: str = pydantic.Field(alias='JWT_ALGORITHM')
    # pixity_api_key: str = pydantic.Field(alias='PIXITY_API_KEY')


# class CeleryTasksConfig(CustomBaseSettings):
#     tasks: list[str] = pydantic.Field(alias='CELERY_TASKS')
#     rabbitmq_host: str = pydantic.Field(alias='RABBITMQ_HOST', default='localhost')
#     rabbitmq_username: str = pydantic.Field(alias='RABBITMQ_DEFAULT_USER')
#     rabbitmq_password: str = pydantic.Field(alias='RABBITMQ_DEFAULT_PASS')
#
#     @property
#     def get_tasks(self):
#         return list(set([_[:_.rfind('.')] for _ in self.tasks]))
#
#     @property
#     def get_schedule(self):
#         _beat_schedule = {}
#         for task in self.tasks:
#             task_path, task_schedule, _ = task.split("/")
#             _beat_schedule[task_path.split(".")[-1]] = {
#                 "task": task_path,
#                 "schedule": int(task_schedule),
#             }
#         return _beat_schedule
#
#     @property
#     def get_tasks_rate_limits(self):
#         _rate_limits = {}
#         for task in self.tasks:
#             task_path, _, rate_limit = task.split("/")
#             _rate_limits[task_path] = {'rate_limit': f'{rate_limit}/s'}
#         return _rate_limits
#
#     @property
#     def get_broker_url(self):
#         return (
#             f"pyamqp://{self.rabbitmq_username}:{self.rabbitmq_password}@{self.rabbitmq_host}:5672//"
#         )
