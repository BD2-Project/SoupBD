from engine.common.rid import RID


def test_rid_is_namedtuple() -> None:
    rid = RID(page_id=3, slot=7)
    assert rid.page_id == 3
    assert rid.slot == 7
    assert rid == RID(3, 7)


def test_rid_is_hashable() -> None:
    assert len({RID(1, 2), RID(1, 2), RID(1, 3)}) == 2
