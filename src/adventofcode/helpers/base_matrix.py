from dataclasses import dataclass
from typing import Generator, List, Tuple

import numpy as np
from pydantic import BaseModel, Field


class Position(BaseModel):
    i: int
    j: int

    def __add__(self, other) -> "Position":
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


@dataclass
class Direction(Position):
    i: int = Field(None, ge=-1, le=1)
    j: int = Field(None, ge=-1, le=1)

    def __post_init__(self):
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


class BaseMatrix:
    """
    Matrix class, to be used as a base class for other matrix classes
    Parses input into a numpy matrix, and provides some helper functions

    Attributes:
        data: the numpy matrix
        pad: the padding used to surround the matrix
    """

    data: np.ndarray
    pad: str

    def parse_input(self, input_: str, pad: str = ".", caster: callable = str):
        """
        Input string to numpy matrix. Surround matrix with pad, to make sure we don't get index errors

        Args:
            input_: input string
            pad: padding to add to the matrix. If None, no padding is added
        """
        self.pad = pad
        self.data = np.array([list(line) for line in input_.split("\n")], dtype=caster)
        if pad is not None:
            self.data = np.pad(self.data, 1, constant_values=pad)

    def __getitem__(self, item: Tuple[int, int] | Position) -> str:
        if isinstance(item, Position):
            return self.data[item.i, item.j]
        return self.data[item]

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
        return "\n".join(["".join(line) for line in self.data])
