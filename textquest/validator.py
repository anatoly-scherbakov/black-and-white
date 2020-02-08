from textquest.models import Quest, Question, Banner


def check_has_start_label(quest: Quest):
    return 'start' in quest


def check_for_undefined_labels(quest: Quest):
    for label, item in quest.items():
        if isinstance(item, Question):
            for i, choice in enumerate(item.choices, start=1):
                assert choice.goto in quest, (
                    f'Question #{label} redirects the user to #{choice.goto} '
                    f'if the user chooses the answer #{i}, but that item does '
                    f'not exist in the quest.'
                )

        elif isinstance(item, Banner):
            assert item.goto in quest, (
                f'Banner #{label} redirects the user to #{item.goto} which '
                f'does not exist in the quest.'
            )


def check_for_cycles(quest: Quest):
    ...


def check_for_unused_labels(quest: Quest):
    ...
