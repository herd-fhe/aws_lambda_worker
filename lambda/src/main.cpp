#include <aws/lambda-runtime/runtime.h>
#include <aws/logging/logging.h>

#include "base_runtime/util/config_loader.hpp"

#include "handler.hpp"


using namespace aws::lambda_runtime;

int main()
{
  Config config = load_config();
  aws::logging::log_info(("Storage directory: " + config.storage_base_dir.string()).c_str(), "INFO");
  aws::logging::log_info(("Keys directory: " + config.key_base_dir.string()).c_str(), "INFO");

  Handler handler(config);

  run_handler(handler);
  return 0;
}