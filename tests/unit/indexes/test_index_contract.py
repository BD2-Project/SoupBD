"""Conformance suite for every Index implementation.

The suite parametrizes over all implementations; real disk-backed indexes
(BPlusTree, ExtendibleHash) join the params when they exist.
"""

from collections import defaultdict

import pytest
from hypothesis import given
from hypothesis import strategies as st

from engine.common.rid import RID
from tests.fakes.fake_index import FakeIndex


@pytest.fixture(params=[FakeIndex])
def index(request, tmp_path):
    idx = request.param()
    yield idx
    idx.close()


def test_insert_and_search(index) -> None:
    rid = RID(page_id=0, slot=1)
    index.insert(10, rid)
    assert index.search(10) == [rid]


def test_duplicate_keys_return_all_rids(index) -> None:
    rids = [RID(0, i) for i in range(3)]
    for rid in rids:
        index.insert("a", rid)
    assert sorted(index.search("a")) == sorted(rids)


def test_search_missing_key_returns_empty(index) -> None:
    assert index.search(999) == []


def test_remove_and_verify_gone(index) -> None:
    rid = RID(1, 1)
    index.insert(5, rid)
    assert index.remove(5, rid) == 1
    assert index.search(5) == []


def test_remove_all_under_key(index) -> None:
    for i in range(2):
        index.insert(7, RID(0, i))
    assert index.remove(7) == 2
    assert index.search(7) == []


@pytest.mark.skip(reason="requires a disk-backed index (BPlusTree, ExtendibleHash)")
def test_persistence(index, tmp_path) -> None:
    """Cerrar, reabrir desde el mismo path y verificar que los datos siguen ahí."""


@given(st.lists(st.integers(min_value=0, max_value=1000), max_size=200))
def test_fuzz_against_oracle(keys: list[int]) -> None:
    idx = FakeIndex()
    oracle: dict[int, list[RID]] = defaultdict(list)
    for key in keys:
        rid = RID(0, len(oracle[key]))
        idx.insert(key, rid)
        oracle[key].append(rid)
    sample = set(keys) | {2000}
    for key in sample:
        assert sorted(idx.search(key)) == sorted(oracle[key])
    idx.close()
