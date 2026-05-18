import unittest
from proj3 import (
    Node, MinHeap, 
    heapify_up, insert, extract_min, build_tree_from_queue, 
    huffman_encoding
)

class TestStudentHuffman(unittest.TestCase):

    def test_heapify_up_independently(self):
        bad_heap = MinHeap([Node(2, 'a'), Node(5, 'b'), Node(1, 'c')])
        
        fixed_heap = heapify_up(bad_heap, 2)
        
        self.assertEqual(len(fixed_heap.data), 3)
        self.assertEqual(fixed_heap.data[0].char, 'c')
        self.assertEqual(bad_heap.data[2].char, 'c')

    def test_insert_independently(self):
        heap = MinHeap([Node(5, 'a')])
        new_node = Node(1, 'b')
        
        new_heap = insert(heap, new_node)
        
        self.assertEqual(len(new_heap.data), 2)
        self.assertEqual(new_heap.data[0].char, 'b')

    def test_extract_min_independently(self):
        heap = MinHeap([Node(1, 'a'), Node(5, 'b')])
        
        new_heap, min_node = extract_min(heap)
        
        self.assertEqual(min_node.char, 'a')
        self.assertEqual(len(new_heap.data), 1)
        self.assertEqual(new_heap.data[0].char, 'b')

    def test_tree_shape(self):
        pq = MinHeap([Node(2, 'a'), Node(3, 'b')])
        
        root = build_tree_from_queue(pq)
        
        self.assertIsNotNone(root, "Root should not be None")
        self.assertEqual(root.freq, 5, "Root frequency should be the sum of children (2+3)")
        self.assertIsNotNone(root.left, "Root must have a left child")
        self.assertIsNotNone(root.right, "Root must have a right child")
        self.assertIsNone(root.left.left, "Left child should be a leaf")
        self.assertIsNone(root.right.right, "Right child should be a leaf")

    def test_edge_case_empty_string(self):
        enc, dec, codes = huffman_encoding("")
        
        self.assertEqual(dec, "")
        self.assertEqual(enc, "")
        self.assertEqual(len(codes), 0)

    def test_edge_case_single_character(self):
        enc, dec, codes = huffman_encoding("a")
        
        self.assertEqual(dec, "a")
        self.assertEqual(len(codes), 1)
        self.assertEqual(len(codes['a']), 1)
        self.assertEqual(codes['a'], "0")

    def test_edge_case_repeated_characters(self):
        enc, dec, codes = huffman_encoding("bbbbb")
        
        self.assertEqual(dec, "bbbbb")
        self.assertEqual(enc, "00000")
        self.assertEqual(len(codes), 1)
        self.assertEqual(len(codes['b']), 1)


if __name__ == "__main__":
    unittest.main()