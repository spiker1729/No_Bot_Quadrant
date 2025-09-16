
def format_number(num):
    '''Format a number with commas.'''
    return f"{num:,}"

def validate_input(value):
    '''Validate that input is a number.'''
    try:
        float(value)
        return True
    except ValueError:
        return False
