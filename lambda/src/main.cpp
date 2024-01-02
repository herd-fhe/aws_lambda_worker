#include <aws/lambda-runtime/runtime.h>

#include <spdlog/cfg/env.h>

#include "handler.hpp"
#include "lambda_config.hpp"


using namespace aws::lambda_runtime;

int main()
{
	spdlog::cfg::load_env_levels();

	spdlog::info("Configuration loading...");
	const LambdaConfig lambda_config = load_lambda_config();
	spdlog::info("Storage directory: {}", lambda_config.base_config.storage_base_dir.string());
	spdlog::info("Keys directory: {}", lambda_config.base_config.key_base_dir.string());
	spdlog::info("API mode: {}", lambda_config.invoker_type == InvokerType::DIRECT ? "DIRECT" : "API_CALL");

	Handler handler(lambda_config);

	run_handler(handler);
	return 0;
}