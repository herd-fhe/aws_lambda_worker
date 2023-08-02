#ifndef AWS_LAMBDA_WORKER_EXCEPTION_HPP
#define AWS_LAMBDA_WORKER_EXCEPTION_HPP

#include <stdexcept>


struct InvalidPayloadError: public std::runtime_error
{
	using std::runtime_error::runtime_error;
};

#endif //AWS_LAMBDA_WORKER_EXCEPTION_HPP
