def sumvalues(values: list)-> int or float:
    """
    Calculates the sum of all numbers in a list.

    Arguments:
        values (list): list of numbers
    Returns:
        sum (int | float): sum of all numbers
    Raises:
        TypeError: Non-numerical elements found in list
    """
    try:
        if values == []:    # Returns none if list is empty
            return None
        elif all(type(n) in (int, float) for n in values):    # Checks if there are any non-numerical values
            sum = 0
            for i in values:
                sum = sum + i
        else:
            raise TypeError ("Non-numerical elements found in list")
    except TypeError as e:
        print(e)
    return sum

def maxvalue(values: list)-> int:
    """
    Finds the index of the largest number in a list.

    Arguments:
        values (list): list of numbers
    Returns:
        index (int): index of largest number
    Raises:
        TypeError: Non-numerical elements found in list
    """
    try:
        if values == []:    # Returns none if list is empty
            return None
        elif all(type(n) in (int, float) for n in values):    # Checks if there are any non-numerical values
            index = 0
            largest = values[0]     # Holds the largest element when iterating over a list. Default value = first element
            for i in range(len(values)):
                if values[i] > largest:
                    index = i
                    largest = values[i]
        else:
            raise TypeError ("Non-numerical elements found in list")
    except TypeError as e:
        print(e)
    return index

def minvalue(values: list)-> int:
    """
    Finds the index of the smallest number in a list.

    Arguments:
        values (list): list of numbers
    Returns:
        index (int): index of smallest number
    Raises:
        TypeError: Non-numerical elements found in list
    """
    try:
        if values == []:    # Returns none if list is empty
            return None
        elif all(type(n) in (int, float) for n in values):    # Checks if there are any non-numerical values
            index = 0
            smallest = values[0]     # Holds the smallest element when iterating over a list. Default value = first element
            for i in range(len(values)):
                if values[i] < smallest:
                    index = i
                    smallest = values[i]
        else:
            raise TypeError("Non-numerical elements found in list")
    except TypeError as e:
        print(e)
    return index

def meannvalue(values: list)-> int or float:
    """
    Calculates the mean of all numbers in a list.

    Arguments:
        values (list): list of numbers
    Returns:
        mean (int | float): sum of all numbers
    Raises:
        TypeError: Non-numerical elements found in list
    """
    try:
        if values == []:    # Returns none if list is empty
            return None
        if all(type(n) in (int, float) for n in values):    # Checks if there are any non-numerical values
            sum = 0
            for i in values:
                sum = sum + i
            mean = sum / len(values) #Divides sum of list by number of elements in list
        else:
            raise TypeError ("Non-numerical elements found in list")
    except TypeError as e:
        print(e)
    return mean
    
def countvalue(values: list, x)-> int:
    """
    Finds the number of occurences of a target value x in a list

    Arguments:
        values (list): list of elements
        x: target value
    Returns:
        occurs (int): number of occurences of x
    """
    occurs = 0  
    for i in values:    # Counts the number of occurences of x
        if x == i:
            occurs = occurs + 1
    return occurs

def sorted(values:list) -> list:
    """
    Sorts the list from smallest to largest value
        Uses the merge-sort algorithm: Divides list into subarrays and sorts by comparison across subarrays

    Arguments:
        values (list): list of elements
    Returns:
        values (list): sorted list
    """
    if len(values) > 1:                                 
        centre = len(values) // 2
        left = values[:centre]
        right = values[centre:]

        sorted(left)                                    # Recursive call breaks down the current left and right arrays into their own halves (until one element left)
        sorted(right)
        i = j = k = 0

        while i < len(left) and j < len(right):         # Compares values in order across left and right array, places smallest value in values array first
            if left[i] < right[j]:                  
                values[k] = left[i]
                i = i + 1
            else:
                values[k] = right[j]
                j = j + 1
            k = k + 1
        
        while i < len(left):                        # Places remaining elements in left array if all values in right array have been placed                        
            values[k] = left[i]
            i = i + 1
            k = k + 1
        
        while j < len(right):                       # Places remaining elements in right array if all values in left array have been placed 
            values[k] = right[j]
            j = j + 1
            k = k + 1
    return values
