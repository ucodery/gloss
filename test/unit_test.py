import collections.abc
from itertools import chain
from typing import Dict

import pytest
from mypy.api import run as run_mypy

from gloss import Gloss


@pytest.fixture
def g():
    return Gloss(
        {
            "xs": 5,
            "s": 10,
            "m": 15,
            "l": 20,
            "xl": 25,
            "xxl": 30,
        }
    )


# Test class instantiation


def test_create():
    g = Gloss()
    assert repr(g) == "Gloss({})"

    g = Gloss(a=1, b=2)
    assert repr(g) == "Gloss({'a': 1, 'b': 2})"

    g = Gloss((("a", 1), ("b", 2)))
    assert repr(g) == "Gloss({'a': 1, 'b': 2})"

    g = Gloss({"a": 1, "b": 2})
    assert repr(g) == "Gloss({'a': 1, 'b': 2})"

    g = Gloss({"a": 1, "b": 2}, c=3)
    assert repr(g) == "Gloss({'a': 1, 'b': 2, 'c': 3})"

    g = Gloss((("a", 1), ("b", 2)), c=3)
    assert repr(g) == "Gloss({'a': 1, 'b': 2, 'c': 3})"


def test_create_duplicate_terms():
    g = Gloss(a="b", b="a", c="c")
    assert repr(g) == "Gloss({'b': 'a', 'c': 'c'})"

    g = Gloss((("a", "b"), ("b", "c"), ("c", "a")))
    assert repr(g) == "Gloss({'c': 'a'})"

    g = Gloss({"a": "d", "b": "d", "c": "d"})
    assert repr(g) == "Gloss({'c': 'd'})"

    g = Gloss((("d", "a"), ("d", "b"), ("d", "c")))
    assert repr(g) == "Gloss({'d': 'c'})"


def test_create_fail():
    with pytest.raises(TypeError):
        Gloss(a=[])
    with pytest.raises(TypeError):
        Gloss({"a": dict()})
    with pytest.raises(TypeError):
        Gloss((lambda: None, 0))
    with pytest.raises(ValueError):
        Gloss(({}, 1))


# Test term access and mutation


def test_update_term(g):
    g["xs"] = 3
    assert repr(g) == "Gloss({'xs': 3, 's': 10, 'm': 15, 'l': 20, 'xl': 25, 'xxl': 30})"

    g[3] = "xxs"
    assert (
        repr(g) == "Gloss({'s': 10, 'm': 15, 'l': 20, 'xl': 25, 'xxl': 30, 3: 'xxs'})"
    )

    g[3] = "s"
    assert repr(g) == "Gloss({'m': 15, 'l': 20, 'xl': 25, 'xxl': 30, 3: 's'})"


def test_new_term(g):
    g["xxs"] = 3
    assert (
        repr(g)
        == "Gloss({'xs': 5, 's': 10, 'm': 15, 'l': 20, 'xl': 25, 'xxl': 30, 'xxs': 3})"
    )

    g[17] = "xm"
    assert repr(g) == (
        "Gloss({'xs': 5, 's': 10, 'm': 15, 'l': 20, 'xl': 25, 'xxl': 30, 'xxs': 3, "
        "17: 'xm'})"
    )


def test_illegal_term(g):
    with pytest.raises(TypeError):
        g[{}] = g


def test_get_term(g):
    assert g["s"] == 10
    assert g["m"] == 15
    assert g[5] == "xs"
    assert g[30] == "xxl"


def test_get_missing_term(g):
    with pytest.raises(KeyError):
        g["xm"]


def test_delete_term(g):
    del g["s"]
    del g[15]

    assert "s" not in g
    assert 15 not in g
    assert "m" not in g
    assert 10 not in g

    g["m"] = "m"
    start_len = len(g)
    del g["m"]
    assert "m" not in g
    assert (len(g) + 2) == start_len


def test_delete_missing_term(g):
    with pytest.raises(KeyError):
        del g["xm"]


# Test attributes


def test_clear(g):
    g.clear()

    assert len(g) == 0
    assert repr(g) == "Gloss({})"

    g["s"] = 10
    assert len(g) == 2
    assert repr(g) == "Gloss({'s': 10})"


def test_copy(g):
    g["xm"] = 17

    g_copy = g.copy()
    assert g == g_copy
    assert g is not g_copy

    g["xm"] = 18
    assert g["xm"] == 18
    assert g_copy["xm"] == 17


def test_get(g):
    assert g.get("s") == 10
    assert g.get(5) == "xs"
    assert g.get(4) is None
    assert g.get(4, "xm") == "xm"
    assert g.get(15, "xm") == "m"


def test_items(g):
    items = list(g.items())
    assert len(items) == len(g)
    all_items = sorted(chain.from_iterable(items), key=str)
    all_terms = sorted(chain(g, g), key=str)
    assert all_items == all_terms


def test_pop(g):
    assert g.pop("s") == 10
    assert g.pop(5) == "xs"
    assert "s" not in g
    assert "xs" not in g

    assert g.pop(20, "xm") == "l"
    assert g.pop(20, "xm") == "xm"
    assert "l" not in g
    assert "xm" not in g

    with pytest.raises(KeyError):
        g.pop("xm")


def test_popitem(g):
    terms = []
    pairs = []
    _len = 12
    while _len > 0:
        assert len(g) == _len
        t, v = g.popitem()
        terms.append(t)
        pairs.append(v)
        _len -= 2

    assert len(g) == 0
    with pytest.raises(KeyError):
        g.popitem()

    terms.sort()
    assert terms == ["l", "m", "s", "xl", "xs", "xxl"]
    pairs.sort()
    assert pairs == [5, 10, 15, 20, 25, 30]


def test_setdefault(g):
    assert g.setdefault("s", 12) == 10
    assert g["s"] == 10
    assert g.setdefault("xm", 17) == 17
    assert g["xm"] == 17


def test_update(g):
    g.update(xs=3)
    assert repr(g) == "Gloss({'xs': 3, 's': 10, 'm': 15, 'l': 20, 'xl': 25, 'xxl': 30})"

    g.update({"m": 16, "L": 20})
    assert repr(g) == "Gloss({'xs': 3, 's': 10, 'm': 16, 'xl': 25, 'xxl': 30, 'L': 20})"

    g.update(Gloss({"xm": 16, "xxs": 1}))
    assert (
        repr(g)
        == "Gloss({'xs': 3, 's': 10, 'xl': 25, 'xxl': 30, 'L': 20, 16: 'xm', 1: 'xxs'})"
    )

    g.update(
        Gloss(
            (
                (1, "one"),
                (3, "three"),
                (10, "ten"),
                (16, "sixteen"),
                (20, "twenty"),
                (25, "twentyfive"),
                (30, "thirty"),
            )
        )
    )
    assert repr(g) == (
        "Gloss({'one': 1, 'three': 3, 'ten': 10, 'sixteen': 16, 'twenty': 20, "
        "'twentyfive': 25, 'thirty': 30})"
    )


def test_update_fail(g):
    with pytest.raises(TypeError):
        g.update(list=[0, 1, 2])


# Test common builtin operations on Gloss


def test_len():
    g = Gloss()
    assert len(g) == 0

    g["a"] = 1
    assert len(g) == 2

    g["b"] = "b"
    assert len(g) == 4

    g["c"] = 1
    assert len(g) == 4

    g["b"] = "c"
    assert len(g) == 2

    del g["c"]
    assert len(g) == 0


def test_iterate(g):
    generator = (t for t in g)
    iterator = iter(g)
    for term in g:
        gen = next(generator)
        iter_ = next(iterator)
        assert term == gen and term == iter_
        assert g[term] == g[gen] and g[term] == g[gen]

    with pytest.raises(StopIteration):
        next(generator)
    with pytest.raises(StopIteration):
        next(iterator)


def test_set(g):
    comprehension = {t for t in g}
    from_class = set(g)
    from_keys = set(g.keys())
    from_values = set(g.values())
    from_terms = set(g.terms())
    for term in comprehension:
        from_class.remove(term)
        from_keys.remove(term)
        from_values.remove(term)
        from_terms.remove(term)
    assert len(from_class) == 0
    assert len(from_keys) == 0
    assert len(from_values) == 0
    assert len(from_terms) == 0


def test_list(g):
    comprehension = [t for t in g]
    from_class = list(g)
    from_keys = list(g.keys())
    from_values = list(g.values())
    from_terms = list(g.terms())
    # order is not guaranteed
    for term in comprehension:
        from_class.remove(term)
        from_keys.remove(term)
        from_values.remove(term)
        from_terms.remove(term)
    assert len(from_class) == 0
    assert len(from_keys) == 0
    assert len(from_values) == 0
    assert len(from_terms) == 0


def test_dict(g):
    comprehension = {t: g[t] for t in g}
    from_class = dict(g)
    from_keys = dict((t, g[t]) for t in g.keys())
    from_values = dict((t, g[t]) for t in g.values())
    from_terms = dict((t, g[t]) for t in g.terms())
    from_items = dict((t, v) for t, v in g.items())
    # key:value order is not guaranteed
    for c, f, k, v, t, i in zip(
        comprehension, from_class, from_keys, from_values, from_terms, from_items
    ):
        assert (c == f and comprehension[c] == from_class[f]) or (
            c == from_class[f] and comprehension[c] == f
        )
        assert (f == k and from_class[f] == from_keys[k]) or (
            f == from_keys[k] and from_class[f] == k
        )
        assert (k == v and from_keys[k] == from_values[v]) or (
            k == from_values[v] and from_keys[k] == v
        )
        assert (v == t and from_values[v] == from_terms[t]) or (
            v == from_terms[t] and from_values[v] == t
        )
        assert (t == i and from_terms[t] == from_items[i]) or (
            t == from_items[i] and from_terms[t] == i
        )
    assert len(from_class) == len(g)


def test_type():
    g = Gloss()
    assert isinstance(g, dict)
    assert isinstance(g, Dict)
    assert isinstance(g, collections.abc.MutableMapping)


def test_mypy():
    check = run_mypy(
        [
            "--no-error-summary",
            "-c",
            """
from typing import Dict, Mapping, MutableMapping

from gloss import Gloss, TermType

example: Gloss
foo: TermType
bar: TermType
baz: TermType
qux: TermType

foo = "foo"
bar = b"bar"
baz = 3
qux = (0.3,)

example = Gloss({foo: bar, baz: qux})
example = Gloss(((foo, bar), (baz, qux)))
example = Gloss(foo=foo, bar=bar, baz=baz, qux=qux)

otherD: Dict = Gloss()
otherM: Mapping = Gloss()
otherMM: MutableMapping = Gloss()
""",
        ]
    )

    assert check == ("", "", 0)
