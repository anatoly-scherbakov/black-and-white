import pytest

from black_and_white.validator import check_for_cycles


def test_no_cycles(quest_without_cycles):
    check_for_cycles(quest_without_cycles)


def test_has_cycles(quest_with_cycles):
    with pytest.raises(ValueError) as err:
        check_for_cycles(quest_with_cycles)

        assert str(err.value) == (
            'There is a cycle in quest graph, which means the user ' +
            'might never find a way out of the quest: start -> john -> start.'
        )
