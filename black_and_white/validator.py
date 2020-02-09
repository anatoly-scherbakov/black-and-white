from dataclasses import astuple
from functools import reduce

from more_itertools import flatten

from .models import Quest
import networkx as nx


def check_has_start_label(quest: Quest):
    return 'start' in quest


def check_for_undefined_labels(quest: Quest):
    for edge in quest.edges():
        assert edge.destination in quest, (
            f'#{edge.source} redirects the user to #{edge.destination}, '
            f'which does not exist in the quest.'
        )


def check_for_cycles(quest: Quest):
    # noinspection PyDataclass
    graph = nx.DiGraph(
        astuple(edge) for edge in quest.edges()
    )

    try:
        cycle = nx.find_cycle(graph)

    except nx.NetworkXNoCycle:
        ...

    else:
        cycle_sequence = reduce(
            lambda acc, label: acc if (
                acc
                and acc[-1] == label
            ) else acc + [label],
            flatten(cycle),
            []
        )

        raise ValueError(
            f'There is a cycle in quest graph, which means the user might '
            f'never find a way out of the quest: {" -> ".join(cycle_sequence)}.'
        )


def check_for_unused_labels(quest: Quest):
    ...
