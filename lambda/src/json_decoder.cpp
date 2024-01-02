#include "json_decoder.hpp"

#include "exception.hpp"


namespace
{
	constexpr const char* const BODY_KEY = "body";
	constexpr const char* const TYPE_KEY = "type";
	constexpr const char* const DATA_KEY = "data";

	TaskType map_type(std::string_view type_str)
	{
		if(type_str == "MAP")
		{
			return TaskType::MAP;
		}
		else if(type_str == "REDUCE")
		{
			return TaskType::REDUCE;
		}
		else if(type_str == "ECHO")
		{
			return TaskType::ECHO;
		}
		else
		{
			throw InvalidPayloadError("Invalid task type!");
		}
	}
}

nlohmann::json extract_body(const nlohmann::json& payload)
{
	if(!payload.contains(BODY_KEY))
	{
		throw InvalidPayloadError("No body!");
	}

	const auto& body = payload.at(BODY_KEY);

	if(!body.is_string())
	{
		throw InvalidPayloadError("Body is not a string!");
	}

	return nlohmann::json::parse(body.get<std::string>());
}

TaskDefinition decode_json(const nlohmann::json& body)
{
	TaskDefinition decoded_json{};

	try
	{
		if(!body.contains(TYPE_KEY))
		{
			throw InvalidPayloadError("No type!");
		}

		{
			const auto json_type = body.at(TYPE_KEY).get<std::string>();
			decoded_json.type = map_type(json_type);
		}

		if(decoded_json.type == TaskType::ECHO)
		{
			return decoded_json;
		}

		if(!body.contains(DATA_KEY))
		{
			throw InvalidPayloadError("No data!");
		}

		const auto& data = body.at(DATA_KEY);

		if(!data.is_array())
		{
			throw InvalidPayloadError("Data is not an array!");
		}

		decoded_json.data.resize(data.size());

		for(std::size_t i = 0; i < data.size(); ++i)
		{
			if(!data[i].is_number_unsigned())
			{
				throw InvalidPayloadError("Data must be an array of uint8 numbers!");
			}
			const auto value = data[i].get<uint8_t>();
			decoded_json.data[i] = value;
		}

		return decoded_json;
	}
	catch(const nlohmann::json::exception& exception)
	{
		throw InvalidPayloadError(exception.what());
	}
}
