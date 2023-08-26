#include <aws/lambda-runtime/runtime.h>
#include <aws/logging/logging.h>

#include <spdlog/cfg/env.h>

#include "handler.hpp"
#include "lambda_config.hpp"


using namespace aws::lambda_runtime;

int main()
{
	spdlog::cfg::load_env_levels();

	LambdaConfig lambda_config = load_lambda_config();
	aws::logging::log_info(("Storage directory: " + lambda_config.base_config.storage_base_dir.string()).c_str(), "INFO");
	aws::logging::log_info(("Keys directory: " + lambda_config.base_config.key_base_dir.string()).c_str(), "INFO");

	Handler handler(lambda_config);

	run_handler(handler);
	return 0;
}