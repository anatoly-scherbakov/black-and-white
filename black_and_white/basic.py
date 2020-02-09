from pathlib import Path
from typing import Optional

import colorama

from black_and_white.loaders.yaml_loader import load_from_file
from black_and_white.models import Banner, Quest, Question

bold = colorama.Style.BRIGHT
reset = colorama.Style.RESET_ALL
red = colorama.Fore.RED


def validate_response(raw_response: str, question: Question) -> Optional[int]:
    """Check that user's response is valid."""
    try:
        response = int(raw_response)

    except ValueError:
        print(f'{red}Пожалуйста, введите целое число.{reset}')
        return None

    if response < 0:
        print(f'{red}Ответ должен быть положительным числом.{reset}')
        return None

    if len(question.choices) < response:
        print(
            f'{red}Пожалуйста, введите число ' +
            f'от 1 до {len(question.choices)}.{reset}'
        )
        return None

    return response


def ask_question(question: Question) -> str:
    """Ask question and return the label to go to."""
    while True:
        raw_response = input('> ')   # noqa: WPS421, S322

        response = validate_response(
            raw_response=raw_response,
            question=question
        )

        if response is not None:
            return question.choices[response - 1].goto


def render_question(question: Question):
    """Display question on console and get answer."""
    print(f'{bold}{question.title}{reset}')

    if question.content:
        print(question.content)

    for choice_id, choice in enumerate(question.choices, start=1):
        print(f'  {choice_id}. {choice.title}')

    return ask_question(question)


def render_banner(banner: Banner):
    """Display the banner on console."""
    print(f'{bold}{banner.title}{reset}')

    if banner.content:
        print(banner.content)

    return banner.goto


def run(quest: Quest, label: str):
    """Run the quest."""
    banner_or_question = quest[label]

    if isinstance(banner_or_question, Question):
        goto = render_question(banner_or_question)

    elif isinstance(banner_or_question, Banner):
        goto = render_banner(banner_or_question)

    else:
        raise ValueError(
            f'{banner_or_question} is neither a Banner nor a Question.'
        )

    if goto is not None:
        return run(quest, label=goto)


def main() -> None:
    """Entry point of the application."""
    filepath = Path(
        __file__
    ).parent.parent.joinpath(
        'scripts/blockchain-cheat-sheet-ru.yml'
    )

    quest = load_from_file(filepath)

    run(quest, label='start')


if __name__ == '__main__':
    main()
