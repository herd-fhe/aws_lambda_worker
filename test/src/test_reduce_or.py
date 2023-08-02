from typing import Tuple

import pytest

from generated.worker_pb2 import DataFramePtr, CryptoKeyPtr, InputDataFramePtr, ReduceTask
from generated.circuit_pb2 import Circuit, OutputColumn, InputStructure
from generated.node_pb2 import InputNode, OutputNode, Node, OperationNode, OR
from generated.common_pb2 import *

from worker import generate_data_frame, random_uuid, decrypt_data_frame, reduce_task


def test_reduce_or(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 3
    input_data = [
        '01111101',
        '01111101',
        '00111101',
        '00011101',
        '00001101'
    ]
    data_frame = generate_data_frame(crypto_tool, session, context, private_key, partition, input_data)

    task = ReduceTask(
        session_uuid=session,
        input_data_frame_ptrs=[
            InputDataFramePtr(
                pointer=DataFramePtr(
                    data_frame_uuid=data_frame,
                    partition=3
                ),
                row_count=len(input_data),
            )
        ],
        output_data_frame_ptr=DataFramePtr(
            data_frame_uuid=random_uuid(),
            partition=0
        ),
        crypto_key_ptr=CryptoKeyPtr(
            schema_type=BINFHE
        ),
        circuit=Circuit(
            inputs=[
                InputStructure(
                    fields=[
                        UINT8
                    ]
                ),
                InputStructure(
                    fields=[
                        UINT8
                    ]
                )
            ],
            output=[
                OutputColumn(
                    data_type=UINT8,
                    name="test"
                )
            ],
            nodes=[
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=0)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=1)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=2)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=3)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=4)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=5)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=6)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=7)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=0)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=1)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=2)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=3)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=4)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=5)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=6)),
                Node(input=InputNode(tuple_index=1, field_index=0, bit_index=7)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(operation=OperationNode(type=OR)),
                Node(output=OutputNode(field_index=0, bit_index=0)),
                Node(output=OutputNode(field_index=0, bit_index=1)),
                Node(output=OutputNode(field_index=0, bit_index=2)),
                Node(output=OutputNode(field_index=0, bit_index=3)),
                Node(output=OutputNode(field_index=0, bit_index=4)),
                Node(output=OutputNode(field_index=0, bit_index=5)),
                Node(output=OutputNode(field_index=0, bit_index=6)),
                Node(output=OutputNode(field_index=0, bit_index=7))
            ],
            edges=[
                Edge(start=0, end=16),
                Edge(start=1, end=17),
                Edge(start=2, end=18),
                Edge(start=3, end=19),
                Edge(start=4, end=20),
                Edge(start=5, end=21),
                Edge(start=6, end=22),
                Edge(start=7, end=23),
                Edge(start=8, end=16),
                Edge(start=9, end=17),
                Edge(start=10, end=18),
                Edge(start=11, end=19),
                Edge(start=12, end=20),
                Edge(start=13, end=21),
                Edge(start=14, end=22),
                Edge(start=15, end=23),
                Edge(start=16, end=24),
                Edge(start=17, end=25),
                Edge(start=18, end=26),
                Edge(start=19, end=27),
                Edge(start=20, end=28),
                Edge(start=21, end=29),
                Edge(start=22, end=30),
                Edge(start=23, end=31),
            ]
        )
    )

    reduce_task(address, task)

    result = decrypt_data_frame(crypto_tool,
                                session, context, private_key,
                                task.output_data_frame_ptr.data_frame_uuid,
                                task.output_data_frame_ptr.partition,
                                len(input_data[0]), 1)

    assert [
                   '01111101',
           ] == result
