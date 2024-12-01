from typing import List, Tuple

import numpy as np
from aocd.models import Puzzle
from numpy.typing import NDArray

from helpers import parse_matrix, neighbours


class Packet:
    input: str
    version: int
    type_id: int

    # Only set if is_literal, else computed
    _value: int

    # Empty if self.is_literal
    sub_packets: List["Packet"]

    def __init__(self, input: str):
        self.input = input
        self.sub_packets = []
        self.parse_header()
        self.parse_body()

    def parse_header(self):
        self.version = self.get_input(3)
        self.type_id = self.get_input(3)

    def parse_body(self):
        if self.is_literal:
            self.parse_literal()
        else:
            self.parse_operator()

    def parse_literal(self):
        final_n = ""
        cur_n = self.get_input(5, False)
        while cur_n[0] == "1":
            final_n += cur_n[1:]
            cur_n = self.get_input(5, False)
        final_n += cur_n[1:]
        final_n = int(final_n, 2)
        self.value = final_n

    def parse_total_len_mode(self):
        sub_packets_len = self.get_input(15)
        input = self.get_input(sub_packets_len, False)
        while input != "":
            sub_packet = Packet(input)
            self.sub_packets.append(sub_packet)
            input = sub_packet.input

    def parse_mode_n_packets(self):
        n_packets = self.get_input(11)
        for _ in range(n_packets):
            sub_packet = Packet(self.input)
            self.sub_packets.append(sub_packet)
            self.input = sub_packet.input

    def parse_operator(self):
        self.sub_packets = []
        length_type_id = self.get_input(1, False)
        if length_type_id == "0":
            self.parse_total_len_mode()
        else:
            self.parse_mode_n_packets()

    # Get first n chars of input, and remove them from input. If as_int, return as int
    def get_input(self, n: int, as_int: bool = True):
        result = self.input[:n]
        self.input = self.input[n:]
        if as_int:
            result = int(result, 2)
        return result

    @property
    def is_literal(self):
        return self.type_id == 4

    @property
    def version_sum(self):
        return self.version + sum([p.version_sum for p in self.sub_packets])

    @property
    def value(self):
        if self.is_literal:
            return self._value
        values = [p.value for p in self.sub_packets]
        if self.type_id == 0:
            return sum(values)
        if self.type_id == 1:
            return np.prod(values)
        if self.type_id == 2:
            return min(values)
        if self.type_id == 3:
            return max(values)
        if self.type_id == 5:
            return int(values[0] > values[1])
        if self.type_id == 6:
            return int(values[0] < values[1])
        if self.type_id == 7:
            return int(values[0] == values[1])

    @value.setter
    def value(self, v):
        self._value = v


puzzle = Puzzle(year=2021, day=16)
hexa = puzzle.input_data
binary = "".join([bin(int(c, 16))[2:].zfill(4) for c in hexa])
packet = Packet(binary)
puzzle.answer_a = packet.version_sum
puzzle.answer_b = packet.value
