#include "handler.hpp"

#include "aws/logging/logging.h"

#include "herd/common/model/worker/crypto_key_ptr.hpp"
#include "herd/common/model/worker/data_frame_ptr.hpp"
#include "herd/common/model/exception.hpp"

#include "herd/mapper/worker.hpp"

#include "base_runtime/executor/executor.hpp"
#include "base_runtime/crypto/crypto_factory.hpp"
#include "base_runtime/data_frame/data_frame.hpp"
#include "base_runtime/executor/runnable_circuit.hpp"
#include "base_runtime/mapper/circuit.hpp"
#include "base_runtime/executor/exception.hpp"

#include "worker.pb.h"

#include "json_decoder.hpp"
#include "exception.hpp"


using namespace aws::lambda_runtime;

Handler::Handler(LambdaConfig lambda_config)
:	lambda_config_(std::move(lambda_config))
{
}

invocation_response Handler::operator()(const invocation_request& request)
{
	DecodedJson decoded_json{};

	try
	{
		const auto json_payload = nlohmann::json::parse(request.payload);

		switch(lambda_config_.invoker_type)
		{
			using enum InvokerType;
			case API_CALL:
			{
				const auto json_body = extract_body(json_payload);
				decoded_json = decode_json(json_body);
				break;
			}
			case DIRECT:
			{
				decoded_json = decode_json(json_payload);
				break;
			}
		}
	}
	catch (const nlohmann::json::exception& exception)
	{
		return invocation_response::failure("Invalid json", "RUNTIME");
	}
	catch (const InvalidPayloadError& exception)
	{
		return invocation_response::failure(exception.what(), "RUNTIME");
	}

	try
	{
		switch(decoded_json.type)
		{
			case TaskType::MAP:
				map(decoded_json);
				break;
			case TaskType::REDUCE:
				reduce(decoded_json);
				break;
			case TaskType::ECHO:
				break;
		}
	}
	catch(const std::runtime_error& exception)
	{
		return invocation_response::failure(exception.what(), "EXECUTOR");
	}

	if(decoded_json.type == TaskType::ECHO)
	{
		return invocation_response::success(request.payload, "text/plain");
	}
	else
	{
		return invocation_response::success("SUCCESS", "text/plain");
	}
}

void Handler::map(const DecodedJson& payload)
{
	herd::proto::MapTask task;
	const auto& payload_data = payload.data;
	if(!task.ParseFromArray(payload_data.data(), static_cast<int>(payload_data.size())))
	{
		throw InvalidPayloadError("Invalid protobuf payload");
	};

	herd::common::CryptoKeyPtr crypto_key_ptr{};
	herd::common::InputDataFramePtr input_data_frame_ptr{};
	herd::common::DataFramePtr output_data_frame_ptr{};
	herd::common::UUID session_uuid{};
	RunnableCircuit circuit{};

	try
	{
		crypto_key_ptr = herd::mapper::to_model(task.crypto_key_ptr());
		input_data_frame_ptr = herd::mapper::to_model(task.input_data_frame_ptr());
		output_data_frame_ptr = herd::mapper::to_model(task.output_data_frame_ptr());
		session_uuid = herd::common::UUID(task.session_uuid());
		circuit = mapper::to_model(task.circuit());
	}
	catch(const std::runtime_error& error)
	{
		aws::logging::log_error(error.what(), "MAP");
		throw;
	}

	auto executor = Executor();
	aws::logging::log_info("Starting Map task", "MAP");
	aws::logging::log_info(
			("Input data frame: "+ input_data_frame_ptr.pointer.uuid.as_string() + ":" + std::to_string(input_data_frame_ptr.pointer.partition)).c_str(),
			"MAP"
	);

	aws::logging::log_info(
			("Output data frame: " + output_data_frame_ptr.uuid.as_string() + ":" + std::to_string(output_data_frame_ptr.partition)).c_str(),
			"MAP"
 	);

	try
	{
		executor.set_crypto(crypto::CryptoFactory::create_crypto(crypto_key_ptr, session_uuid, lambda_config_.base_config.key_base_dir));
		executor.add_input(data::load_input(input_data_frame_ptr, circuit.inputs[0], session_uuid, lambda_config_.base_config.storage_base_dir));
		executor.set_output(data::load_output(output_data_frame_ptr, circuit.output, session_uuid, lambda_config_.base_config.storage_base_dir));
	}
	catch(const herd::common::IOError& error)
	{
		aws::logging::log_error(error.what(), "MAP");
		throw;
	}

	executor.set_circuit(std::move(circuit));

	aws::logging::log_info("Loaded task requirements (input data frame, cloud key)", "MAP");

	try
	{
		executor.map();
	}
	catch(const ExecutorException& exception)
	{
		aws::logging::log_error(exception.what(), "MAP");
		throw;
	}
}

void Handler::reduce(const DecodedJson& payload)
{
	herd::proto::ReduceTask task;
	const auto& payload_data = payload.data;
	if(!task.ParseFromArray(payload_data.data(), static_cast<int>(payload_data.size())))
	{
		throw InvalidPayloadError("Invalid protobuf payload");
	}

	herd::common::CryptoKeyPtr crypto_key_ptr{};
	std::vector<herd::common::InputDataFramePtr> input_data_frame_ptrs{};
	herd::common::DataFramePtr output_data_frame_ptr{};
	herd::common::UUID session_uuid{};
	RunnableCircuit circuit{};

	try
	{
		crypto_key_ptr = herd::mapper::to_model(task.crypto_key_ptr());

		input_data_frame_ptrs.reserve(static_cast<std::size_t>(task.input_data_frame_ptrs_size()));
		for(const auto& input_data_frame_ptr_proto: task.input_data_frame_ptrs())
		{
			input_data_frame_ptrs.emplace_back(herd::mapper::to_model(input_data_frame_ptr_proto));
		}

		output_data_frame_ptr = herd::mapper::to_model(task.output_data_frame_ptr());
		session_uuid = herd::common::UUID(task.session_uuid());
		circuit = mapper::to_model(task.circuit());
	}
	catch(const std::runtime_error& error)
	{
		aws::logging::log_error(error.what(), "REDUCE");
		throw;
	}

	auto executor = Executor();

	aws::logging::log_info("Starting Reduce task", "REDUCE");
	aws::logging::log_info(
			("Output data frame: " + output_data_frame_ptr.uuid.as_string() + ":" + std::to_string(output_data_frame_ptr.partition)).c_str(),
			"REDUCE"
	);

	try
	{
		executor.set_crypto(crypto::CryptoFactory::create_crypto(crypto_key_ptr, session_uuid, lambda_config_.base_config.key_base_dir));
		for(std::size_t i = 0; i < input_data_frame_ptrs.size(); ++i)
		{
			executor.add_input(data::load_input(input_data_frame_ptrs[i], circuit.inputs[i], session_uuid, lambda_config_.base_config.storage_base_dir));
		}
		executor.set_output(data::load_output(output_data_frame_ptr, circuit.output, session_uuid, lambda_config_.base_config.storage_base_dir));
	}
	catch(const herd::common::IOError& error)
	{
		aws::logging::log_error(error.what(), "REDUCE");
		throw;
	}

	executor.set_circuit(std::move(circuit));

	aws::logging::log_info("Loaded task requirements (input data frame, cloud key)", "MAP");

	try
	{
		executor.reduce();
	}
	catch(const ExecutorException& exception)
	{
		aws::logging::log_error(exception.what(), "REDUCE");
		throw;
	}
}
