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

DecodedJson decode_json(const nlohmann::json& payload);

#endif //AWS_LAMBDA_WORKER_JSON_DECODER_HPP
