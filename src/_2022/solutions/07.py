import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from src._2022.puzzle_to_solve import PuzzleToSolve


@dataclass
class Node:
    name: str
    parent: 'Node' = None
    children: Dict[str, 'Node'] = field(default_factory=lambda: {})
    size: int = 0

    def parse_input(self, remaining_input: List[str]):
        if not remaining_input:
            return
        item = remaining_input.pop(0)
        if item.startswith('$ cd'):
            new_node = self.parse_cd(item)
        elif item.startswith('$ ls'):
            new_node = self.parse_ls(item)
        elif item.startswith('dir'):
            new_node = self.parse_dir(item)
        else:
            new_node = self.parse_file(item)
        new_node.parse_input(remaining_input)

    def parse_cd(self, line: str):
        name = line[5:]
        if name == '..':
            return self.parent
        else:
            return self.children[name]

    def parse_ls(self, line: str):
        return self

    def parse_dir(self, line: str):
        name = line[4:]
        child = Node(name=name, parent=self)
        self.children[name] = child
        return self

    def parse_file(self, line: str):
        size, name = re.search("(\d+) (.*)", line).groups()
        size = int(size)
        child = Node(name=name, parent=self, size=size)
        self.children[name] = child
        return self

    def get_directories_of_at_most_size(self, size: int):
        result = []
        if self.total_size <= size and self.is_dir:
            result.append(self)
        for child in self.children.values():
            result.extend(child.get_directories_of_at_most_size(size))
        return result

    @property
    def is_dir(self):
        return len(self.children) > 0

    @property
    def total_size(self):
        return self.size + sum([x.total_size for x in self.children.values()])

    def get_all_dirs(self):
        if self.children:
            result = [self]
            for child in self.children.values():
                result.extend(child.get_all_dirs())
            return result
        return []


class Puzzle7(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 7

    @property
    def test_input(self) -> str:
        return """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

    @property
    def test_answer_a(self):
        return 95437

    @property
    def test_answer_b(self):
        return 24933642

    def create_tree(self, input: str):
        """
        Create the tree:
        - Assert the first item is cd /
        - Create the root note, and let it parse the rest of the input
        """
        items = input.split('\n')
        first = items.pop(0)
        assert first == '$ cd /'
        root = Node(name='/')
        root.parse_input(items)
        return root

    def a(self, input_: str):
        """
        Solve a):
        - Create the tree
        - From the tree, get all (nested) directories of at most size max_size
        - Sum the sizes of the found dirs
        """
        max_size = 100000
        tree = self.create_tree(input_)
        result = tree.get_directories_of_at_most_size(max_size)
        summed = sum([x.total_size for x in result])
        return summed

    def b(self, input_: str):
        """
        Solve b):
        - Create the tree
        - Compute the size to free, based on the current free size
        - Get the list of options to delete. These are the directories that are at least size to_free
        - Get the smallest option, return its size
        """
        max_size = 70000000
        wanted_free_size = 30000000
        tree = self.create_tree(input_)
        current_size = tree.total_size
        current_free = wanted_free_size - current_size
        to_free = 30000000 - current_free
        options = [x for x in tree.get_all_dirs() if x.total_size >= to_free]
        sorted_options = sorted(options, key=lambda x: x.total_size)
        item_to_delete = sorted_options[0]
        return item_to_delete.total_size


puzzle = Puzzle7()
puzzle.solve()
