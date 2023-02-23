"""
Fibonacci heap implementation.
"""

from typing import List, Any
from math import log

class FibonacciHeap:
    """
    Fibonacci heap implementation.
    """

    class Node:
        """
        Node class for the Fibonacci heap.
        """
        def __init__(self, key) -> None:
            """
            Initialize the node.
            """
            self.key = key
            self.parent = None
            self.child = None
            self.left = self
            self.right = self
            self.degree = 0
            self.mark = False

        def __repr__(self) -> str:
            """
            Return a string representation of the node.
            """
            return str(self.key)

        def siblings(self) -> List[Any]:
            """
            Return a list of the node's siblings.
            """
            if self.left == self:
                return [self]
            else:
                sibs = [self.left]
                current = self.left
                while current != self:
                    sibs.append(current.left)
                    current = current.left
                return sibs

        def add(self, node) -> None:
            """
            Add a node to the right of the current node.
            """
            node.left = self.left
            node.right = self
            self.left.right = node
            self.left = node

        def remove(self) -> None:
            """
            Remove the current node from the list.
            """
            self.left.right = self.right
            self.right.left = self.left

    def __init__(self) -> None:
        """
        Initialize the heap.
        """
        self.min = None
        self.num_nodes = 0

    def __len__(self) -> int:
        """
        Return the number of nodes in the heap.
        """
        return self.num_nodes

    def insert(self, key: Any) -> None:
        """
        Insert a new node into the heap.
        """
        node = self.Node(key)
        if self.min is not None:
            self.min.add(node)

            if key < self.min.key:
                self.min = node
        else:
            self.min = node

        self.num_nodes += 1

    def minimum(self) -> Any:
        """
        Return the minimum node.
        """
        return self.min.key

    def extract_minimum(self) -> Any:
        """
        Remove and return the minimum node.
        """
        min_node = self.min

        if min_node is not None:
            if min_node.child is not None:
                for rnode in min_node.child.siblings():
                    rnode.parent = None
                    self.min.add(rnode)

            min_node.remove()

            if min_node == min_node.right:
                self.min = None
            else:
                self.min = min_node.right
                self.__consolidate()

            self.num_nodes -= 1
            return min_node.key

        return None

    def __consolidate(self) -> None:
        """
        Consolidate the heap.
        """
        deg_list = [None] * int(log(self.num_nodes) * 2)
        nodes = self.min.siblings()

        for node in nodes:
            xnode = node
            node_deg = xnode.degree
            while deg_list[node_deg] is not None:
                ynode = deg_list[node_deg]
                if xnode.key > ynode.key:
                    xnode, ynode = ynode, xnode
                self.__link(ynode, xnode)
                deg_list[node_deg] = None
                node_deg += 1
            deg_list[node_deg] = xnode

        for deg_node in deg_list:
            if deg_node is not None:
                if not self.min:
                    self.min = deg_node
                    deg_node.right = deg_node.left = deg_node
                else:
                    self.min.add(deg_node)
                    if deg_node.key < self.min.key:
                        self.min = deg_node

    def __link(self, node1: Node, node2: Node) -> None:
        """
        Link two nodes.
        """
        node1.remove()
        node1.parent = node2

        if node2.child is None:
            node1.left = node1.right = node1
            node2.child = node1
        else:
            node2.child.add(node1)

        node2.degree += 1
        node1.mark = False

    def decrease_key(self, node: Node, new_key: Any) -> None:
        """
        Decrease the key of a node by a certain amount.
        """
        if new_key > node.key:
            return

        node.key = new_key
        parent = node.parent

        if parent is not None and node.key < parent.key:
            self.__cut(node, parent)
            self.__cascading_cut(parent)

        if node.key < self.min.key:
            self.min = node

    def __cut(self, node, parent) -> None:
        """
        Cut a node from its parent.
        """
        node.remove()
        if node.right == node:
            parent.child = None

        parent.degree -= 1
        self.min.add(node)
        node.parent = None
        node.mark = False

    def __cascading_cut(self, node) -> None:
        """
        Cut a node from its parent and perform the same operation on its parent.
        """
        parent = node.parent
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self.__cut(node, parent)
                self.__cascading_cut(parent)

    def delete(self, node) -> None:
        """
        Delete a node from the heap.
        """
        self.decrease_key(node, float('-inf'))
        self.extract_minimum()
