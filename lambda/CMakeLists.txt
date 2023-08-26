cmake_minimum_required(VERSION 3.21)
project(
        aws_lambda_worker
        VERSION 0.1
        DESCRIPTION "herd executor worker"
        LANGUAGES CXX
)

#Libraries
find_package(aws-lambda-runtime REQUIRED)
set(JSON_BuildTests OFF CACHE INTERNAL "")
add_subdirectory(third-party/json)
add_subdirectory(worker)

#Main target
add_executable(aws_lambda_worker)

target_include_directories(aws_lambda_worker PRIVATE include)
target_link_libraries(
        aws_lambda_worker
        PUBLIC
        AWS::aws-lambda-runtime
        nlohmann_json::nlohmann_json
		spdlog::spdlog_header_only

		worker::base_runtime
)

target_sources(
        aws_lambda_worker
        PRIVATE
        src/main.cpp

        src/handler.cpp
        src/json_decoder.cpp
		src/lambda_config.cpp
		src/response_helper.cpp

        include/handler.hpp
        include/json_decoder.hpp
        include/task_type.hpp
		include/lambda_config.hpp
        include/exception.hpp
		include/response_helper.hpp
)


aws_lambda_package_target(aws_lambda_worker)