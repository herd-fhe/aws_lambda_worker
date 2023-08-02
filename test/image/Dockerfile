FROM debian:bookworm-slim

RUN apt update\
    && apt install -y curl unzip

RUN curl -L https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie -o aws-lambda-rie\
    && chmod +x aws-lambda-rie

COPY build/aws_lambda_worker.zip .
RUN unzip aws_lambda_worker.zip -d lambda

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]
