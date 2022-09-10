'''
Given a binary tree, return the product of the largest value in each level of the tree
'''

# Ask questions -
# How is the tree represented? Node struct? (val, left, right)
# Ask about calculating product, and whether overflow matters?
# If root is null, return 0?

# BFS w/ queue and keep track of largest var. Multiply running product by largest var.

def tree_product(root):
    if not root:
        return 0
    
    product = 1
    queue = collections.deque([root])
    
    while queue:
        largest_val = float('-inf')
        
        for _ in range(len(queue)):
            node = queue.popleft()
            
            largest_val = max(node.val, largest_val)
            
            if node.left:
                queue.append(node.left)
                
            if node.right:
                queue.append(node.right)
        
        product *= largest_val
    
    return product

