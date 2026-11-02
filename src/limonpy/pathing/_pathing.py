"""General helper functions."""
########################################################################
# region Setup
########################################################################

from __future__ import annotations

# Imports ==============================================================

# Standard
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.resources.abc import Traversable

# Config ===============================================================

logger = logging.getLogger(__name__)


# endregion
########################################################################
# region Locating key directories
########################################################################


def find_project_root(
    start: Path | str | None = None, sentinels: Sequence[str] | None = None
) -> Path:
    r"""Walk up from ``start`` (default: cwd) to find the project root.

    The root is the nearest ancestor directory containing any of
    ``sentinels``.

    Parameters
    ----------
    start : Path or str, default ``Path.cwd()``
        Starting directory for project root walk-up search.
    sentinels : Sequence of str, default ('.git', 'pyproject.toml')
        File/directory names that denote a project root.

    Raises
    ------
    FileNotFoundError
        No directory above ``start`` contains ``sentinels``.
    """
    if sentinels is None:
        sentinels: tuple[str, ...] = ('.git', 'pyproject.toml')
    elif isinstance(sentinels, str):
        # Silently support single str input
        sentinels: tuple[str, ...] = (sentinels,)
    elif not isinstance(sentinels, Sequence):
        msg: str = (
            'sentinels must be list[str] | tuple[str] | set[str]. '
            f'Got type: {type(sentinels)}'
        )
        raise TypeError(msg)

    cwd: Path = Path(start or Path.cwd()).resolve()
    for directory in (cwd, *cwd.parents):
        if any((directory / s).exists() for s in sentinels):
            logger.debug(
                'Found project root at %s using sentinels %s',
                directory,
                sentinels,
            )
            return directory

    msg: str = f'No valid project root found above: {cwd!s}.'
    raise FileNotFoundError(msg)


# endregion
