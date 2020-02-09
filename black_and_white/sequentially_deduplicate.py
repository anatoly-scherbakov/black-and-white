from typing import Iterable, TypeVar, Union

ItemType = TypeVar('ItemType')


class Sentinel:
    """Sentinel object."""


def sequentially_deduplicate(
    iterable: Iterable[ItemType]
) -> Iterable[ItemType]:
    """
    Remove sequential duplicates.

        ..pycon
        >>> list(sequentially_deduplicate([1, 3, 1, 1, 8, 1]))
        [1, 3, 8, 1]
    """
    sentinel = Sentinel()
    previous_item: Union[Sentinel, ItemType] = sentinel

    for item in iterable:   # noqa: WPS110 - this is an item of an iterable
        if item not in {previous_item, sentinel}:
            yield item

        previous_item = item
