# syntax = edrevo/dockerfile-plus

INCLUDE+ Dockerfile.base

COPY ./src/service_${SRV_LETTER} .

CMD [ "python3", "separate_run.py"]