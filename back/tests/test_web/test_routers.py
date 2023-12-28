import re
from random import randbytes
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from main import app
from web.dependencies import get_file_crud, get_file
from web.models import RWFile
from web.crud import FileCRUD, FILEID_LEN

engine = create_engine("sqlite:///tests/dbs/test_routers.db")
SQLModel.metadata.drop_all(engine)


def get_fake_filecrud():
    with Session(engine) as sess:
        yield FileCRUD(sess)


def get_fake_file(blob_size: int, filename: str):
    return RWFile(
        blob=randbytes(blob_size * 1024**2),
        filename=filename,
    )


app.dependency_overrides[get_file_crud] = get_fake_filecrud
app.dependency_overrides[get_file] = get_fake_file


@pytest.fixture
def client():
    SQLModel.metadata.create_all(engine)
    client = TestClient(app)
    yield client
    client.close()
    SQLModel.metadata.drop_all(engine)


class TestFileRoutes:
    def test_post_file_ok(self, client: TestClient):
        res = client.post(
            "/file-service/file",
            params={
                "blob_size": 1,
                "filename": "aboba",
            },
        )
        file_id = res.json()["file_id"]

        assert res.status_code == 201
        assert len(file_id) == FILEID_LEN

    def test_post_file_too_large(self, client: TestClient):
        res = client.post(
            "/file-service/file",
            params={
                "blob_size": 3,
                "filename": "aboba",
            },
        )

        assert res.status_code == 400
        assert res.json()["file_maxsize"] == 2
        assert res.json()["recieved_size"] == 3

    def test_recieve_file_ok(self, client: TestClient):
        body = randbytes(1024**2)
        filename = "або-bus"
        with Session(engine) as sess:
            file_id = FileCRUD(sess).save_file(
                RWFile(
                    blob=body,
                    filename=filename,
                )
            )

        res = client.get("/file-service/file", params={"file_id": file_id})

        search_res = re.search(
            r'attachment; filename="(.+)"', res.headers["Content-Disposition"]
        )
        if not search_res:
            raise Exception("filename not found")

        assert res.status_code == 200
        assert res.content == body
        assert quote(filename, safe="") == search_res[1]

    def test_recieve_file_not_found(self, client: TestClient):
        res = client.get(
            "/file-service/file",
            params={"file_id": "notexisting"}
        )

        assert res.status_code == 404
