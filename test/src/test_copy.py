from typing import Tuple

import pytest

from generated.worker_pb2 import MapTask, DataFramePtr, CryptoKeyPtr, InputDataFramePtr
from generated.circuit_pb2 import Circuit, OutputColumn, InputStructure
from generated.node_pb2 import InputNode, OutputNode, Node
from generated.common_pb2 import *

from worker import generate_data_frame, map_task, decrypt_data_frame, random_uuid


def test_copy_8(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 0
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

    map_task(address, task)

    result = decrypt_data_frame(crypto_tool,
                                session, context, private_key,
                                task.output_data_frame_ptr.data_frame_uuid,
                                task.output_data_frame_ptr.partition,
                                len(input_data[0]), len(input_data))

    assert [
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
           ] == result


def test_copy_16(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 1
    input_data = [
        '1111111111111111', '0111111111111111', '0011111111111111', '0001111111111111',
        '0000111111111111', '0000011111111111', '0000001111111111', '0000000111111111',
        '0000000011111111', '0000000001111111', '0000000000111111', '0000000000011111',
        '0000000000001111', '0000000000000111', '0000000000000011', '0000000000000001',
        '0000000000000000', '1000000000000000', '1100000000000000', '1110000000000000',
        '1111000000000000', '1111100000000000', '1111110000000000', '1111111000000000',
        '1111111100000000', '1111111110000000', '1111111111000000', '1111111111100000',
        '1111111111110000', '1111111111111000', '1111111111111100', '1111111111111110',
    ]
    data_frame = generate_data_frame(crypto_tool, session, context, private_key, partition, input_data)

    task = MapTask(
        session_uuid=session,
        input_data_frame_ptr=InputDataFramePtr(
            pointer=DataFramePtr(
                data_frame_uuid=data_frame,
                partition=partition
            ),
            row_count=32,
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
                        UINT16
                    ]
                )
            ],
            output=[
                OutputColumn(
                    data_type=UINT16,
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
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=8)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=9)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=10)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=11)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=12)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=13)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=14)),
                Node(input=InputNode(tuple_index=0, field_index=0, bit_index=15)),
                Node(output=OutputNode(field_index=0, bit_index=0)),
                Node(output=OutputNode(field_index=0, bit_index=1)),
                Node(output=OutputNode(field_index=0, bit_index=2)),
                Node(output=OutputNode(field_index=0, bit_index=3)),
                Node(output=OutputNode(field_index=0, bit_index=4)),
                Node(output=OutputNode(field_index=0, bit_index=5)),
                Node(output=OutputNode(field_index=0, bit_index=6)),
                Node(output=OutputNode(field_index=0, bit_index=7)),
                Node(output=OutputNode(field_index=0, bit_index=8)),
                Node(output=OutputNode(field_index=0, bit_index=9)),
                Node(output=OutputNode(field_index=0, bit_index=10)),
                Node(output=OutputNode(field_index=0, bit_index=11)),
                Node(output=OutputNode(field_index=0, bit_index=12)),
                Node(output=OutputNode(field_index=0, bit_index=13)),
                Node(output=OutputNode(field_index=0, bit_index=14)),
                Node(output=OutputNode(field_index=0, bit_index=15))
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
                Edge(start=8, end=24),
                Edge(start=9, end=25),
                Edge(start=10, end=26),
                Edge(start=11, end=27),
                Edge(start=12, end=28),
                Edge(start=13, end=29),
                Edge(start=14, end=30),
                Edge(start=15, end=31),
            ]
        )
    )

    map_task(address, task)

    result = decrypt_data_frame(crypto_tool,
                                session, context, private_key,
                                task.output_data_frame_ptr.data_frame_uuid,
                                task.output_data_frame_ptr.partition,
                                len(input_data[0]), len(input_data))
    assert [
               '1111111111111111', '0111111111111111', '0011111111111111', '0001111111111111',
               '0000111111111111', '0000011111111111', '0000001111111111', '0000000111111111',
               '0000000011111111', '0000000001111111', '0000000000111111', '0000000000011111',
               '0000000000001111', '0000000000000111', '0000000000000011', '0000000000000001',
               '0000000000000000', '1000000000000000', '1100000000000000', '1110000000000000',
               '1111000000000000', '1111100000000000', '1111110000000000', '1111111000000000',
               '1111111100000000', '1111111110000000', '1111111111000000', '1111111111100000',
               '1111111111110000', '1111111111111000', '1111111111111100', '1111111111111110',
           ] == result


def test_copy_2_8(address, crypto_tool, session, key: Tuple[str, str]):
    context, private_key = key

    partition = 2
    input_data = [
        '1111111111111111', '0111111111111111', '0011111111111111', '0001111111111111',
        '0000111111111111', '0000011111111111', '0000001111111111', '0000000111111111',
        '0000000011111111', '0000000001111111', '0000000000111111', '0000000000011111',
        '0000000000001111', '0000000000000111', '0000000000000011', '0000000000000001',
        '0000000000000000', '1000000000000000', '1100000000000000', '1110000000000000',
        '1111000000000000', '1111100000000000', '1111110000000000', '1111111000000000',
        '1111111100000000', '1111111110000000', '1111111111000000', '1111111111100000',
        '1111111111110000', '1111111111111000', '1111111111111100', '1111111111111110',
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
                        INT8,
                        UINT8
                    ]
                )
            ],
            output=[
                OutputColumn(
                    data_type=UINT8,
                    name="test"
                ),
                OutputColumn(
                    data_type=UINT8,
                    name="test2"
                ),
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
                Node(output=OutputNode(field_index=0, bit_index=0)),
                Node(output=OutputNode(field_index=0, bit_index=1)),
                Node(output=OutputNode(field_index=0, bit_index=2)),
                Node(output=OutputNode(field_index=0, bit_index=3)),
                Node(output=OutputNode(field_index=0, bit_index=4)),
                Node(output=OutputNode(field_index=0, bit_index=5)),
                Node(output=OutputNode(field_index=0, bit_index=6)),
                Node(output=OutputNode(field_index=0, bit_index=7)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=0)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=1)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=2)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=3)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=4)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=5)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=6)),
                Node(input=InputNode(tuple_index=0, field_index=1, bit_index=7)),
                Node(output=OutputNode(field_index=1, bit_index=0)),
                Node(output=OutputNode(field_index=1, bit_index=1)),
                Node(output=OutputNode(field_index=1, bit_index=2)),
                Node(output=OutputNode(field_index=1, bit_index=3)),
                Node(output=OutputNode(field_index=1, bit_index=4)),
                Node(output=OutputNode(field_index=1, bit_index=5)),
                Node(output=OutputNode(field_index=1, bit_index=6)),
                Node(output=OutputNode(field_index=1, bit_index=7))
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

    map_task(address, task)
    result = decrypt_data_frame(crypto_tool,
                                session, context, private_key,
                                task.output_data_frame_ptr.data_frame_uuid,
                                task.output_data_frame_ptr.partition,
                                len(input_data[0]), len(input_data))

    assert [
               '1111111111111111', '0111111111111111', '0011111111111111', '0001111111111111',
               '0000111111111111', '0000011111111111', '0000001111111111', '0000000111111111',
               '0000000011111111', '0000000001111111', '0000000000111111', '0000000000011111',
               '0000000000001111', '0000000000000111', '0000000000000011', '0000000000000001',
               '0000000000000000', '1000000000000000', '1100000000000000', '1110000000000000',
               '1111000000000000', '1111100000000000', '1111110000000000', '1111111000000000',
               '1111111100000000', '1111111110000000', '1111111111000000', '1111111111100000',
               '1111111111110000', '1111111111111000', '1111111111111100', '1111111111111110',
           ] == result