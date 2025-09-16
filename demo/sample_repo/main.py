
def calculate_sum(a, b):
    '''Calculate the sum of two numbers.'''
    return a + b

def calculate_product(a, b):
    '''Calculate the product of two numbers.'''
    return a * b

def main():
    '''Main function that uses other functions.'''
    result = calculate_sum(5, 3)
    print(f"Sum: {result}")
    
    product = calculate_product(4, 6)
    print(f"Product: {product}")

if __name__ == "__main__":
    main()
