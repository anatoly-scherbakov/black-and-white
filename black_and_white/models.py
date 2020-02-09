from pydantic import dataclasses
from typing import Optional, List, Dict, Union, Generator, Iterable


@dataclasses.dataclass(frozen=True)
class Choice:
    title: str
    goto: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class QuestItem:
    title: str

    @property
    def directions(self) -> List[str]:
        raise NotImplementedError(
            f'Implement {self.__class__.__name__}.directions property.'
        )


@dataclasses.dataclass(frozen=True)
class Question(QuestItem):
    choices: List[Choice]
    content: Optional[str] = None

    @property
    def directions(self) -> List[str]:
        return [
            choice.goto
            for choice
            in (self.choices or [])
        ]


@dataclasses.dataclass(frozen=True)
class Banner(QuestItem):
    content: Optional[str] = None
    goto: Optional[str] = None

    @property
    def directions(self) -> List[str]:
        if self.goto:
            return [self.goto]
        else:
            return []


@dataclasses.dataclass(frozen=True)
class Edge:
    source: str
    destination: str


class Quest(Dict[str, Union[Banner, Question]]):
    def edges(self) -> Iterable[Edge]:
        """Returns the sequence of edges in the quest items graph."""
        for source, item in self.items():
            for destination in item.directions:
                yield Edge(source=source, destination=destination)
