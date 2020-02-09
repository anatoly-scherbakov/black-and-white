import dataclasses
from typing import Dict, Iterable, List, Optional, Union


@dataclasses.dataclass(frozen=True)
class Step:
    """Base class for a Question or a Banner."""

    title: str

    @property
    def directions(self) -> List[str]:
        """Labels this quest item can direct the user to."""
        raise NotImplementedError(
            f'Implement {self.__class__.__name__}.directions property.'
        )


@dataclasses.dataclass(frozen=True)
class Choice:
    """A question choice."""

    title: str
    goto: str


@dataclasses.dataclass(frozen=True)
class Question(Step):
    """A question with choices list."""

    choices: List[Choice]
    content: Optional[str] = None  # noqa: WPS110

    @property
    def directions(self) -> List[str]:
        """Question directs to a number of other items, one per Choice."""
        return list({
            choice.goto
            for choice
            in (self.choices or [])
            if choice.goto
        })


@dataclasses.dataclass(frozen=True)
class Banner(Step):
    """Just a text to display and optionally to direct to another step."""

    content: Optional[str] = None  # noqa: WPS110
    goto: Optional[str] = None

    @property
    def directions(self) -> List[str]:
        """Banner only directs to one other item, if it does."""
        if self.goto:
            return [self.goto]

        return []


@dataclasses.dataclass(frozen=True)
class Edge:
    """Link from one Question or Banner directing user to another."""

    source: str
    destination: str


class Quest(Dict[str, Union[Banner, Question]]):
    """Encapsulates a text Quest."""

    def edges(self) -> Iterable[Edge]:
        """Returns the sequence of edges in the quest items graph."""
        for source, banner_or_question in self.items():
            yield from (
                Edge(source=source, destination=destination)
                for destination in banner_or_question.directions
            )
