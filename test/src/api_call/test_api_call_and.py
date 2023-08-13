from typing import Tuple

import pytest

from generated.worker_pb2 import MapTask, DataFramePtr, CryptoKeyPtr, InputDataFramePtr
from generated.circuit_pb2 import Circuit, OutputColumn, InputStructure
from generated.node_pb2 import InputNode, OutputNode, Node, OperationNode, ConstantNode, AND
from generated.common_pb2 import *

from worker import generate_data_frame, map_task, decrypt_data_frame, random_uuid


def test_and(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 3
    input_data = [
        '11111111',
        '01111111',
        '00111111',
        '00011111',
        '00001111',
        '00000111',
        '00000011',
        '00000001',
        '00000000',
        '10000000',
        '11000000',
        '11100000',
        '11110000',
        '11111000',
        '11111100',
        '11111110'
    ]
    data_frame = generate_data_frame(crypto_tool, session, context, private_key, partition, input_data)

    task = MapTask(
        session_uuid=session,
        input_data_frame_ptr=InputDataFramePtr(
            pointer=DataFramePtr(
                data_frame_uuid=data_frame,
                partition=partition
            ),
            row_count=len(input_data),
        ),
        output_data_frame_ptr=DataFramePtr(
            data_frame_uuid=random_uuid(),
            partition=partition
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
                )
            ],
            output=[
                OutputColumn(
                    data_type=UINT8,
                    name="test"
                )
            ],
            nodes=[
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=False)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=0)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=1)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=2)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=3)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=4)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=5)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=6)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=7)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
                Node(operation=OperationNode(type=AND)),
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
                Edge(start=2, end=10),
                Edge(start=3, end=11),
                Edge(start=4, end=12),
                Edge(start=5, end=13),
                Edge(start=6, end=14),
                Edge(start=7, end=15),
                Edge(start=8, end=16),
                Edge(start=9, end=17),
                Edge(start=0, end=10),
                Edge(start=0, end=11),
                Edge(start=0, end=12),
                Edge(start=0, end=13),
                Edge(start=1, end=14),
                Edge(start=1, end=15),
                Edge(start=1, end=16),
                Edge(start=1, end=17),
                Edge(start=10, end=18),
                Edge(start=11, end=19),
                Edge(start=12, end=20),
                Edge(start=13, end=21),
                Edge(start=14, end=22),
                Edge(start=15, end=23),
                Edge(start=16, end=24),
                Edge(start=17, end=25),
            ]
        )
    )

    map_task(address, task, True)

    result = decrypt_data_frame(crypto_tool,
                                session, context, private_key,
                                task.output_data_frame_ptr.data_frame_uuid,
                                task.output_data_frame_ptr.partition,
                                len(input_data[0]), len(input_data))

    assert [
               '11110000',
               '01110000',
               '00110000',
               '00010000',
               '00000000',
               '00000000',
               '00000000',
               '00000000',
               '00000000',
               '10000000',
               '11000000',
               '11100000',
               '11110000',
               '11110000',
               '11110000',
               '11110000'
           ] == result
