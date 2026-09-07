from engine.common.record import Record
from engine.common.rid import RID
from tests.fakes.fake_storage import FakeFileOrganization


def test_insert_and_fetch() -> None:
    org = FakeFileOrganization()
    rid = org.insert(Record(b"hello"))
    assert org.fetch(rid) == Record(b"hello")


def test_fetch_missing_returns_none() -> None:
    org = FakeFileOrganization()
    assert org.fetch(RID(0, 99)) is None


def test_remove() -> None:
    org = FakeFileOrganization()
    rid = org.insert(Record(b"x"))
    assert org.remove(rid) is True
    assert org.remove(rid) is False


def test_scan_yields_inserted_records() -> None:
    org = FakeFileOrganization()
    inserted = [org.insert(Record(data)) for data in (b"a", b"b", b"c")]
    assert {rid for rid, _ in org.scan()} == set(inserted)
