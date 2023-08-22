.DEFAULT_GOAL = help

LB_MANIFEST=apm_cluster/docker-compose.lb.yml
LOCALS3_MANIFEST=apm_cluster/docker-compose.locals3.yml
GRAFANA_MANIFEST=apm_cluster/docker-compose.grafana.yml
ALERTMANAGER_MANIFEST=apm_cluster/docker-compose.alertmanager.yml
METRICS_MANIFEST=apm_cluster/docker-compose.metrics.yml
LOGS_MANIFEST=apm_cluster/docker-compose.logs.yml
TRACING_MANIFEST=apm_cluster/docker-compose.tracing.yml
METAMONITORING_MANIFEST=apm_cluster/docker-compose.metaagents.yml

# Dev svc manifests
TEMPORAL_MANIFEST=apm_cluster/development/docker-compose.temporal.yml
SVC_DEV_MANIFEST=apm_cluster/development/docker-compose.services-dev.yml
SVC_PROD_MANIFEST=apm_cluster/development/docker-compose.services-prod.yml
SVC_AGENTS_MANIFEST=apm_cluster/development/docker-compose.agents.yml

CLUSTER_CONFIG=apm_cluster/cluster.config

TEMPORAL_CONFIG=apm_cluster/development/temporal.config


include ${CLUSTER_CONFIG}

include ${TEMPORAL_CONFIG}

# Build test svc
export DOCKER_BUILDKIT=true
export COMPOSE_DOCKER_CLI_BUILD=true

export


---------------------------------------------> : ## *Docker network deployment**
create_network: ## Create a network for cluster
	@docker network create	--attachable \
								${NETWORK_NAME}


drop_network: ## Drop a network for cluster
	@docker network rm ${NETWORK_NAME}

recreate_network: drop_network create_network ## ReCreate a network for cluster


---------------------------------------------> : ## **Load balancer deployment**

create_lb: ## Create lb
	@docker-compose --file ${LB_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_lb: ## Drop lb
	@docker-compose --file ${LB_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_lb: drop_lb create_lb ## ReCreate lb

logs_lb: ## Show logs of lb
	@docker-compose --file ${LB_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow

---------------------------------------------> : ## **MinIO svc for local development**

create_local_s3: ## Create MinIO cluster
	@docker-compose --file ${LOCALS3_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_local_s3: ## Drop MinIO cluster
	@docker-compose --file ${LOCALS3_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_local_s3: drop_local_s3 create_local_s3 ## ReCreate MinIO cluster

logs_local_s3: ## Show logs of MinIO cluster
	@docker-compose --file ${LOCALS3_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow

---------------------------------------------> : ## **Grafana development**

create_grafana: ## Create grafana
	@docker-compose --file ${GRAFANA_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_grafana: ## Drop grafana
	@docker-compose --file ${GRAFANA_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_grafana: drop_grafana create_grafana ## ReCreate grafana

logs_grafana: ## Show logs of grafana
	@docker-compose --file ${GRAFANA_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow

---------------------------------------------> : ## **Alertmanager development**

create_alertmanager: ## Create alertmanager
	@docker-compose --file ${ALERTMANAGER_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_alertmanager: ## Drop alertmanager
	@docker-compose --file ${ALERTMANAGER_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_alertmanager: drop_alertmanager create_alertmanager ## ReCreate alertmanager

logs_alertmanager: ## Show logs of alertmanager
	@docker-compose --file ${ALERTMANAGER_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow
---------------------------------------------> : ## **Mimir cluster in read/write deployment mode**

create_metrics_cluster: ## Create Mimir cluster
	@docker-compose --file ${METRICS_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_metrics_cluster: ## Drop Mimir cluster
	@docker-compose --file ${METRICS_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_metrics_cluster: drop_metrics_cluster create_metrics_cluster ## ReCreate Mimir cluster

logs_metrics_cluster: ## Show logs of Mimir cluster
	@docker-compose --file ${METRICS_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow
---------------------------------------------> : ## **Loki cluster in read/write deployment mode**

create_logging_cluster: ## Create Loki cluster
	@docker-compose --file ${LOGS_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_logging_cluster: ## Drop Loki cluster
	@docker-compose --file ${LOGS_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_logging_cluster: drop_logging_cluster create_logging_cluster ## ReCreate Loki cluster

logs_logging_cluster: ## Show logs of Loki cluster
	@docker-compose --file ${LOGS_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow

---------------------------------------------> : ## **Tempo cluster in read/write deployment mode**

create_tracing_cluster: ## Create Tempo cluster
	@docker-compose --file ${TRACING_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_tracing_cluster: ## Drop Tempo cluster
	@docker-compose --file ${TRACING_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_tracing_cluster: drop_tracing_cluster create_tracing_cluster ## ReCreate Tempo cluster

logs_tracing_cluster: ## Show logs of Tempo cluster
	@docker-compose --file ${TRACING_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow
---------------------------------------------> : ## **Metamonitoring agents deployment**

create_metamon_cluster: ## Create Meta agents
	@docker-compose --file ${METAMONITORING_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_metamon_cluster: ## Drop Meta agents
	@docker-compose --file ${METAMONITORING_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						down

recreate_metamon_cluster: drop_metamon_cluster create_metamon_cluster ## ReCreate Meta agents

logs_metamon_cluster: ## Show logs of Meta agents
	@docker-compose --file ${METAMONITORING_MANIFEST} \
					--env-file ${CLUSTER_CONFIG} \
						logs \
							--follow


---------------------------------------------> : ## **Temporal deployment**

create_temporal_cluster: ## Create Temporal
	@docker-compose --file ${TEMPORAL_MANIFEST} \
					--env-file ${TEMPORAL_CONFIG} \
						up \
							--detach \
							--force-recreate

drop_temporal_cluster: ## Drop Temporal
	@docker-compose --file ${TEMPORAL_MANIFEST} \
					--env-file ${TEMPORAL_CONFIG} \
						down

recreate_temporal_cluster: drop_temporal_cluster create_temporal_cluster ## ReCreate Temporal

logs_temporal_cluster: ## Show logs of Temporal
	@docker-compose --file ${TEMPORAL_MANIFEST} \
					--env-file ${TEMPORAL_CONFIG} \
						logs \
							--follow


---------------------------------------------> : ## **SVC_DEV deployment**

create_svc_dev: ## Create svc_dev
	@docker-compose --file ${SVC_DEV_MANIFEST} \
						up \
							--detach \
							--force-recreate\
							--build

drop_svc_dev: ## Drop svc_dev
	@docker-compose --file ${SVC_DEV_MANIFEST} \
						down

recreate_svc_dev: drop_svc_dev create_svc_dev ## ReCreate svc_dev

logs_svc_dev: ## Show logs of svc_dev
	@docker-compose --file ${SVC_DEV_MANIFEST} \
						logs \
							--follow

---------------------------------------------> : ## **SVC_PROD deployment**

create_svc_prod: ## Create svc_prod
	@docker-compose --file ${SVC_PROD_MANIFEST} \
						up \
							--detach \
							--force-recreate

drop_svc_prod: ## Drop svc_prod
	@docker-compose --file ${SVC_PROD_MANIFEST} \
						down

recreate_svc_prod: drop_svc_prod create_svc_prod ## ReCreate svc_prod

logs_svc_prod: ## Show logs of svc_prod
	@docker-compose --file ${SVC_PROD_MANIFEST} \
						logs \
							--follow \
							--build


---------------------------------------------> : ## **SVC_AGENTS deployment**

create_svc_agents: ## Create svc_agents
	@docker-compose --file ${SVC_AGENTS_MANIFEST} \
						up \
							--detach \
							--force-recreate

drop_svc_agents: ## Drop svc_agents
	@docker-compose --file ${SVC_AGENTS_MANIFEST} \
						down

recreate_svc_agents: drop_svc_agents create_svc_agents ## ReCreate svc_agents

logs_svc_agents: ## Show logs of svc_agents
	@docker-compose --file ${SVC_AGENTS_MANIFEST} \
						logs \
							--follow
---------------------------------------------> : ## **Cluster deployment**
create_all: create_network create_local_s3 create_grafana create_alertmanager create_metrics_cluster create_logging_cluster create_tracing_cluster create_metamon_cluster create_lb ## Deploy all part of cluster
	
drop_all: drop_metamon_cluster drop_grafana drop_alertmanager drop_metrics_cluster drop_logging_cluster drop_tracing_cluster drop_local_s3 drop_lb drop_network ## Drop all part of cluster

---------------------------------------------> : ## **System commands**
prune_system: ## Prune docker system
	@docker system prune --force

help: ## Show help
	@awk 	'BEGIN {FS = ":.*?## "} \
			/^[a-z A-Z0-9\[\]\<\>_-]+:.*?## / \
			{printf "  \033[36m%-47s\033[0m %s\n", $$1, $$2}' \
				$(MAKEFILE_LIST)
