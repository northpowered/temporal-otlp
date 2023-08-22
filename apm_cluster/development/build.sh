export DOCKER_BUILDKIT=1 
export COMPOSE_DOCKER_CLI_BUILD=1
chmod -R 777 dynamicconfig
docker-compose -f docker-compose.services-dev.yml up --build