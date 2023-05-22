"""
File: linkedbst.py
Author: Ken Lambert
"""

import time
from random import sample
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            final_string = ""
            if node is not None:
                final_string += recurse(node.right, level + 1)
                final_string += "| " * level
                final_string += str(node.data) + "\n"
                final_string += recurse(node.left, level + 1)
            return final_string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            liftMaxInLeftSubtreeToTop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def children(self, peek: BSTNode):
        """Generate an iteration of Positions representing p's children."""
        if peek.left is not None:
            yield peek.left
        if peek.right is not None:
            yield peek.right

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        root = self._root
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            else:
                return 1 + max(height1(c) for c in self.children(top))
        return height1(root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        vertices_counter = 0
        for _ in self.inorder():
            vertices_counter += 1
        tree_height = self.height()
        return tree_height < (2 * log(vertices_counter + 1, 2) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        between_array = []
        index = 0
        for value in self.inorder():
            if value >= low and value <= high:
                between_array.append(value)
                index += 1
        return between_array

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        inorder_list = self.inorder()
        self.clear()
        linked_stack = LinkedStack()
        for element in inorder_list:
            linked_stack.push(element)
        def helper(new_stack):
            middle_index = None
            if len(new_stack) == 2:
                self.add(new_stack.pop())
                self.add(new_stack.pop())
            elif len(new_stack) == 1:
                self.add(new_stack.pop())
            else:
                middle = len(new_stack) // 2
                left_stack = LinkedStack()
                right_stack = LinkedStack()
                for index, element in enumerate(new_stack):
                    if index == middle:
                        middle_index = True
                        self.add(element)
                    elif middle_index is None:
                        left_stack.push(element)
                    elif middle_index is True:
                        right_stack.push(element)
                helper(left_stack)
                helper(right_stack)
        helper(linked_stack)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        min_value = float('inf')
        inorder = self.inorder()
        for value in inorder:
            if value > item and value < min_value:
                min_value = value
        if min_value == float('inf'):
            return None
        return min_value

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        max_value = float('-inf')
        inorder = self.inorder()
        for value in inorder:
            if value < item and value > max_value:
                max_value = value
        if max_value == float('-inf'):
            return None
        return max_value

    def new_add(self, item):
        """Adds item to the tree without recursion."""
        node = self._root
        while node.right is not None:
            node = node.right
        node.right =  BSTNode(item)

    def new_find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise. Works without
        recursion."""
        node = self._root
        while node is not None:
            if item == node.data:
                return node.data
            else:
                node = node.right

    def new_rebalance(self):
        """Rebalance a tree without recursion."""
        inorder_list = self.inorder()
        self.clear()
        new_inorder_list = []
        for element in inorder_list:
            new_inorder_list.append(element)
        curr_list = [new_inorder_list]
        while len(curr_list) != 0:
            middle = len(curr_list[0]) // 2
            self.add(curr_list[0][middle])
            left_list = curr_list[0][:middle]
            right_list = curr_list[0][middle+1:]
            curr_list.pop(0)
            if len(left_list) != 0:
                curr_list.append(left_list)
            if len(right_list) != 0:
                curr_list.append(right_list)

    def demo_bst(self, path):
        """Demonstration of efficiency binary search tree for the search tasks."""
        #read a file
        with open(path, 'r', encoding='UTF-8') as file:
            read_file = file.readlines()
        new_read_file = []
        for element in read_file:
            new_read_file.append(element.strip())
        #---------------------------------------------
        #count time 1
        start_time_1 = time.time()
        words = sample(new_read_file, 10000)
        new_words = []
        for word in sorted(new_read_file):
            if word in words:
                new_words.append(word)
        end_time_1 = time.time()
        time_1 = end_time_1 - start_time_1
        #---------------------------------------------
        tree1 = LinkedBST()
        index1 = 0
        #create a sorted tree
        for element in sorted(new_read_file):
            if index1 == 0:
                tree1._root = BSTNode(element)
                index1 += 1
            else:
                tree1.new_add(element)
        #count time 2
        start_time_2 = time.time()
        for word in words:
            tree1.new_find(word)
        end_time_2 = time.time()
        time_2 = end_time_2 - start_time_2
        #---------------------------------------------
        tree2 = LinkedBST()
        index2 = 0
        #create a non-sorted tree
        for element in sample(new_read_file, len(new_read_file)):
            if index2 == 0:
                tree2._root = BSTNode(element)
                index2 += 1
            else:
                tree2.add(element)
        #count time 3
        start_time_3 = time.time()
        new_words_1 = []
        for word in tree2:
            if word in words:
                new_words_1.append(word)
        end_time_3 = time.time()
        time_3 = end_time_3 - start_time_3
        #---------------------------------------------
        new_words_2 = []
        tree2.new_rebalance()
        #count time 4
        start_time_4 = time.time()
        for word in tree2:
            if word in words:
                new_words_2.append(word)
        end_time_4 = time.time()
        time_4 = end_time_4 - start_time_4
        final_result = f'{time_1} - час пошуку 10000 випадкових слів у впорядкованому за \
абеткою словнику\n{time_2} - час пошуку 10000 випадкових слів у впорядкованому словнику, \
який представлений у вигляді бінарного дерева пошуку\n{time_3} - час пошуку 10000 випадкових \
слів у невпорядкованому словнику, який представлений у вигляді бінарного дерева пошуку\n\
{time_4} - час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного \
дерева пошуку після його балансування'
        return final_result

if __name__ == "__main__":
    #example of output for a smaller file
    tree = LinkedBST()
    print(tree.demo_bst('small_words.txt'))
