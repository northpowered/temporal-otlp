import os


SERVICE_LETTER: str = os.getenv("SERVICE_LETTER", "A")

PROMETHEUS_PORT: str = os.getenv("PROMETHEUS_PORT", "5001")

TEMPORAL_ENDPOINT: str = os.getenv("TEMPORAL_ENDPOINT", "localhost:7233")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")

LOG_JSON: bool = os.getenv("LOG_JSON", True)

JAEGER_HOST: str = os.getenv("JAEGER_HOST", "localhost")

JAEGER_PORT: int = int(os.getenv("JAEGER_PORT", "6831"))

TEMPO_ENDPOINT: str = os.getenv("TEMPO_ENDPOINT", "http://127.0.0.1:4317")

APP_MODE: str = os.getenv("APP_MODE", "local")