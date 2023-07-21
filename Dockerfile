# syntax = edrevo/dockerfile-plus

INCLUDE+ Dockerfile.base

ARG SRV_LETTER

ENV SERVICE_LETTER=${SRV_LETTER}

COPY ./src/service_${SRV_LETTER} .

CMD [ "python3", "separate_run.py"]