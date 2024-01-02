#include "response_helper.hpp"


#include "spdlog/spdlog.h"

#include <nlohmann/json.hpp>

namespace response
{
	constexpr const char* const CONTENT_TYPE = "application/json";

	namespace
	{
		int map_error_status_to_code(ErrorStatus status)
		{
			switch(status)
			{
				case ErrorStatus::INTERNAL:
					return 500;
				case ErrorStatus::BAD_REQUEST:
					return 400;
			}

			return 500;
		}

		std::string map_error_status_to_code_description(ErrorStatus status)
		{
			switch(status)
			{
				case ErrorStatus::INTERNAL:
					return "500 Internal Server Error";
				case ErrorStatus::BAD_REQUEST:
					return "400 Bad Request";
			}
			return "500 Internal Server Error";
		}
	}

	aws::lambda_runtime::invocation_response success(std::string_view response)
	{
		nlohmann::json body;
		body["status"] = "SUCCESS";
		body["message"] = response;

		nlohmann::json payload;
		payload["isBase64Encoded"] = false;
		payload["statusCode"] = 200;
		payload["statusDescription"] = "200 OK";
		payload["headers"]["Content-Type"] = "application/json";
		payload["body"] = body.dump();

		spdlog::debug("Responding with success (200): {}", payload.dump().c_str());
		return aws::lambda_runtime::invocation_response::success(payload.dump(), CONTENT_TYPE);
	}

	aws::lambda_runtime::invocation_response error(std::string_view response, ErrorStatus status)
	{
		nlohmann::json body;
		body["status"] = "ERROR";
		body["message"] = response;

		nlohmann::json payload;
		payload["isBase64Encoded"] = false;
		payload["statusCode"] = map_error_status_to_code(status);
		payload["statusDescription"] = map_error_status_to_code_description(status);
		payload["headers"]["Content-Type"] = "application/json";
		payload["body"] = body.dump();

		spdlog::debug("Responding with error ({}): {}", map_error_status_to_code(status), payload.dump().c_str());
		return aws::lambda_runtime::invocation_response::success(payload.dump(), CONTENT_TYPE);	}
}