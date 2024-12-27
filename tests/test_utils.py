import pytest

import stifc.utils as utils

def test_make_numbered_name_1():
    iterable = ["node_1", "node_2", "node_3"]
    base_string = "node_"
    result = utils.make_numbered_name(iterable, base_string)
    assert result == "node_4"

def test_make_numbered_name_2():
    iterable = ["member_1", "member_2", "member_4"]
    base_string = "member_"
    result = utils.make_numbered_name(iterable, base_string)
    assert result == "member_5"

def test_make_numbered_name_3():
    iterable = []
    base_string = "node_"
    result = utils.make_numbered_name(iterable, base_string)
    assert result == "node_0"

def test_make_numbered_name_4():
    iterable = ["node_1", "node_3", "not_a_number"]
    base_string = "node_"
    result = utils.make_numbered_name(iterable, base_string)
    assert result == "node_4"

def test_make_numbered_name_5():
    iterable = ["not_a_number"]
    base_string = "member_"
    result = utils.make_numbered_name(iterable, base_string)
    assert result == "member_0"
