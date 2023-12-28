from datetime import datetime, timedelta

import pytest
from sqlmodel import SQLModel, create_engine, Session, select, func

from web.models import File, RWFile
from web.crud import FileCRUD, ID_SYMBOLS, FILEID_LEN

engine = create_engine("sqlite:///tests/dbs/test_crud.db")
SQLModel.metadata.drop_all(engine)


@pytest.fixture
def db_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as sess:
        yield sess
    SQLModel.metadata.drop_all(engine)


rows = [
    (
        ID_SYMBOLS[1] * FILEID_LEN,
        "aboba.jpg",
        b"aboba",
        datetime.now() - timedelta(hours=1),
    ),
    (
        ID_SYMBOLS[2] * FILEID_LEN,
        "meme.txt",
        b"My name is Giovanni Giorgio,\nbut everybody calls me Giorgio.\n",
        datetime.now() - timedelta(days=3),
    ),
    (
        ID_SYMBOLS[3] * FILEID_LEN,
        "kirill.txt",
        b"main abobus",
        datetime.now() - timedelta(minutes=30),
    ),
]


@pytest.fixture
def insert_test_data(db_session: Session):
    for id, name, content, time in rows:
        db_session.add(
            File(
                id=id,
                filename=name,
                blob=content,
                created_at=time,
            )
        )
    db_session.commit()


class TestFileCRUD:
    def test_save_file(self, db_session: Session, insert_test_data):
        crud = FileCRUD(db_session)

        file_id = crud.save_file(
            RWFile(
                filename="simple_name",
                blob=b"interesting_content",
            )
        )

        assert len(file_id) == FILEID_LEN
        for c in file_id:
            assert c in ID_SYMBOLS
        assert (
            db_session.exec(
                select(func.count("*"))
                .select_from(File)
                .where(File.filename == "simple_name")
                .where(File.blob == b"interesting_content")
            ).first()
            == 1
        )

    def test_get_file_by_id_ok(self, db_session: Session, insert_test_data):
        crud = FileCRUD(db_session)

        res = crud.get_file_by_id(ID_SYMBOLS[1] * FILEID_LEN)
        row_count = db_session.exec(
            select(func.count("*"))
            .select_from(File)
            .where(File.id == ID_SYMBOLS[1] * FILEID_LEN)
        ).first()

        assert (
            res is not None
            and res.filename == "aboba.jpg"
            and res.blob == b"aboba"
            and row_count == 0
        )

    def test_get_file_by_id_fail(self, db_session: Session, insert_test_data):
        crud = FileCRUD(db_session)

        res = crud.get_file_by_id("notexists")

        assert res is None

    def test_delete_expired(self, db_session: Session, insert_test_data):
        crud = FileCRUD(db_session)

        crud.delete_expired(timedelta(days=1))

        assert (
            db_session.exec(
                select(func.count("*"))
                .select_from(File)
            ).first()
            == 2
        )
