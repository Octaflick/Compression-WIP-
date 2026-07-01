from __future__ import annotations

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from typing import Optional


@dataclass
class HuffmanNode:
    ch: Optional[str]
    freq: int
    left: Optional["HuffmanNode"] = None
    right: Optional["HuffmanNode"] = None

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


class HuffmanTreeBuilder:
    def build(self, frequencies: dict[str, int]) -> Optional[HuffmanNode]:
        heap: list[tuple[int, int, HuffmanNode]] = []
        unique = count()

        for ch, freq in frequencies.items():
            heappush(heap, (freq, next(unique), HuffmanNode(ch, freq)))

        if not heap:
            return None

        while len(heap) > 1:
            left_freq, _, left_node = heappop(heap)
            right_freq, _, right_node = heappop(heap)
            merged = HuffmanNode(None, left_freq + right_freq, left_node, right_node)
            heappush(heap, (merged.freq, next(unique), merged))

        return heappop(heap)[2]


class HuffmanDecoder:
    def __init__(self, root: Optional[HuffmanNode] = None) -> None:
        self.root = root

    def set_tree(self, root: Optional[HuffmanNode]) -> None:
        self.root = root

    def decode(self, encoded_bits: str) -> str:
        if self.root is None:
            raise ValueError("Huffman tree is empty")

        decoded: list[str] = []
        current = self.root

        for bit in encoded_bits:
            if bit not in "01":
                continue

            current = current.left if bit == "0" else current.right

            if current is None:
                raise ValueError("Invalid encoded string: walked into a missing branch")

            if current.is_leaf():
                if current.ch is None:
                    raise ValueError("Invalid Huffman tree: leaf without a character")
                decoded.append(current.ch)
                current = self.root

        if current is not self.root:
            raise ValueError("Invalid encoded string: trailing incomplete Huffman code")

        return "".join(decoded)


if __name__ == "__main__":
    frequencies = {"A": 1, "B": 1, "C": 1}

    builder = HuffmanTreeBuilder()
    root = builder.build(frequencies)

    decoder = HuffmanDecoder(root)
    encoded = "01011"

    print(decoder.decode(encoded))
