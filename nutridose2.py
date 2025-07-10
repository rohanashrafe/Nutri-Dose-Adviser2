
class Node:
    def __init__(self, parameter, value, recommendation):
        self.parameter = parameter
        self.value = value
        self.recommendation = recommendation
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, parameter, value, recommendation):
        node = Node(parameter, value, recommendation)
        if not self.head:
            self.head = node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = node

    def display(self):
        temp = self.head
        while temp:
            print(f"{temp.parameter}: {temp.value} | Recommendation: {temp.recommendation}")
            temp = temp.next

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            temp = self.head
            while temp:
                file.write(f"{temp.parameter}: {temp.value} | Recommendation: {temp.recommendation}\n")
                temp = temp.next

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def is_empty(self):
        return not self.items

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def is_empty(self):
        return not self.items


NORMAL_RANGES = { 'Hemoglobin': (12.0, 17.5), 'Vitamin D': (20.0, 50.0), 'Calcium': (8.5, 10.5), 'Iron': (60.0, 170.0), 'Vitamin B12': (200, 900), 'Magnesium': (1.7, 2.2) }

RECOMMENDATIONS = { 'Hemoglobin': 'Take Iron supplements 15 mg/day', 'Vitamin D': 'Take Vitamin D3 2000 IU/day or sunlight exposure', 'Calcium': 'Consume dairy products and calcium supplements', 'Iron': 'Eat iron-rich foods like spinach, red meat', 'Vitamin B12': 'Take Vitamin B12 supplement or consume eggs/meat', 'Magnesium': 'Eat magnesium-rich foods like nuts, leafy greens' }


def check_deficiency(param, value):
    low, high = NORMAL_RANGES[param]
    if value < low:
        return f"Low {param}: {RECOMMENDATIONS[param]}"
    elif value > high:
        return f"High {param}: Adjust diet and consult physician"
    else:
        return None

def process_data(data):
    ll = LinkedList()
    q = Queue()

    for param, val in data.items():
        rec = check_deficiency(param, val)
        if rec:
            ll.add_node(param, val, rec)
            q.enqueue(rec)

    return ll, q

def read_data_from_file(filepath):
    data = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[0] in NORMAL_RANGES:
                    try:
                        data[parts[0].strip()] = float(parts[1].strip())
                    except ValueError:
                        print(f"Invalid value for {parts[0]}")
    except FileNotFoundError:
        print("File not found.")
    return data


def main():
    print("=== Example Data Processing ===\n")
    example_data = { 'Hemoglobin': 10.5, 'Vitamin D': 15, 'Calcium': 7.8, 'Iron': 55, 'Vitamin B12': 150, 'Magnesium': 1.4 }

    ll, q = process_data(example_data)
    ll.display()

    print("\nRecommendations Queue:")
    while not q.is_empty():
        print("->", q.dequeue())

    file_name = input("\nEnter file name to save example results: ")
    ll.save_to_file(file_name)

    # ------------------ User Input Section ------------------

    print("\n=== Enter Your Own Data ===")
    user_data = {}

    for param in NORMAL_RANGES:
        try:
            val = float(input(f"Enter your {param} level: "))
            user_data[param] = val
        except ValueError:
            print("Invalid input, skipping this parameter.")

    ll, q = process_data(user_data)

    print("\nYour Results:")
    ll.display()

    print("\nYour Recommendations:")
    while not q.is_empty():
        print("->", q.dequeue())

    file_name = input("\nEnter file name to save your results: ")
    ll.save_to_file(file_name)

    # ------------------ File Input Section ------------------

    print("\n=== File Input ===")
    file_path = input("Enter the path of your data file (.txt): ")
    file_data = read_data_from_file(file_path)

    ll, q = process_data(file_data)

    print("\nResults from File:")
    ll.display()

    print("\nRecommendations from File:")
    while not q.is_empty():
        print("->", q.dequeue())

    file_name = input("\nEnter file name to save results from file: ")
    ll.save_to_file(file_name)

if __name__ == "__main__":
    main()

