
def insert_at_nth(self, index: int, data):
    """
        Adds data to a list. The index can by any number,
        and self is a regular list type.
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
        Takes binary numbers and makes them into an
        actual number. This doesn't handle negative binary values
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
            Prints all of th enodes in a linked list. We can do this via
            simple iteration. Starting vertix is the node in the list
            we print first.
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
