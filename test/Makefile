OUT_DIR = src/generated/
SRC_DIR = ../lambda/worker/proto/src/

WORKER_PROTOS = worker circuit common node
WORKER_PROTOS_GRPC_FULL_PATH = $(addsuffix _pb2_grpc.py, $(addprefix $(OUT_DIR), $(WORKER_PROTOS)))
WORKER_PROTOS_FULL_PATH = $(addsuffix _pb2.py, $(addprefix $(OUT_DIR), $(WORKER_PROTOS)))

all: $(WORKER_PROTOS_FULL_PATH) $(WORKER_PROTOS_FULL_PATH)
	sed -i -E "s/^import.*_pb2/from . \\0/" src/generated/*.py
	@echo "Generated"

$(OUT_DIR)%_pb2.py $(OUT_DIR)%_pb2_grpc.py: $(SRC_DIR)%.proto
	python3 -m grpc_tools.protoc -I $(SRC_DIR) --python_out=$(OUT_DIR) --pyi_out=$(OUT_DIR) --grpc_python_out=$(OUT_DIR) $<

.PHONY: all