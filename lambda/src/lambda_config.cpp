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

	return lambda_config;
}
