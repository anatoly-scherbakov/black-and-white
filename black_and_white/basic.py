from typing import Union, Dict, List, TypedDict, Optional

from yaml import load
from pathlib import Path

import colorama

from .models import Question, Banner, Quest, Choice

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper  # type: ignore


bold = colorama.Style.BRIGHT
reset = colorama.Style.RESET_ALL
red = colorama.Fore.RED


def render_question(question: Question):
    print(f'{bold}{question.title}{reset}')

    if question.content:
        print(question.content)

    while True:
        for i, choice in enumerate(question.choices, start=1):
            print(f'  {i}. {choice.title}')

        try:
            response = int(input('> '))
            print()

        except ValueError:
            print(f'{red}Пожалуйста, введите целое число.{reset}')
            continue

        if response < 0:
            print(f'{red}Ответ должен быть положительным числом.{reset}')
            continue

        try:
            return question.choices[response - 1].goto
        except IndexError:
            print(
                f'{red}Пожалуйста, введите число '
                f'от 1 до {len(question.choices)}.{reset}'
            )


def render_banner(banner: Banner):
    print(f'{bold}{banner.title}{reset}')

    if banner.content:
        print(banner.content)

    return banner.goto


def run(quest: Quest, label: str):
    item = quest[label]

    if isinstance(item, Question):
        goto = render_question(item)

    elif isinstance(item, Banner):
        goto = render_banner(item)

    else:
        raise ValueError(f'{item} is neither a Banner nor a Question.')

    if goto is not None:
        return run(quest, label=goto)


class BannerDict(TypedDict):
    title: str
    content: Optional[str]
    goto: Optional[str]


def deserialize_banner(data: BannerDict) -> Banner:
    return Banner(**data)


class QuestionDict(TypedDict):
    title: str
    content: Optional[str]
    choices: Dict[str, str]


def deserialize_question(
    data: QuestionDict
) -> Question:
    return Question(
        title=data['title'],
        content=data.get('content'),
        choices=[
            Choice(
                title=title,
                goto=goto
            )
            for title, goto in data['choices'].items()
        ]
    )


def load_from_file(filepath: Union[str, Path]) -> Quest:
    with open(filepath, 'r') as f:
        data = load(f, Loader=Loader)

    return Quest(
        (label, (
            deserialize_question(item)
            if 'choices' in item
            else deserialize_banner(item)
        ))
        for label, item
        in data.items()
    )


def main() -> None:
    filepath = Path(
        __file__
    ).parent.parent.joinpath(
        'scripts/blockchain-cheat-sheet-ru.yml'
    )

    quest = load_from_file(filepath)

    run(quest, label='start')


if __name__ == '__main__':
    main()
