export DOCKER_BUILDKIT=1 
export COMPOSE_DOCKER_CLI_BUILD=1
chmod -R 777 grafana_data
chmod -R 777 dynamicconfig
chmod -R 777 prometheus
chmod -R 777 prometheus_data
chmod -R 777 loki
docker-compose -f docker-compose.services.yml up --build