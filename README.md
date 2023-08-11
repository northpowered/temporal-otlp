# Temporal-OTLP-example

> Still under development

Grafana stack deployment in production mode with Temporal microservices as small load generators


## How does it works?

![](img/schema.svg)



## Deployment

```bash
docker-compose -f docker-compose.base.yml up  # Network, load balancer, S3 storage, grafana
docker-compose -f docker-compose.metrics.yml up  # Prometheus with Mimir
docker-compose -f docker-compose.logs.yml up  # Loki
docker-compose -f docker-compose.tracing.yml up  # Tempo
docker-compose -f docker-compose.temporal.yml up  # Temporal
./build.sh  # Services building and deployment
```

### Usage
```bash
poetry shell
poetry install --no-root
python3 starter.py
```

## Service graph

![sg](img/good_sg.png)
