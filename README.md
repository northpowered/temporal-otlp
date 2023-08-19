# Temporal-OTLP-example

> Still under development

Grafana stack deployment in production mode with Temporal microservices as small load generators


## How does it works?

![](img/schema.svg)



## Deployment

```bash
docker-compose -f docker-compose.base.yml up  # Network, load balancer, S3 storage, grafana
docker-compose -f docker-compose.metrics.yml up  # Mimir in read-write mode
docker-compose -f docker-compose.logs.yml up  # Loki
docker-compose -f docker-compose.tracing.yml up  # Tempo
docker-compose -f docker-compose.temporal.yml up  # Temporal
docker-compose -f docker-compose.agents.yml up  # VictoriaMetrics agents, promtail, OTEL collectors
./build.sh  # Services (DEV) building and deployment
./build_prod.sh  # Services (PROD) building and deployment
```

### Usage
```bash
poetry shell
poetry install --no-root
python3 starter.py # Dev svc
python3 starter_prod.py # Prod svc
```

## Service graph

![sg](img/good_sg.png)
