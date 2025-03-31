"""
File: test_propertygraph.py
Description: A test of each method in PropertyGraph
"""

import pytest
from dstruct.propertygraph import Node, Relationship, PropertyGraph

@pytest.fixture
def s1():
    s1 = Node('nick', 'fiction', {'knows':'souren'})
    return s1

@pytest.fixture
def s2():
    s2 = Node('souren', 'non-fiction')
    return s2

@pytest.fixture
def a():
    a = Node('Nick', 'Person')
    return a

@pytest.fixture
def b():
    b =  Node('Souren', 'Person')
    return b

@pytest.fixture
def c():
    c = Node('Pride and Prejudice', 'Book', {'Price': 20})
    return c

@pytest.fixture
def d():
    d = Node('Dune', 'Book', {'Price': 20})
    return d

@pytest.fixture
def e():
    e = Relationship('Bought', {'Price': 19.45})
    return e

@pytest.fixture
def f():
    f = Relationship(category='Knows')
    return f

@pytest.fixture
def tg():
    tg = PropertyGraph()
    return tg

def test_node_constructor():
    s1 = Node('nick', 'fiction')
    assert isinstance(s1, Node), "It worked"
    assert type(s1.name) == str, "Name must be a string"
    assert type(s1.category) == str, "Category must be a string"
    assert type(s1.props) == type(None), "Properties must be a dictionary"
    assert s1.name == 'nick', "Name should be nick"
    assert s1.category == 'fiction', "Category should be fiction"
    assert s1.props is None, "The props should be None"

def test_node_getitem(s2):
    r = s2.__getitem__('knows')
    assert r is None, "There are no props now, the result should be none"
    s2.__setitem__('knows', 'souren')
    r = s2.__getitem__('knows')
    assert r == 'souren', "The result should be souren"
    r = s2.__getitem__(1)
    assert r is None, "The key doesnt exist, so the result should be None"


def test_node_setitem(s1, s2):
    s2.__setitem__('knows', 'souren')
    assert s2.props == {'knows': 'souren'}, "The props should be a dictionary with key of knows and value of souren"
    s1.__setitem__('knows', 'john')
    assert s1.props == {'knows': 'john'}, 'The props should be the same as earlier because a duplicate key will raise an exception'

def test_node_eq(s1,s2):
    a = s1.__eq__(s2)
    assert a is False, "s1 and s2 are not the same"
    b = s1.__eq__(s1)
    assert b is True, "s1 and s1 are the same"

def test_node_hash():
    a = s1.__hash__()
    b = s2.__hash__()
    assert a == a, "Hash should be the same"
    assert b == b, "Hash should be the same"
    assert a != b, "Hash should not be the same"

def test_node_repr(a,d):
    ra = repr(a)
    rd = repr(d)
    expa = "Nick:Person"
    expd = "Dune:Book\t{'Price': 20}"
    assert ra == expa, "Wrong Output"
    assert rd == expd, "Wrong Output"

def test_rel_constructor():
    s1 = Relationship('Bought', {'Price': 19.45})
    assert isinstance(s1, Relationship), "Incorrect type"
    assert type(s1.category) == str, "Name must be a string"
    assert type(s1.props) == dict, "Properties must be a dictionary"
    assert s1.category == 'Bought', "Category should be fiction"
    assert s1.props == {'Price': 19.45}, "The props should be correct"

def test_rel_getitem(e,f):
    price1 = e.__getitem__('Price')
    assert price1 == 19.45
    price3 = e.__getitem__("Doesnt exist")
    assert price3 is None
    price3 = f.__getitem__("Doesnt exist")
    assert price3 is None

def test_rel_setitem(e,f):
    e.__setitem__('Canadian Price', 25)
    assert e.props.__getitem__('Canadian Price') == 25
    f.__setitem__('Canadian Price', 25)
    assert e.props.__getitem__('Canadian Price') == 25

def test_rel_repr(e,f):
    re = repr(e)
    rf = repr(f)
    expe = ":Bought {'Price': 19.45}"
    expf = ":Knows"
    assert re == expe, "Wrong Output"
    assert rf == expf, "Wrong Output"

def test_pg_constructor():
    tester = PropertyGraph()
    assert type(tester) == PropertyGraph, "It should make a property graph"

def test_pg_addnode(a, tg, b):
    tg.add_node(a)
    assert a in tg.pg.keys(), "a should be in the keys of tg"
    assert tg.pg[a] == [(),()], "The structure of a property graph should be {Src, [(Targs),(Rels)]}"
    with pytest.raises(Exception):
        tg.add_node(a)
    with pytest.raises(Exception):
        tg.add_node(5)

def test_pg_addrelationship(a, b, c, d, e, f, tg):
    tg.add_relationship(b, d, e)
    assert b in tg.pg.keys(), "b should be in the keys of tg"
    assert d in tg.pg.keys(), "d should be in the keys of tg"
    assert e in tg.pg.get(b)[1], "e should be in the values of tg"
    assert d in tg.pg.get(b)[0], "d should be in the values of tg"
    tg.add_relationship(a, b, f)
    assert len(tg.pg.keys()) == len(set(tg.pg.keys()))
    assert len(tg.pg.get(b)[1]) == len(tg.pg.get(b)[0])
    with pytest.raises(Exception):
        tg.add_node(5, c, f)
    with pytest.raises(Exception):
        tg.add_node(a, b, c)
    with pytest.raises(Exception):
        tg.add_node(a, 5, f)
    with pytest.raises(Exception):
        tg.add_node(a, b, 5)
    with pytest.raises(Exception):
        tg.add_node(a, a, e)
    with pytest.raises(Exception):
        tg.add_node(b, d, e)

def test_pg_getnodes(tg, a, b, c, d, e, f):
    tg.add_relationship(a, c, e)
    tg.add_relationship(a, b, f)
    tg.add_relationship(a, d, e)
    test1 = tg.get_nodes(name = 'Nick', category = None, key = None, value = None)
    assert test1 == {a}
    test2 =tg.get_nodes(name=None, category='Person', key=None, value=None)
    assert test2 == {a,b}, "Wrong output"
    test3 =tg.get_nodes(name=None, category=None, key='Price', value=None)
    assert test3 == {c,d}, "wrong output"
    test4 = tg.get_nodes(name=None, category=None, key=None, value=20)
    assert test4 == {c,d}, "Wrong output"
    test5 = tg.get_nodes(name=None, category='Person', key=None, value=20)
    assert test5 == set(), "Wrong output"
    test6 = tg.get_nodes(name=None, category=None, key=None, value=None)
    assert test6 == {a,b,c,d}, "Wrong output"
    with pytest.raises(Exception):
        tg.get_nodes(1, 'Book', 'Price', 20)
    with pytest.raises(Exception):
        tg.get_nodes(1, 'Book', 'Price', 20)
    with pytest.raises(Exception):
        tg.get_nodes('Dune', 'Book', 'Price', '20')
def test_pg_adjacent(tg, a, b, c, d, e, f):
    tg.add_relationship(a, c, e)
    tg.add_relationship(a, b, f)
    tg.add_relationship(a, d, e)
    tg.add_relationship(b, d, e)
    set_adj = tg.adjacent(a)
    assert set_adj == {b,d,c}, "Wrong output"
    set_adj = tg.adjacent(a, node_category='Book')
    assert set_adj == {d, c}, "Wrong output"
    set_adj = tg.adjacent(b, rel_category='Knows')
    assert set_adj == {a}, "Wrong output"
    assert type(set_adj) == set, "Wrong Type"
    with pytest.raises(Exception):
        tg.adjacent({4,a})
def test_pg_subgraph(tg, a, b, c, d, e, f):
    sub_test = tg.subgraph({a,b,c})
    comp = PropertyGraph()
    comp.add_relationship(a, c, e)
    comp.add_relationship(a, b, f)
    assert sub_test.pg.keys() == comp.pg.keys(), "Wrong output"
    with pytest.raises(Exception):
        tg.subgraph(a)
    with pytest.raises(Exception):
        tg.subgraph({a,b,5})
def test_pg_repr(tg, b, d):
    tester = tg.subgraph({b, d})
    expected1 = (
        "Dune (Book)\n"
        "Souren (Person)\n"
        "\tBought: Dune (Book)\n"
    )
    expected2 = (
        "Souren (Person)\n"
        "\tBought: Dune (Book)\n"
        "Dune (Book)\n"
    )
    assert tester.__repr__() == expected1 or expected2, "Wrong output"