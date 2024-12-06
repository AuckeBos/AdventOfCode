from dataclasses import dataclass
from enum import Enum
from typing import Any, Generator, List, Tuple, Union

import numpy as np


@dataclass
class Position:
    i: int
    j: int

    def __add__(self, other: Union["Position", "Direction"]) -> "Position":
        return Position(self.i + other.i, self.j + other.j)

    @property
    def tuple_(self) -> tuple[int, int]:
        return self.i, self.j

    def direction_of(self, other: "Position") -> "Direction":
        return Direction(*(other - self).tuple_)

    @classmethod
    def directions(
        self, *, include_axis: bool = True, include_diagonal: bool = True
    ) -> List["Direction"]:
        directions = []
        if include_axis:
            directions += [
                Direction(0, 1),
                Direction(1, 0),
                Direction(0, -1),
                Direction(-1, 0),
            ]
        if include_diagonal:
            directions += [
                Direction(1, 1),
                Direction(1, -1),
                Direction(-1, 1),
                Direction(-1, -1),
            ]
        return directions

    @property
    def neighbors(
        self, *, include_axis: bool = True, include_diagonal: bool = True
    ) -> List["Position"]:
        return [
            self + d
            for d in self.directions(
                include_axis=include_axis, include_diagonal=include_diagonal
            )
        ]


class Direction(Position):
    def __post_init__(self):
        if abs(self.i) > 1 or abs(self.j) > 1:
            raise ValueError("i and j cannot be greater than 1")
        if self.i == 0 and self.j == 0:
            raise ValueError("i and j cannot both be 0")

    def turn_right(self) -> "Direction":
        if abs(self.i) == abs(self.j):
            raise ValueError(
                f"Can only turn on horizontal / vertical directions, not {self.tuple_}"
            )
        return {
            (-1, 0): Direction(0, 1),
            (0, 1): Direction(1, 0),
            (1, 0): Direction(0, -1),
            (0, -1): Direction(-1, 0),
        }[self.tuple_]

    def turn_left(self):
        return self.turn_right().turn_right().turn_right()

    def reverse(self):
        return Direction(-self.i, -self.j)


class Directions(Enum):
    TOP: Direction = Direction(-1, 0)
    RIGHT: Direction = Direction(0, 1)
    BOTTOM: Direction = Direction(1, 0)
    LEFT: Direction = Direction(0, -1)


class BaseMatrix:
    """
    Matrix class, to be used as a base class for other matrix classes
    Parses input into a numpy matrix, and provides some helper functions

    Attributes:
        data: the numpy matrix
        pad: the padding used to surround the matrix
    """

    data: np.matrix
    pad: str
    input_: str
    dtype: type

    def __init__(self, input_: str = None, pad: str = ".", dtype: type = str):
        self.input_ = input_
        self.pad = pad
        self.dtype = dtype
        self.data = np.matrix([list(line) for line in input_.split("\n")], dtype=dtype)
        if pad is not None:
            self.data = np.pad(self.data, 1, constant_values=pad)

    def __getitem__(self, item: Tuple[int, int] | Position) -> str:
        if isinstance(item, Position):
            return self.data[item.i, item.j]
        return self.data[item]

    def __setitem__(self, key: tuple[int, int] | Position, value: Any) -> None:
        if isinstance(key, Position):
            key = key.tuple_
        if not self.is_in_bounds(Position(*key)):
            raise ValueError(f"Index {key} is out of bounds")
        self.data[key] = value

    def is_in_bounds(self, position: Position) -> bool:
        return (
            0 <= position.i < self.data.shape[0]
            and 0 <= position.j < self.data.shape[1]
        )

    def iter_topleft_to_bottomright(self) -> Generator[Position, None, None]:
        """
        Yield all indices from top left to bottom right. Do not iterate of the pad
        """
        start_at = 1 if self.pad is not None else 0
        yield from [
            Position(i, j)
            for i in range(start_at, self.data.shape[0] - (start_at))
            for j in range(start_at, self.data.shape[1] - (start_at))
        ]

    def adjacent_fields(
        self,
        field: Position,
        *,
        include_axis: bool = True,
        include_diagonal: bool = True,
    ) -> Generator[Position, None, None]:
        yield from [
            field + d
            for d in Position.directions(
                include_axis=include_axis, include_diagonal=include_diagonal
            )
            if self.is_in_bounds(field + d)
        ]

    def adjacent_values(
        self,
        field: Position,
        *,
        include_axis: bool = True,
        include_diagonal: bool = True,
    ) -> List[str]:
        return [
            self[d]
            for d in self.adjacent_fields(
                field, include_axis=include_axis, include_diagonal=include_diagonal
            )
        ]

    def __repr__(self):
        return "\n".join(["".join(line) for line in np.array(self.data)])

    def __copy__(self):
        return BaseMatrix(self.input_, pad=self.pad, dtype=self.dtype)
