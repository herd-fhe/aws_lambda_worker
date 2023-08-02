#include "json_decoder.hpp"

#include "exception.hpp"


namespace
{
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
		else
		{
			throw InvalidPayloadError("Invalid task type!");
		}
	}
}

DecodedJson decode_json(const nlohmann::json& payload)
{
	DecodedJson decoded_json{};

	try
	{
		if(!payload.contains(TYPE_KEY))
		{
			throw InvalidPayloadError("No type!");
		}

		{
			const auto json_type = payload.at(TYPE_KEY).get<std::string>();
			decoded_json.type = map_type(json_type);
		}

		if(!payload.contains(DATA_KEY))
		{
			throw InvalidPayloadError("No data!");
		}

		const auto& data = payload.at(DATA_KEY);

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
