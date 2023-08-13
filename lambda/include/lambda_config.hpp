#ifndef AWS_LAMBDA_WORKER_LAMBDA_CONFIG_HPP
#define AWS_LAMBDA_WORKER_LAMBDA_CONFIG_HPP

#include "base_runtime/config.hpp"


enum class InvokerType
{
	DIRECT,
	API_CALL
};

struct LambdaConfig
{
	Config base_config;
	InvokerType invoker_type;
};

LambdaConfig load_lambda_config();

#endif //AWS_LAMBDA_WORKER_LAMBDA_CONFIG_HPP
