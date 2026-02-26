import csv
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class HomeWork2:

    # Problem 1: Construct an expression tree (Binary Tree) from a postfix expression
    # input -> list of strings (e.g., [3,4,+,2,*])
    # this is parsed from p1_construct_tree.csv (check it out for clarification)

    # there are no duplicate numeric values in the input
    # support basic operators: +, -, *, /

    # output -> the root node of the expression tree. Here: [*,+,2,3,4,None,None]
    # Tree Node with * as root node, the tree should be as follows
    #         *
    #        / \
    #       +   2
    #      / \
    #     3   4

    def constructBinaryTree(self, input_list) -> TreeNode:
        if not input_list:
            return None
        
        stack = []
        operators = {'+', '-', '*', '/'}
        
        for token in input_list:
            # Strip whitespace to handle cases like ' 4' or ' +' 
            clean_token = token.strip()
            
            if clean_token not in operators:
                # Operand: Push a new leaf node onto the stack
                stack.append(TreeNode(token))
            else:
                # Operator: Pop two nodes and make them children
                # Error check: ensure there are enough operands 
                if len(stack) < 2:
                    continue 
                
                new_node = TreeNode(token)
                new_node.right = stack.pop()  # First pop is the right child
                new_node.left = stack.pop()   # Second pop is the left child
                stack.append(new_node)
        
        # The last remaining node on the stack is the root 
        return stack.pop() if stack else None




    # Problem 2.1: Use pre-order traversal (root, left, right) to generate prefix notation
    # return an array of elements of a prefix expression
    # expected output for the tree from problem 1 is [*,+,3,4,2]
    # you can see the examples in p2_traversals.csv

    def prefixNotationPrint(self, head: TreeNode) -> list:
        if not head:
            return []
        return [head.val] + self.prefixNotationPrint(head.left) + self.prefixNotationPrint(head.right)

    # Problem 2.2: In-order traversal (Infix) with parentheses 
    def infixNotationPrint(self, head: TreeNode) -> list:
        if not head:
            return []
        # If it's a leaf node (operand), just return its value 
        if head.left is None and head.right is None:
            return [head.val]
        
        # Wrapping the expression in parentheses as required 
        return (['('] + self.infixNotationPrint(head.left) + 
                [head.val] + 
                self.infixNotationPrint(head.right) + [')'])

    # Problem 2.3: Post-order traversal (Postfix)
    def postfixNotationPrint(self, head: TreeNode) -> list:
        if not head:
            return []
        return self.postfixNotationPrint(head.left) + self.postfixNotationPrint(head.right) + [head.val]

class Stack:
    def __init__(self):
        # Using a list as underlying storage but managing 'top' manually 
        self.storage = []
        self.top = -1 

    def push(self, val):
        self.storage.append(val)
        self.top += 1

    def pop(self):
        if self.top < 0:
            raise IndexError("Pop from empty stack")
        val = self.storage.pop()
        self.top -= 1
        return val

    # Problem 3: Evaluate postfix expression using the custom stack 
    def evaluatePostfix(self, exp: str) -> int:
        # Requirement: input is a space-separated string 
        tokens = exp.split()
        operators = {'+', '-', '*', '/'}
        
        for token in tokens:
            if token not in operators:
                # Convert string to integer for evaluation 
                self.push(int(token))
            else:
                # Pop operands for the operation
                b = self.pop()
                a = self.pop()
                
                if token == '+': self.push(a + b)
                elif token == '-': self.push(a - b)
                elif token == '*': self.push(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero") 
                    # Use integer division or truncation as per standard postfix eval
                    self.push(int(a / b))
        
        return self.pop()


# Main Function. Do not edit the code below
if __name__ == "__main__":
    homework2 = HomeWork2()

    print("\nRUNNING TEST CASES FOR PROBLEM 1")
    testcases = []
    try:
        with open('p1_construct_tree.csv', 'r') as f:
            testcases = list(csv.reader(f))
    except FileNotFoundError:
        print("p1_construct_tree.csv not found")

    for i, (postfix_input,) in enumerate(testcases, 1):
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)
        output = homework2.postfixNotationPrint(root)

        assert output == postfix, f"P1 Test {i} failed: tree structure incorrect"
        print(f"P1 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 2")
    testcases = []
    with open('p2_traversals.csv', 'r') as f:
        testcases = list(csv.reader(f))

    for i, row in enumerate(testcases, 1):
        postfix_input, exp_pre, exp_in, exp_post = row
        postfix = postfix_input.split(",")

        root = homework2.constructBinaryTree(postfix)

        assert homework2.prefixNotationPrint(root) == exp_pre.split(","), f"P2-{i} prefix failed"
        assert homework2.infixNotationPrint(root) == exp_in.split(","), f"P2-{i} infix failed"
        assert homework2.postfixNotationPrint(root) == exp_post.split(","), f"P2-{i} postfix failed"

        print(f"P2 Test {i} passed")

    print("\nRUNNING TEST CASES FOR PROBLEM 3")
    testcases = []
    try:
        with open('p3_eval_postfix.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                testcases.append(row)
    except FileNotFoundError:
        print("p3_eval_postfix.csv not found")

    for idx, row in enumerate(testcases, start=1):
        expr, expected = row

        try:
            s = Stack()
            result = s.evaluatePostfix(expr)
            if expected == "DIVZERO":
                print(f"Test {idx} failed (expected division by zero)")
            else:
                expected = int(expected)
                assert result == expected, f"Test {idx} failed: {result} != {expected}"
                print(f"Test case {idx} passed")

        except ZeroDivisionError:
            assert expected == "DIVZERO", f"Test {idx} unexpected division by zero"
            print(f"Test case {idx} passed (division by zero handled)")