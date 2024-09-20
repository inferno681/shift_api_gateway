from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class _SettingsModel(BaseSettings):
    """Базовые настройки."""

    @classmethod
    def from_yaml(cls, config_path: str) -> '_SettingsModel':
        return cls(
            **yaml.safe_load(Path(config_path).read_text(encoding='utf-8')),
        )

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix='EMP_',
        env_nested_delimiter='__',
    )

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        """Определяем приоритет использования переменных."""
        return init_settings, env_settings, file_secret_settings


class _ServiceSettings(_SettingsModel):
    """Валидация настроек сервиса из файла YAML."""

    title: str
    description: str
    host: str
    port: int
    debug: bool
    tags_metadata_health: dict[str, str]


class _AuthSettings(_SettingsModel):
    """Валидация настроек настроек сервиса авторизации."""

    base_url: str
    tags_metadata: dict[str, str]


class _TransactionSettings(_SettingsModel):
    """Валидация настроек настроек сервиса транзакций."""

    base_url: str
    tags_metadata: dict[str, str]


class Settings(_SettingsModel):
    """Настройки сервиса."""

    service: _ServiceSettings
    auth_service: _AuthSettings
    transaction_service: _TransactionSettings


config = Settings.from_yaml('./src/config/config.yaml')
