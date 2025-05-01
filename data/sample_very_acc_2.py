
def insert_at_nth(self, index: int, data):
    """
        Inserts data into a linked list, indicated by self, at
        the specified index. Assures that self is not None, and has conditions
        that allows for inserting at the tail or head given the respective index. Otherwise,
        it loops through the nodes until we reach the node at the index.
    
    """
    length = len(self)

    if not 0 <= index <= length:
        raise IndexError("list index out of range")
    new_node = Node(data)
    if self.head is None:
        self.head = self.tail = new_node
    elif index == 0:
        self.head.previous = new_node
        new_node.next = self.head
        self.head = new_node
    elif index == length:
        self.tail.next = new_node
        new_node.previous = self.tail
        self.tail = new_node
    else:
        temp = self.head
        for _ in range(index):
            temp = temp.next
        temp.previous.next = new_node
        new_node.previous = temp.previous
        new_node.next = temp
        temp.previous = new_node
def bin_to_decimal(bin_string: str) -> int:
    """
        Converts binary in a string format into a decimal number. The string is error checked if it exists or if
        it contains anything but 0's and 1's. The negative symbol '-' leads the string to indicate if the binary
        code is negative, else it is positive. Initializes our return decimal return value to 0. Then, converts each char in the string to its 
        integer value, then adds it to the current decimal times 2
        
    """
    bin_string = str(bin_string).strip()
    if not bin_string:
        raise ValueError("Empty string was passed to the function")
    is_negative = bin_string[0] == "-"
    if is_negative:
        bin_string = bin_string[1:]
    if not all(char in "01" for char in bin_string):
        raise ValueError("Non-binary value was passed to the function")
    decimal_number = 0
    for char in bin_string:
        decimal_number = 2 * decimal_number + int(char)
    return -decimal_number if is_negative else decimal_number

def bfs(self, start_vertex: int) -> set[int]:
        """
            Iterates through a Graph structure via Breadth search. This is done by starting at
            the root node, and maintaining a queue that contains our visited nodes and a set that will be returned
            as the ordered of nodes visisted. Whenever the queue is not empty, we dequeue the node at visit itschild nodes, then we
            add them to our queue. When the queue is empty, we are done and return our set.
        
        """
        
        visited = set()

        
        queue: Queue = Queue()

        
        visited.add(start_vertex)
        queue.put(start_vertex)

        while not queue.empty():
            vertex = queue.get()

            
            for adjacent_vertex in self.vertices[vertex]:
                if adjacent_vertex not in visited:
                    queue.put(adjacent_vertex)
                    visited.add(adjacent_vertex)
        return visited
