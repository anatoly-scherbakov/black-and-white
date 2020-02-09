from dataclasses import astuple
from typing import Iterable, TypeVar, Union

import networkx as nx
from more_itertools import flatten

from .models import Quest

T = TypeVar('T')


def check_has_start_label(quest: Quest):
    return 'start' in quest


def check_for_undefined_labels(quest: Quest):
    for edge in quest.edges():
        assert edge.destination in quest, (
            f'#{edge.source} redirects the user to #{edge.destination}, '
            f'which does not exist in the quest.'
        )


class Sentinel:
    pass


def sequentially_deduplicate(iterable: Iterable[T]) -> Iterable[T]:
    """
    Remove sequential duplicates.

        ..pycon
        >>> list(sequentially_deduplicate([1, 3, 1, 1, 8, 1]))
        [1, 3, 8, 1]
    """
    sentinel = Sentinel()
    previous_item: Union[Sentinel, T] = sentinel

    for item in iterable:
        if (
            item != previous_item
            and item != sentinel
        ):
            yield item

        previous_item = item


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
        cycle_sequence = sequentially_deduplicate(flatten(cycle))

        raise ValueError(
            f'There is a cycle in quest graph, which means the user might '
            f'never find a way out of the quest: {" -> ".join(cycle_sequence)}.'
        )


def check_for_unused_labels(quest: Quest):
    ...
