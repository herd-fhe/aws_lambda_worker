import os
import subprocess
import tempfile
import uuid
from typing import Tuple

import pytest


@pytest.fixture()
def address():
    port = os.environ.get("WORKER_PORT")
    return f'http://localhost:{port}/2015-03-31/functions/function/invocations'


@pytest.fixture(scope="session")
def crypto_tool():
    tools_dir = os.environ.get("TEST_HOME")
    return os.path.join(tools_dir, "crypto_tool")


@pytest.fixture(scope="session")
def session() -> str:
    return uuid.uuid4().urn[9:]


@pytest.fixture(scope="session")
def key(session, crypto_tool) -> Tuple[str, str]:
    key_dir = os.environ.get("KEY_BASE_DIR")

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        os.makedirs(os.path.join(key_dir, session), exist_ok=True)

        context = os.path.join(key_dir, session, "1.key")
        private = os.path.join(tmp_dir_name, "1.secret")
        subprocess.run([
            crypto_tool,
            "generate-keys",
            "--context_out",
            context, # only BinFHE for now,
            "--key_out",
            private
        ])

        yield context, private
