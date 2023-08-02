#!/bin/sh

export LAMBDA_TASK_ROOT=/lambda
export _HANDLER=""

exec ./aws-lambda-rie lambda/bootstrap