from typing import Tuple

import pytest

from generated.worker_pb2 import MapTask, DataFramePtr, CryptoKeyPtr, InputDataFramePtr
from generated.circuit_pb2 import Circuit, OutputColumn, InputStructure
from generated.node_pb2 import InputNode, OutputNode, Node, ConstantNode
from generated.common_pb2 import *

from worker import random_uuid, generate_data_frame, map_task


def test_wrong_out_bit(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 3
    input_data = [
        '11111111',
        '01111111',
        '00111111',
        '00011111'
    ]
    data_frame = generate_data_frame(crypto_tool, session, context, private_key, partition, input_data)

    task = MapTask(
        session_uuid=session,
        input_data_frame_ptr=InputDataFramePtr(
            pointer=DataFramePtr(
                data_frame_uuid=data_frame,
                partition=partition
            ),
            row_count=len(input_data)
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
                Node(constant=ConstantNode(value=False)),
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=False)),
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=True)),
                Node(output=OutputNode(field_index=0, bit_index=22)),
                Node(output=OutputNode(field_index=0, bit_index=1)),
                Node(output=OutputNode(field_index=0, bit_index=2)),
                Node(output=OutputNode(field_index=0, bit_index=3)),
                Node(output=OutputNode(field_index=0, bit_index=4)),
                Node(output=OutputNode(field_index=0, bit_index=5)),
                Node(output=OutputNode(field_index=0, bit_index=6)),
                Node(output=OutputNode(field_index=0, bit_index=7))
            ],
            edges=[
                Edge(start=0, end=8),
                Edge(start=1, end=9),
                Edge(start=2, end=10),
                Edge(start=3, end=11),
                Edge(start=4, end=12),
                Edge(start=5, end=13),
                Edge(start=6, end=14),
                Edge(start=7, end=15),
            ]
        )
    )

    assert "errorMessage" in map_task(address, task).json()


def test_wrong_out_tuple(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 3
    input_data = [
        '11111111',
        '01111111',
        '00111111',
        '00011111'
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
            data_frame_uuid="f5a1afbc-7090-483b-8602-eaca0d5c7620",
            partition=3
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
                Node(constant=ConstantNode(value=False)),
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=False)),
                Node(constant=ConstantNode(value=True)),
                Node(constant=ConstantNode(value=True)),
                Node(output=OutputNode(field_index=32, bit_index=0)),
                Node(output=OutputNode(field_index=0, bit_index=1)),
                Node(output=OutputNode(field_index=0, bit_index=2)),
                Node(output=OutputNode(field_index=0, bit_index=3)),
                Node(output=OutputNode(field_index=0, bit_index=4)),
                Node(output=OutputNode(field_index=0, bit_index=5)),
                Node(output=OutputNode(field_index=0, bit_index=6)),
                Node(output=OutputNode(field_index=0, bit_index=7))
            ],
            edges=[
                Edge(start=0, end=8),
                Edge(start=1, end=9),
                Edge(start=2, end=10),
                Edge(start=3, end=11),
                Edge(start=4, end=12),
                Edge(start=5, end=13),
                Edge(start=6, end=14),
                Edge(start=7, end=15),
            ]
        )
    )

    assert "errorMessage" in map_task(address, task).json()


def test_wrong_in_tuple(address, crypto_tool, session, key: Tuple[str, str]):
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
                Node(input=InputNode(tuple_index=21, field_index=0, bit_index=0)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=1)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=2)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=3)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=4)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=5)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=6)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=7)),
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
                Edge(start=0, end=8),
                Edge(start=1, end=9),
                Edge(start=2, end=10),
                Edge(start=3, end=11),
                Edge(start=4, end=12),
                Edge(start=5, end=13),
                Edge(start=6, end=14),
                Edge(start=7, end=15),
            ]
        )
    )

    assert "errorMessage" in map_task(address, task).json()


def test_wrong_in_field(address, crypto_tool, session, key: Tuple[str, str]):
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
            data_frame_uuid="f5a1afbc-7090-483b-8602-eaca0d5c7620",
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
                Node(input=InputNode(tuple_index=0, field_index=22, bit_index=0)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=1)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=2)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=3)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=4)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=5)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=6)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=7)),
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
                Edge(start=0, end=8),
                Edge(start=1, end=9),
                Edge(start=2, end=10),
                Edge(start=3, end=11),
                Edge(start=4, end=12),
                Edge(start=5, end=13),
                Edge(start=6, end=14),
                Edge(start=7, end=15),
            ]
        )
    )

    assert "errorMessage" in map_task(address, task).json()


def test_wrong_in_bit(address, crypto_tool, session, key: Tuple[str, str]):
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
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=0)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=21)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=2)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=3)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=4)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=5)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=6)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=7)),
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
                Edge(start=0, end=8),
                Edge(start=1, end=9),
                Edge(start=2, end=10),
                Edge(start=3, end=11),
                Edge(start=4, end=12),
                Edge(start=5, end=13),
                Edge(start=6, end=14),
                Edge(start=7, end=15),
            ]
        )
    )

    assert "errorMessage" in map_task(address, task).json()
