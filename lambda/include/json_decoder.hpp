#ifndef AWS_LAMBDA_WORKER_JSON_DECODER_HPP
#define AWS_LAMBDA_WORKER_JSON_DECODER_HPP

#include <vector>
#include <cstdint>

#include <nlohmann/json.hpp>

#include "task_type.hpp"


struct DecodedJson
{
	TaskType type;
	std::vector<uint8_t> data;
};

nlohmann::json extract_body(const nlohmann::json& payload);
DecodedJson decode_json(const nlohmann::json& body);

#endif //AWS_LAMBDA_WORKER_JSON_DECODER_HPP
