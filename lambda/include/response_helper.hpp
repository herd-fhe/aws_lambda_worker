#ifndef AWS_LAMBDA_WORKER_RESPONSE_HELPER_HPP
#define AWS_LAMBDA_WORKER_RESPONSE_HELPER_HPP

#include <aws/lambda-runtime/runtime.h>


namespace response
{
	enum class ErrorStatus
	{
		INTERNAL,
		BAD_REQUEST
	};

	aws::lambda_runtime::invocation_response success(std::string_view response);
	aws::lambda_runtime::invocation_response error(std::string_view response, ErrorStatus status);
}

#endif //AWS_LAMBDA_WORKER_RESPONSE_HELPER_HPP
