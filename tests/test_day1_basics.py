import pytest

def test_addition():
    assert 1 + 1 == 2

def test_string():
    s = "Hello world"
    assert "world" in s


def test_list_operations():
    items = [1, 2, 3]
    assert len(items) == 3
    assert 2 in items
    assert items[0] == 1

def test_dict_validation():
    user = {"name": "Alice", "role": "SDET"}
    assert user["role"] == "SDET"
    assert "email" not in user

@pytest.mark.xfail
def test_assert_fail():
    assert 1 + 1 == 3

@pytest.mark.smoke
def test_smoke_test():
    print("smoke test..")
    assert True

@pytest.mark.smoke
def test_smoke_test2():
    print("smoke test2..")
    assert True

@pytest.mark.regression
def test_regression():
    print("regression test")
    assert True

@pytest.mark.skip(reason="Feature not comleted yet")
def test_upcoming_feature():
    pass

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        a = 1/0
