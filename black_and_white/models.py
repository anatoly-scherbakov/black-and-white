from pydantic import dataclasses
from typing import Optional, List, Dict, Union


@dataclasses.dataclass(frozen=True)
class Choice:
    title: str
    goto: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class QuestItem:
    title: str
    content: Optional[str] = None


@dataclasses.dataclass(frozen=True)
class Question(QuestItem):
    choices: Optional[List[Choice]] = None


@dataclasses.dataclass(frozen=True)
class Banner(QuestItem):
    goto: Optional[str] = None


class Quest(Dict[str, Union[Banner, Question]]):
    pass
