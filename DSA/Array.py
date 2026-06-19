class Array:
    def __init__(self,capacity):
        self.capacity = capacity
        self.arr = [0] * self.capacity
        self.size = 0

    def insert(self,index,value):
        if self.size < self.capacity and index >= 0 and index <= self.size:
            for i in range(self.size,index,-1):
                self.arr[i] = self.arr[i-1]
            self.arr[index] = value
            self.size += 1
        else:
            return False
        
    def delete(self,index):
        if index < self.size and index >= 0:
            for i in range(index,self.size-1):
                self.arr[i] = self.arr[i+1]
            self.size -= 1
        else:
            return False

    def display(self):
        print("Array element: ")
        for i in range(self.size):
            print(self.arr[i],end=" ")
        print()

    def get_size(self):
        return self.size

    def get_capacity(self):
        return self.capacity
    
    def search(self,value):
        for i in range(self.size):
            if self.arr[i] == value:
                return i
        return -1
    
    def set(self,index,value):
        if index >= 0 and index < self.size:
            self.arr[index] = value
        else:
            return False
        
    def get(self,index):
        if index >=0 and index < self.size:
            return self.arr[index]

        else:
            return False 
        
if __name__ == "__main__":
  array = Array(10)

  array.insert(0, 10)
  array.insert(1, 20)
  array.insert(2, 30)
  array.insert(1, 15)  # Insert in between

  array.display()  # Expected: 10 15 20 30

  array.set(2, 25)
  print("Element at index 2:", array.get(2))  # Expected: 25

  array.delete(1)
  array.display()  # Expected: 10 25 30

  print("Index of 30:", array.search(30)) 

