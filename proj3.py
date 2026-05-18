from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None  = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)

def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    
    if index ==0:
        return heap

    parent_index = (index - 1) // 2
    parent_node = heap.data[parent_index]
    current_node = heap.data[index]

    if parent_node <= current_node:
        return heap
        
    new_data = heap.data[:]
    temp = new_data[index]
    new_data[index] = new_data[parent_index]
    new_data[parent_index] = temp

    new_heap = MinHeap(new_data)

    return heapify_up(new_heap, parent_index)

def insert(heap: MinHeap, element: Node) -> MinHeap:
    new_data = heap.data + [element]

    new_heap = MinHeap(new_data)

    last_index = (len(new_data) - 1)

    return heapify_up(new_heap, last_index)

def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    length = len(heap.data)
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    smallest = index

    if left_index < length and heap.data[left_index] < heap.data[smallest]:
        smallest = left_index

    # Change <= to <
    if right_index < length and heap.data[right_index] < heap.data[smallest]:
        smallest = right_index

    if smallest == index:
        return heap

    new_data = heap.data[:]
    temp = new_data[index]
    new_data[index] = new_data[smallest]
    new_data[smallest] = temp

    new_heap = MinHeap(new_data)

    return heapify_down(new_heap, smallest)


def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    if not heap.data:
        raise IndexError("Heap is empty")
    if len(heap.data) == 1:
        return MinHeap([]), heap.data[0]
    
    min_node = heap.data[0]

    new_data = [heap.data[-1]] + heap.data[1:-1]
    new_heap = MinHeap(new_data)

    fixed_heap = heapify_down(new_heap, 0)

    return (fixed_heap, min_node)

        
def count_frequency(s: str)-> dict[str,int]:
    counts = {}

    for char in s:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    
    return counts


def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    
    heap = MinHeap()

    for char, freq in frequency.items():
        new_node = Node(freq, char)
        heap = insert(heap, new_node)
    
    return heap


def build_tree_from_queue(priority_queue: MinHeap) -> Node:
    heap = priority_queue

    if len(heap.data) == 0:
        return Node(0, "")

    while len(heap.data) > 1:
        heap, left_node = extract_min(heap)
        heap, right_node = extract_min(heap)
        parent_node = Node(left_node.freq + right_node.freq, left_node.char + right_node.char, left_node, right_node)
        heap = insert(heap, parent_node)

    return heap.data[0]

def generate_codes(node: Node | None, prefix: str = "") -> dict:
    if node is None:
        return {}

    # Check for a leaf node structurally
    if node.left is None and node.right is None:
        # Check if it's the dummy node for an empty string!
        if node.char == "":
            return {}
        return {node.char: prefix or "0"}

    left_codes = generate_codes(node.left, prefix + "0")
    right_codes = generate_codes(node.right, prefix + "1")

    # Functionally merge and return the dictionaries
    return {**left_codes, **right_codes}


def encode(s: str, codes: dict)-> str:
    return "".join(codes[char] for char in s)


def decode(encoded_string: str, root: Node):
    if root.left is None and root.right is None:
        return root.char * len(encoded_string)

    decoded_chars = []
    current_node = root

    for bit in encoded_string:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        # Check for a leaf node structurally
        if current_node.left is None and current_node.right is None:
            decoded_chars.append(current_node.char)
            current_node = root

    return "".join(decoded_chars)

def huffman_encoding(s:str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string,root)
    return encoded_string, decoded_string, codes

