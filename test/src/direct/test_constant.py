import pytest

from generated.worker_pb2 import MapTask, DataFramePtr, CryptoKeyPtr, InputDataFramePtr
from generated.circuit_pb2 import Circuit, OutputColumn, InputStructure
from generated.node_pb2 import OutputNode, Node, ConstantNode
from generated.common_pb2 import *

from worker import generate_data_frame, map_task, decrypt_data_frame, random_uuid


def test_constant(address, crypto_tool, session, key):
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
               '10011011', '10011011',
               '10011011', '10011011',
           ] == result