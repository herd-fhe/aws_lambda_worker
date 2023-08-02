#ifndef AWS_LAMBDA_WORKER_HANDLER_HPP
#define AWS_LAMBDA_WORKER_HANDLER_HPP

#include <aws/lambda-runtime/runtime.h>

#include "base_runtime/config.hpp"
#include "json_decoder.hpp"


class Handler
{
public:
	explicit Handler(Config config);

	aws::lambda_runtime::invocation_response operator()(const aws::lambda_runtime::invocation_request& request);

	void map(const DecodedJson& payload);
	void reduce(const DecodedJson& payload);

private:
	Config config_;
};

#endif // AWS_LAMBDA_WORKER_HANDLER_HPP
