#!/bin/python

# class Item(object):
#     def __init__(self, value):
#         self.value = value
#         self.below = None
#         self.above = None
    
class Stack(object):
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()
    
    def get_stack(self):
        # return ''.join(self.items)
        return self.items
    
    def is_empty(self):
        return self.items == []
    
    def peek(self):
        return self.items[-1]

def test1():
    s = Stack()
    print(s.is_empty())
    s.push("A")
    s.push("B")
    s.push("C")
    print(s.is_empty())
    s.push("D")
    s.push("E")
    print(s.get_stack())
    s.pop()
    s.pop()
    print(s.peek())
    print(s.get_stack())
    s.pop()
    print(s.get_stack())

def test2(str_in):
    list_in = list(str_in)
    sqr_stack = Stack()
    crl_stack = Stack()
    crv_stack = Stack()

    for par in list_in:
        if par == "[":
            sqr_stack.push("square")
        elif par == "]":
            sqr_stack.pop()
        else:
            pass
        if par == "{":
            crl_stack.push("square")
        elif par == "}":
            crl_stack.pop()
        else:
            pass
        if par == "(":
            crv_stack.push("square")
        elif par == ")":
            crv_stack.pop()
        else:
            pass

    print(sqr_stack.get_stack())
    print(crv_stack.get_stack())
    print(crl_stack.get_stack())

def test3(dec_num):
    bin_stack = Stack()
    dec_num = abs(dec_num)
    
    while dec_num > 0:
        if dec_num % 2 == 0:
            bin_stack.push(0)
        else:
            bin_stack.push(1)
        dec_num = dec_num // 2
    
    print(bin_stack.get_stack())
    
def main():
    # test1()
    # test2("[[[]{}((((()")
    test3(242)

if __name__ == "__main__":
    main()