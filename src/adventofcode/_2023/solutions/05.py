from adventofcode._templates.v20231204.puzzle_to_solve import PuzzleToSolve
from typing import List, Tuple
import re

class Alamanc:
    
    sources: List[int]
    maps: List[List[Tuple[int, int, int]]]
    
    def __init__(self, parsed_input: Tuple[List[int], List[List[Tuple[int, int, int]]]]):
        self.sources, self.maps = parsed_input

    def find_closest_location(self):
        """
        Brute-force solution for part a). 
        - Loop over each map, for each map
        - Loop voer each source. For each source
        - Loop over each map-entry. For each map-entry
        - If the source is in the range of the map-entry, calculate the new source
        - Repeat until all map entries are applied to each of the sources
        - Return the minimum source
        """
        sources = self.sources
        for map in self.maps:
            new_sources = []
            for source in sources:
                new_source = source
                for dest_range_start, source_range_start, range_len in map:
                    if source_range_start <= source < source_range_start + range_len:
                        new_source = dest_range_start + (source - source_range_start)
                        break
                new_sources.append(new_source)
            sources = new_sources
            print("Done one map")
        return min(sources)

    def map_if_possible(self, source_range_start, source_range_len, mapped_dest_range_start, mapped_source_range_start, range_len) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        """
        Check if the source_range can be mapped to the mapped_dest_range. If so, return the mapped_dest_range and the remaining ranges to be mapped. If not, return None and the source_range
        
        Args:
            source_range_start (int): Start of the source range (the to-be-mapped range)
            source_range_len (int): Length of the source range (the to-be-mapped range)
            mapped_dest_range_start (int): Start of the mapped dest range (the range to which the source range is mapped)
            mapped_source_range_start (int): Start of the mapped source range (the start part of the source that are mapped by this map-entry)
            range_len (int): Length of the mapped source range (mapped_source_range_start + range_len is the full source range that is mapped by this map-entry)
        Returns:
            Tuple[Tuple[int, int], List[Tuple[int, int]]]: The mapped dest range and the remaining ranges to be mapped. If the source range cannot be mapped, return None and the source range
        """
        # If the end of the source range is before the start of the mapped source range, or the start of the source range is after the end of the mapped source range, there is no overlap
        if source_range_start + source_range_len <= mapped_source_range_start or mapped_source_range_start + range_len <= source_range_start:
            return None, [(source_range_start, source_range_len)]
        else:
            # Some part overlaps, so we need to map this part
            # The start of the matching part is the max of the start of the mapped source range and the start of the source range
            matched_part_start = max(mapped_source_range_start, source_range_start)
            # The end of the matching part is the min of the end of the mapped source range and the end of the source range
            matched_part_end = min(mapped_source_range_start + range_len, source_range_start + source_range_len)
            # The length of the matching part is the difference between the start and the end
            matched_part_len = matched_part_end - matched_part_start
            # Map the start of the matching part to the value in the mapped dest range
            matched_part_start_in_dest = mapped_dest_range_start + (matched_part_start - mapped_source_range_start)
            # The dest range is the start value mapped in the dest range, and the length of the matching part
            matched_dest_range = matched_part_start_in_dest, matched_part_len
            
            # If the match is not a complete match (ie start or end of the source does not fall in the dest), we need to compute and return the remaining ranges
            remaining_ranges = []
            # If the source range has some values before the matched part
            if matched_part_start > source_range_start:
                # Add the part before the start of the matched part to the remaining ranges
                remaining_ranges.append((source_range_start, matched_part_start - source_range_start))
            # If the source range has some values after the matched part
            if matched_part_end < source_range_start + source_range_len:
                # Add the part after the end of the matched part to the remaining ranges
                remaining_ranges.append((matched_part_end, source_range_start + source_range_len - matched_part_end))
            return matched_dest_range, remaining_ranges
    
    def find_closest_location_given_ranges(self):
        """
        Smarter solution for part b). Use ranges instead of looping over each source
        - Convert the sources into range. A range is a tuple, (start, len)
        - Loop over each map, for each map
        - Loop over each range_to_be_mapped. For each range_to_be_mapped
        - Loop over each map-entry. For each map-entry
        - If the range_to_be_mapped is (partly) in the range of the map-entry, map that part. The unmapped parts are added to the unmapped_ranges, to be mapped by subsequent map-entries of this map
        - If all entries of a map are applied, the mapped_ranges + the unmapped_ranges are the new ranges_to_be_mapped. This makes the unmapped_ranges to be mapped to themselves in this map
        - If all maps are applied, all ranges have been mapped. The result are the ranges mapped through all maps
        - Return the start of the range with the lowest start
        """
        sources = self.sources
        source_ranges = [(sources[i], sources[i+1]) for i in range(0, len(sources), 2)]
        ranges_to_map = source_ranges
        for map in self.maps:
            mapped_ranges = []
            for mapped_dest_range_start, mapped_source_range_start, range_len in map:
                # Keep track of the ranges that are not mapped by this map-entry
                unmapped_ranges = []
                # Try to map each range_to_map
                for source_range_start, source_range_len in ranges_to_map:
                    # Map if possible
                    mapped_range, remaining_ranges = self.map_if_possible(source_range_start, source_range_len, mapped_dest_range_start, mapped_source_range_start, range_len)
                    # Add the part that can be mapped by this map-entry to the mapped_ranges
                    if mapped_range:
                        mapped_ranges.append(mapped_range)
                    # The parts that are not mapped, are added to the unmapped_ranges
                    unmapped_ranges.extend(remaining_ranges)
                # All source ranges that were mappable by this map-entry are now mapped.
                # The remaining ranges are only the unmapped ranges, as each unmapped range was added to this list
                ranges_to_map = unmapped_ranges
            # All map entries are applied to all ranges_to_map. We now have the mapped ranges and the ranges that still need to be mapped. 
            # The ranges that are still to be mapped are mapped to their original value, hence ranges_to_map = mapped_ranges + ranges_to_map
            ranges_to_map = mapped_ranges + ranges_to_map
        # All maps are applied to all ranges_to_map. We now have the mapped ranges and the ranges that still need to be mapped. Return the start of the range with the lowest start
        return min(ranges_to_map, key=lambda x: x[0])[0]

class Puzzle5(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 5
    
    @property
    def year(self) -> int:
        return 2023

    @property
    def test_input(self) -> str:
        return """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    @property
    def test_answer_a(self):
        return 35

    @property
    def test_answer_b(self):
        return 46

    def parse_input(self, input_: str) -> Tuple[List[int], List[List[Tuple[int, int, int]]]]:
        """
        Parse the input. Harcode all available maps, as they are equal for test- and actual-input.
        Convert the seeds into a list of ints
        Convert the maps into a list of lists of tuples of ints
        Return a tuple, with the list of seeds and the list of maps
        """
        regex = r"seeds: (.*)\n\nseed-to-soil map:\n([\s\S]*?)\n\nsoil-to-fertilizer map:\n([\s\S]*?)\n\nfertilizer-to-water map:\n([\s\S]*?)\n\nwater-to-light map:\n([\s\S]*?)\n\nlight-to-temperature map:\n([\s\S]*?)\n\ntemperature-to-humidity map:\n([\s\S]*?)\n\nhumidity-to-location map:\n([\s\S]*)"
        if not re.match(regex, input_):
            raise ValueError(f"Invalid input: {input_}")
        
        groups = re.search(regex, input_).groups()
        sources, maps = groups[0], groups[1:]
        sources = [int(x) for x in sources.split()]
        maps = [[tuple(int(y) for y in x.split()) for x in map.splitlines()] for map in maps]
        return sources, maps

    def a(self, input_: Tuple[List[int], List[List[Tuple[int, int, int]]]]):
        """
        Apply the brute-force solution for part a)
        """
        alamanc = Alamanc(input_)
        return alamanc.find_closest_location()

    def b(self, input_: Tuple[List[int], List[List[Tuple[int, int, int]]]]):
        """
        Apply the smarter solution for part b). This solution will also convert the sources into ranges instead of a list of ints
        """
        sources, maps = input_
        alma = Alamanc((sources, maps))
        return alma.find_closest_location_given_ranges()


puzzle = Puzzle5()
puzzle.solve()
