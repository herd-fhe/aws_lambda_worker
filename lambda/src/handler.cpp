#include "handler.hpp"

#include <spdlog/spdlog.h>

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

#include "exception.hpp"
#include "json_decoder.hpp"
#include "response_helper.hpp"


using namespace aws::lambda_runtime;

Handler::Handler(LambdaConfig lambda_config)
:	lambda_config_(std::move(lambda_config))
{
}

invocation_response Handler::operator()(const invocation_request& request)
{
	TaskDefinition decoded_json{};

	try
	{
		const auto json_payload = nlohmann::json::parse(request.payload);

		switch(lambda_config_.invoker_type)
		{
			using enum InvokerType;
			case API_CALL:
			{
				spdlog::info("Parsing API call");
				const auto json_body = extract_body(json_payload);
				decoded_json = decode_json(json_body);
				break;
			}
			case DIRECT:
			{
				spdlog::info("Parsing direct call");
				decoded_json = decode_json(json_payload);
				break;
			}
		}
	}
	catch (const nlohmann::json::exception& exception)
	{
		spdlog::error("Invalid task json");
		return response::error("Invalid json", response::ErrorStatus::BAD_REQUEST);
	}
	catch (const InvalidPayloadError& exception)
	{
		spdlog::error("Invalid payload: {}", exception.what());
		return response::error(exception.what(), response::ErrorStatus::BAD_REQUEST);
	}

	try
	{
		switch(decoded_json.type)
		{
			case TaskType::MAP:
				spdlog::info("Starting map task");
				map(decoded_json);
				break;
			case TaskType::REDUCE:
				spdlog::info("Starting reduce task");
				reduce(decoded_json);
				break;
			case TaskType::ECHO:
				spdlog::info("Starting echo task");
				break;
		}
	}
	catch(const std::runtime_error& exception)
	{
		spdlog::error("Error during task processing: {}", exception.what());
		return response::error(exception.what(), response::ErrorStatus::INTERNAL);
	}

	if(decoded_json.type == TaskType::ECHO)
	{
		spdlog::debug("Responding with echo: {}", request.payload);
		return response::success(request.payload);
	}
	else
	{
		spdlog::debug("Responding with success status");
		return response::success("Task completed!");
	}
}

void Handler::map(const TaskDefinition& payload)
{
	herd::proto::MapTask task;
	const auto& payload_data = payload.data;
	if(!task.ParseFromArray(payload_data.data(), static_cast<int>(payload_data.size())))
	{
		spdlog::error("Invalid protobuf message");
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
		spdlog::error("Decoding task data error");
		spdlog::error(error.what());
		throw;
	}

	auto executor = Executor();
	spdlog::info("Starting Map task");
	spdlog::info("Input data frame: {}:{}",
			input_data_frame_ptr.pointer.uuid.as_string(),
			input_data_frame_ptr.pointer.partition
	);

	spdlog::info("Output data frame: {}:{}",
			output_data_frame_ptr.uuid.as_string(),
			output_data_frame_ptr.partition
 	);

	try
	{
		executor.set_crypto(crypto::CryptoFactory::create_crypto(crypto_key_ptr, session_uuid, lambda_config_.base_config.key_base_dir));
		executor.add_input(data::load_input(input_data_frame_ptr, circuit.inputs[0], session_uuid, lambda_config_.base_config.storage_base_dir));
		executor.set_output(data::load_output(output_data_frame_ptr, circuit.output, session_uuid, lambda_config_.base_config.storage_base_dir));
	}
	catch(const herd::common::IOError& error)
	{
		spdlog::error(error.what());
		throw;
	}

	executor.set_circuit(std::move(circuit));

	spdlog::info("Loaded task requirements (input data frame, cloud key)");

	try
	{
		spdlog::debug("Executor map started");
		executor.map();
		spdlog::debug("Executor map completed");
	}
	catch(const ExecutorException& exception)
	{
		spdlog::error(exception.what());
		throw;
	}
}

void Handler::reduce(const TaskDefinition& payload)
{
	herd::proto::ReduceTask task;
	const auto& payload_data = payload.data;
	if(!task.ParseFromArray(payload_data.data(), static_cast<int>(payload_data.size())))
	{
		spdlog::error("Invalid protobuf message");
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
		spdlog::error("Decoding task data error");
		spdlog::error(error.what());
		throw;
	}

	auto executor = Executor();

	spdlog::info("Starting Reduce task");
	spdlog::info("Input data frames count: {}", input_data_frame_ptrs.size());
	for(const auto& input_data_frame_ptr: input_data_frame_ptrs)
	{
        spdlog::info("Input data frame: {}:{}",
			input_data_frame_ptr.pointer.uuid.as_string(),
			input_data_frame_ptr.pointer.partition
        );
	}
	spdlog::info("Output data frame: {}:{}",
			output_data_frame_ptr.uuid.as_string(),
			output_data_frame_ptr.partition
	);

	try
	{
		executor.set_crypto(crypto::CryptoFactory::create_crypto(crypto_key_ptr, session_uuid, lambda_config_.base_config.key_base_dir));
		for(std::size_t i = 0; i < input_data_frame_ptrs.size(); ++i)
		{
			executor.add_input(data::load_input(input_data_frame_ptrs[i], circuit.inputs[0], session_uuid, lambda_config_.base_config.storage_base_dir));
		}
		executor.set_output(data::load_output(output_data_frame_ptr, circuit.output, session_uuid, lambda_config_.base_config.storage_base_dir));
	}
	catch(const herd::common::IOError& error)
	{
		spdlog::error(error.what());
		throw;
	}

	executor.set_circuit(std::move(circuit));

	spdlog::info("Loaded task requirements (input data frame, cloud key)");

	try
	{
		spdlog::debug("Executor reduce started");
		executor.reduce();
		spdlog::debug("Executor reduce completed");
	}
	catch(const ExecutorException& exception)
	{
		spdlog::error(exception.what());
		throw;
	}
}
