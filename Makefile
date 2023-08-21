.DEFAULT_GOAL = help

LB_MANIFEST=apm_cluster/docker-compose.lb.yml
LOCALS3_MANIFEST=apm_cluster/docker-compose.locals3.yml
GRAFANA_MANIFEST=apm_cluster/docker-compose.grafana.yml
ALERTMANAGER_MANIFEST=apm_cluster/docker-compose.alertmanager.yml
METRICS_MANIFEST=apm_cluster/docker-compose.metrics.yml
LOGS_MANIFEST=apm_cluster/docker-compose.logs.yml
TRACING_MANIFEST=apm_cluster/docker-compose.tracing.yml

CLUSTER_CONFIG=apm_cluster/cluster.config

include ${CLUSTER_CONFIG}

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
---------------------------------------------> : ## **Cluster deployment**
create_all: create_network create_local_s3 create_grafana create_alertmanager create_metrics_cluster create_logging_cluster create_lb ## Deploy all part of cluster
	
drop_all: drop_local_s3 drop_grafana drop_alertmanager drop_metrics_cluster drop_logging_cluster drop_lb drop_network ## Drop all part of cluster

---------------------------------------------> : ## **System commands**
prune_system: ## Prune docker system
	@docker system prune --force

help: ## Show help
	@awk 	'BEGIN {FS = ":.*?## "} \
			/^[a-z A-Z0-9\[\]\<\>_-]+:.*?## / \
			{printf "  \033[36m%-47s\033[0m %s\n", $$1, $$2}' \
				$(MAKEFILE_LIST)
