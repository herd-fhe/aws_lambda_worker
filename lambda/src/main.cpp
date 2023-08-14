#include <aws/lambda-runtime/runtime.h>
#include <aws/logging/logging.h>

#include <aws/core/Aws.h>
#include <aws/core/utils/logging/ConsoleLogSystem.h>
#include <aws/core/utils/logging/LogMacros.h>

#include "lambda_config.hpp"
#include "handler.hpp"


using namespace aws::lambda_runtime;

std::function<std::shared_ptr<Aws::Utils::Logging::LogSystemInterface>()> get_console_logger_factory(Aws::Utils::Logging::LogLevel level)
{
	return [level] {
		return Aws::MakeShared<Aws::Utils::Logging::ConsoleLogSystem>(
				"console_logger", level);
	};
}

int main()
{
	LambdaConfig lambda_config = load_lambda_config();
	aws::logging::log_info(("Storage directory: " + lambda_config.base_config.storage_base_dir.string()).c_str(), "INFO");
	aws::logging::log_info(("Keys directory: " + lambda_config.base_config.key_base_dir.string()).c_str(), "INFO");

	Aws::SDKOptions options;

	const auto log_level = map_log_level(lambda_config.log_level);
	options.loggingOptions.logLevel = log_level;
	options.loggingOptions.logger_create_fn = get_console_logger_factory(log_level);

	Aws::InitAPI(options);

	Handler handler(lambda_config);
	AWS_LOGSTREAM_INFO("worker", "Handler initialized. Serving...");
	AWS_LOGSTREAM_FLUSH();

	run_handler(handler);

	Aws::ShutdownAPI(options);

	return 0;
}