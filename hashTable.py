class HashTable:
    """"
    Definition: 
    __init__ is a constructor method that is automatically called when an instance of a class is created.
    
    Parameters:
    self: A reference to the instance of the class.
    capacity (default value is 32): The initial capacity of the table.
    
    Return: 
    The __init__ method does not explicitly return a value; it initializes the instance of the class.
    """
    def __init__(self, capacity=32):
        self._capacity = capacity # Initialize table with given capacity
        self.size = 0 # Number of key-value pairs in the table
        self.table = [None] * self._capacity # Create empty table
    
    
    """
    Definition: 
    insert adds a key-value pair to the hash table.

    Parameters:
    key: The key to be inserted.
    value: The value associated with the key.
    
    Return: 
    Returns True if the key-value pair is successfully inserted; otherwise, returns False if the key already exists.
    """
    def insert(self, key, value):
        # Insert a key-value pair into the hash table.
        index = hash(key) % self._capacity # Compute hash index
        bucket = self.table[index] # Get the bucket at the index
        if bucket is not None:
            for item in bucket:
                if item[0] == key:
                    return False # Key already exists

            bucket.append((key, value)) # Add new key-value pair
        else:
            self.table[index] = [(key, value)] # Create new bucket with pair

        self.size += 1 # Increment size

        if self.size / self._capacity > 0.7:
            self._resize() # Resize table if load factor exceeds threshold

        return True
    
    """
    Definition: 
    modify updates the value associated with a given key in the hash table.
    
    Parameters:
    key: The key whose associated value is to be modified.
    value: The new value to associate with the key.
    
    Return: 
    Returns True if the key was found and its value was updated; otherwise, returns False.
    """
    def modify(self, key, value):
        # Modify the value associated with the given key.
        index = hash(key) % self._capacity # Compute hash index
        bucket = self.table[index] # Get the bucket at the index
        
        if bucket is not None:
            for i in range(len(bucket)):
                if bucket[i][0] == key:
                    bucket[i] = (key, value) # Update existing value
                    return True
        return False
    
    """
    Definition: 
    remove deletes a key-value pair from the hash table based on the provided key.
    
    Parameters:
    key: The key whose associated key-value pair is to be removed.
    
    Return: 
    Returns True if the key was found and the pair was successfully removed; otherwise, returns False.
    """
    def remove(self, key):
        # Remove the key-value pair associated with the given key.
        index = hash(key) % self._capacity # Compute hash index
        if self.table[index] is not None:
            for i, item in enumerate(self.table[index]):
                if item[0] == key:
                    self.table[index].pop(i) # Remove item from bucket
                    if len(self.table[index]) == 0:
                        self.table[index] = None # Clear empty bucket
                    self.size -= 1 # Decrement size
                    return True
        return False
    
    """
    Definition: 
    search retrieves the value associated with a specified key from the hash table.
    
    Parameters:
    key: The key whose associated value is to be searched for.
    
    Return: 
    Returns the value associated with the key if it is found; otherwise, returns None.
    """
    def search(self, key):
        # Search for the value associated with the given key.
        index = hash(key) % self._capacity # Compute hash index
        if self.table[index] is not None:
            for item in self.table[index]:
                if item[0] == key:
                    return item[1] # Return the value if key is found
        return None
    
    """
    Definition: 
    Returns the current capacity of the hash table.
    
    Return: 
    The value of _capacity, which indicates the number of slots available in the hash table.
    """
    def capacity(self):
        # Return the current capacity of the hash table.
        return self._capacity
    
    """
    Definition: 
    Returns the number of key-value pairs currently stored in the hash table.
    
    Return: 
    The value of size, representing the count of key-value pairs in the hash table.
    """
    def __len__(self):
        # Return the number of records in the hash table.
        return self.size
    
    """
    Definition: 
    _resize adjusts the size of the hash table when the load factor exceeds a specified threshold, usually to improve performance by reducing collisions.
    """
    def _resize(self):
        # esize the hash table when the load factor exceeds the threshold.
        prev_table = self.table # Save current table
        prev_capacity = self._capacity # Save current capacity
        self._capacity *= 2 # Double the capacity
        self.table = [None] * self._capacity # Create new table
        self.size = 0 # Reset size

        for chaining in prev_table:
            if chaining is not None:
                for key, value in chaining:
                    self.insert(key, value) # Reinsert all items into the new table
