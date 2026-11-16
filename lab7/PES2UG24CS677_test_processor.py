from hypothesis import given, strategies as st
from processor import process_name, process_age, process_tags


@given(st.one_of(st.text(), st.none(), st.integers()))
def test_process_name_does_not_crash(value):
    result = process_name(value)
    assert isinstance(result, str)


@given(st.one_of(st.text(), st.none(), st.integers()))
def test_process_age_does_not_crash(value):
    result = process_age(value)
    assert result is None or isinstance(result, int)


@given(st.one_of(
    st.lists(st.text()),
    st.none(),
    st.integers()
))
def test_process_tags_does_not_crash(value):
    result = process_tags(value)
    assert isinstance(result, list)
