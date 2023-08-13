import shutil
import json
import tempfile
import subprocess
import os
import uuid
import requests

from generated.worker_pb2 import MapTask, ReduceTask
from generated.common_pb2 import *


tools_dir = os.environ.get("TEST_HOME")
storage_dir = os.environ.get("STORAGE_BASE_DIR")
key_dir = os.environ.get("KEY_BASE_DIR")


def map_data_type_to_width(data_type: DataType):
    if data_type == UINT8 or data_type == INT8:
        return 8
    elif data_type == UINT16 or data_type == INT16:
        return 16
    elif data_type == UINT32 or data_type == INT32:
        return 32
    elif data_type == UINT64 or data_type == INT64:
        return 64

    assert False


def decrypt_data(temp_dir, session, output_data_frame, row_size, row_count):
    result = subprocess.run(
        [
            os.path.join(tools_dir, "dataframe_decryptor"),
            os.path.join(temp_dir, "key.pub"), os.path.join(temp_dir, "key"),
            os.path.join(storage_dir, session, output_data_frame), str(row_size), str(row_count)
        ], capture_output=True)
    return result.stdout.decode().split("\n")[:-1]


def reduce_task(address, task: ReduceTask, api_gateway_call=False):
    os.makedirs(os.path.join(storage_dir, task.session_uuid, task.output_data_frame_ptr.data_frame_uuid), exist_ok=True)

    data = task.SerializeToString()
    data = [val for val in data]
    body = {
        "type": "REDUCE",
        "data": data
    }

    if api_gateway_call:
        payload = {
            "body": json.dumps(body)
        }
        return requests.post(address, json=payload)
    else:
        return requests.post(address, json=body)


def map_task(address, task: MapTask, api_gateway_call=False):
    os.makedirs(os.path.join(storage_dir, task.session_uuid, task.output_data_frame_ptr.data_frame_uuid), exist_ok=True)

    data = task.SerializeToString()
    data = [val for val in data]
    body = {
        "type": "MAP",
        "data": data
    }

    if api_gateway_call:
        payload = {
            "body": json.dumps(body)
        }
        return requests.post(address, json=payload)
    else:
        return requests.post(address, json=body)


def random_uuid():
    return uuid.uuid4().urn[9:]


def generate_data_frame(crypto_tool, session, context, private_key, partition, rows):
    assert len(rows) != 0

    count = len(rows)
    width = len(rows[0])

    for row in rows:
        assert len(row) == width

    input_data = "\n".join(rows) + "\n"

    data_frame_uuid = uuid.uuid4().urn[9:]
    data_frame_dir = os.path.join(storage_dir, session, data_frame_uuid)
    os.makedirs(data_frame_dir, exist_ok=True)

    result = subprocess.run(
        [
            crypto_tool,
            "encrypt",
            "--context",
            context,
            "--key",
            private_key,
            "--data_out",
            os.path.join(data_frame_dir, str(partition)),
            "--width",
            str(width),
            "--count",
            str(count)
        ],
        input=input_data.encode(),
        capture_output=True)

    return data_frame_uuid


def decrypt_data_frame(crypto_tool, session, context, private_key, data_frame_uuid, partition, width, count):
    data_frame_dir = os.path.join(storage_dir, session, data_frame_uuid)

    result = subprocess.run(
        [
            crypto_tool,
            "decrypt",
            "--context",
            context,
            "--key",
            private_key,
            "--data_in",
            os.path.join(data_frame_dir, str(partition)),
            "--width",
            str(width),
            "--count",
            str(count)
        ], capture_output=True)

    return result.stdout.decode().split("\n")[:-1]
