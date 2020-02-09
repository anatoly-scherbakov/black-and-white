from black_and_white.models import Quest, Question, Choice, Banner
from black_and_white.validator import check_for_cycles
import pytest


@pytest.fixture
def quest_without_cycles():
    return Quest(
        start=Question(title='What is your name?', choices=[
            Choice(title='John', goto='john'),
            Choice(title='Jane', goto='jane')
        ]),
        john=Banner(title='Hi John!'),
        jane=Banner(title='Hi Jane!'),
    )


@pytest.fixture
def quest_with_cycles():
    return Quest(
        start=Question(title='What is your name?', choices=[
            Choice(title='John', goto='john'),
            Choice(title='Jane', goto='jane')
        ]),
        john=Banner(title='Hi John!', goto='start'),
        jane=Banner(title='Hi Jane!', goto='start'),
    )


def test_no_cycles(quest_without_cycles):
    check_for_cycles(quest_without_cycles)


def test_has_cycles(quest_with_cycles):
    with pytest.raises(ValueError) as err:
        check_for_cycles(quest_with_cycles)

    assert str(err.value) == (
        'There is a cycle in quest graph, which means the user '
        'might never find a way out of the quest: start -> john -> start.'
    )
