import pytest

from black_and_white.models import Banner, Choice, Quest, Question


@pytest.fixture()
def quest_without_cycles():
    """A sample quest."""
    return Quest(
        start=Question(title='What is your name?', choices=[
            Choice(title='John', goto='john'),
            Choice(title='Jane', goto='jane'),
        ]),
        john=Banner(title='Hi John!'),
        jane=Banner(title='Hi Jane!'),
    )


@pytest.fixture()
def quest_with_cycles():
    """A sample quest with a cycle in it."""
    return Quest(
        start=Question(title='What is your name?', choices=[
            Choice(title='John', goto='john'),
            Choice(title='Jane', goto='jane'),
        ]),
        john=Banner(title='Hi John!', goto='start'),
        jane=Banner(title='Hi Jane!', goto='start'),
    )
