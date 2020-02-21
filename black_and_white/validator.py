from dataclasses import astuple

import networkx as nx
from more_itertools import flatten

from black_and_white.models import Quest
from black_and_white.sequentially_deduplicate import sequentially_deduplicate


def check_has_start_label(quest: Quest):
    """Quest must have a "start" label which the user will see first."""
    if 'start' not in quest:
        raise ValueError('Quest does not have "start" label.')


def check_for_undefined_labels(quest: Quest):
    """Look for redirects to labels which do not exist."""
    for edge in quest.edges():
        if edge.destination not in quest:
            raise ValueError(
                f'#{edge.source} redirects the user to #{edge.destination}, ' +
                f'which does not exist in the quest.',
            )


def check_for_cycles(quest: Quest):
    """Detect if Quest graph contains cycles."""
    # noinspection PyDataclass
    graph = nx.DiGraph(
        astuple(edge) for edge in quest.edges()
    )

    try:
        cycle = nx.find_cycle(graph)

    except nx.NetworkXNoCycle:
        return

    else:
        cycle_sequence = ' -> '.join(sequentially_deduplicate(flatten(cycle)))

        raise ValueError(
            f'There is a cycle in quest graph, which means the user might ' +
            f'never find a way out of the quest: {cycle_sequence}.',
        )


def check_for_unused_labels(quest: Quest):
    """Determine cases when a label in a quest is unused."""
    edges = quest.edges()

    total_labels, called_labels = zip(*map(astuple, edges))

    unused_labels = set(total_labels) - set(called_labels) - {'start'}

    if unused_labels:
        raise ValueError(unused_labels)
