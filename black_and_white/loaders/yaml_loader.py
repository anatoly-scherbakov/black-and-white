from pathlib import Path
from typing import Dict, Optional, TypedDict, Union

import yaml

from black_and_white.models import Banner, Choice, Quest, Question


class BannerDict(TypedDict):
    """YAML format description of Banner."""

    title: str
    content: Optional[str]  # noqa: WPS110
    goto: Optional[str]


def deserialize_banner(banner: BannerDict) -> Banner:
    """Convert a dict into Banner object."""
    return Banner(**banner)


class QuestionDict(TypedDict):
    """YAML format description of Question."""

    title: str
    content: Optional[str]    # noqa: WPS110
    choices: Dict[str, str]


def deserialize_question(
    question: QuestionDict
) -> Question:
    """Convert a dict into Question object."""
    return Question(
        title=question['title'],
        content=question.get('content'),
        choices=[
            Choice(
                title=title,
                goto=goto
            )
            for title, goto in question['choices'].items()
        ]
    )


def load_from_file(filepath: Union[str, Path]) -> Quest:
    """Load quest in YAML format from a file and output Quest object."""
    with open(filepath, 'r') as quest_file:
        quest_content = yaml.safe_load(quest_file)

    return Quest(
        (label, (
            deserialize_question(question_or_banner)
            if 'choices' in question_or_banner
            else deserialize_banner(question_or_banner)
        ))
        for label, question_or_banner
        in quest_content.items()
    )
