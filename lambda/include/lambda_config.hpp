#ifndef AWS_LAMBDA_WORKER_LAMBDA_CONFIG_HPP
#define AWS_LAMBDA_WORKER_LAMBDA_CONFIG_HPP

#include "base_runtime/config.hpp"
#include <aws/core/utils/logging/LogLevel.h>

enum class LogLevel
{
	NONE,
	INFO,
	WARNING,
	ERROR,
	DEBUG,
	TRACE
};

enum class InvokerType
{
	DIRECT,
	API_CALL
};

struct LambdaConfig
{
	Config base_config;
	InvokerType invoker_type;

	LogLevel log_level;
};

LambdaConfig load_lambda_config();

Aws::Utils::Logging::LogLevel map_log_level(LogLevel level);

#endif //AWS_LAMBDA_WORKER_LAMBDA_CONFIG_HPP
