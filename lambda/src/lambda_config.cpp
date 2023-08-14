#include "lambda_config.hpp"

#include <cstring>

#include <base_runtime/util/config_loader.hpp>


LambdaConfig load_lambda_config()
{
	LambdaConfig lambda_config{};
	lambda_config.base_config = load_config();

	lambda_config.invoker_type = InvokerType::DIRECT;

	if(const char* invoker = std::getenv("INVOKER"))
	{
		if (strcmp(invoker, "API_CALL") == 0)
		{
			lambda_config.invoker_type = InvokerType::API_CALL;
		}
		else if(strcmp(invoker, "DIRECT") != 0)
		{
			throw std::runtime_error("Invalid invoker type");
		}
	}

	lambda_config.log_level = LogLevel::NONE;
	if(const char* log_level = std::getenv("LOG_LEVEL"))
	{
		if(strcmp(log_level, "INFO") == 0)
		{
			lambda_config.log_level = LogLevel::INFO;
		}
		else if(strcmp(log_level, "WARNING") == 0)
		{
			lambda_config.log_level = LogLevel::WARNING;
		}
		else if(strcmp(log_level, "ERROR") == 0)
		{
			lambda_config.log_level = LogLevel::ERROR;
		}
		else if(strcmp(log_level, "DEBUG") == 0)
		{
			lambda_config.log_level = LogLevel::DEBUG;
		}
		else if(strcmp(log_level, "TRACE") == 0)
		{
			lambda_config.log_level = LogLevel::TRACE;
		}
		else if(strcmp(log_level, "NONE") != 0)
		{
			throw std::runtime_error("Invalid log level");
		}
	}
	return lambda_config;
}

Aws::Utils::Logging::LogLevel map_log_level(LogLevel level)
{
	switch(level)
	{
		using enum LogLevel;
		case NONE:
			return Aws::Utils::Logging::LogLevel::Off;
		case INFO:
			return Aws::Utils::Logging::LogLevel::Info;
		case WARNING:
			return Aws::Utils::Logging::LogLevel::Warn;
		case ERROR:
			return Aws::Utils::Logging::LogLevel::Error;
		case DEBUG:
			return Aws::Utils::Logging::LogLevel::Debug;
		case TRACE:
			return Aws::Utils::Logging::LogLevel::Trace;
	}

	return Aws::Utils::Logging::LogLevel::Off;
}
