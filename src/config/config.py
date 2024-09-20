from pathlib import Path

import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class _SettingsModel(BaseSettings):
    """Base settings."""

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
        """Variables priority."""
        return init_settings, env_settings, file_secret_settings


class _ServiceSettings(_SettingsModel):
    """Service settings validation."""

    title: str
    description: str
    host: str
    port: int
    debug: bool
    tags_metadata_health: dict[str, str]


class _AuthSettings(_SettingsModel):
    """Auth service settings validation."""

    base_url: str
    tags_metadata: dict[str, str]


class _TransactionSettings(_SettingsModel):
    """Transaction service setting validation."""

    base_url: str
    tags_metadata: dict[str, str]


class _JaegerSettings(_SettingsModel):
    """Jaeger settings validation."""

    service_name: str
    host: str
    port: int
    logging: bool
    sampler_type: str
    sampler_param: float | int


class Settings(_SettingsModel):
    """Service settings."""

    service: _ServiceSettings
    auth_service: _AuthSettings
    transaction_service: _TransactionSettings
    jaeger: _JaegerSettings


config = Settings.from_yaml('./src/config/config.yaml')
