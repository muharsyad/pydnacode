from typing import List, Dict, Optional

def message(length: int) -> list:
    # Check if 'length' is of type 'int'
    if not isinstance(length, int):
        # Raise a TypeError with a message if 'length' is not an integer
        raise TypeError("Argument 'length must be of type 'int'")
    
    # List to store binary vectors
    binary_vectors = []

    # Initialize the first binary vector with length n (all 0s)
    current_vector = [0]*length

    # Add the first binary vectors to the list
    binary_vectors.append(current_vector.copy())

    # Loop continues as long as the vector is not all 1s (last vector)
    while True:
        # Find the last index that is still 0
        # Start from the last index to the first index
        index = length - 1
        while index >= 0 and current_vector[index] == 1:
            index -= 1

        # If no index can be changed (all elements are 1s), stop the loop
        if index < 0:
            break

        # Change the element at the found index from 0 to 1    
        current_vector[index] = 1

        # Set all elements after the found index to 0
        for i in range(index + 1, length):
            current_vector[i] = 0
        
        # Add the updated binary vectors to the list
        binary_vectors.append(current_vector.copy())

    # Return the resulting list of binary vectors
    return binary_vectors

def codewords(message: List[List[int]], generator_matrix: List[List[int]]) -> List[List[int]]:
    """
    Compute codewords from the given message matrix and generator matrix.
    
    :param message: 2D list (message matrix) where each row is a binary vector
    :param generator_matrix: 2D list (generator matrix) where elements are binary (0 or 1)
    :return: 2D list (Codeword matrix) where each row is a binary vector
    :raises TypeError: If input are not of the correct types or contain non-integer element
    :raises ValueError: If input are not binary of dimensions are incompatible
    """
    
    # Check if message and generator_matrix are 2D list 
    if not all(isinstance(row, list) for row in message) or not all(isinstance(elem, int) for row in message for elem in row):
        raise TypeError("Message must be a 2D list of integers")
    
    if not all(isinstance(row, list) for row in generator_matrix) or not all(isinstance(elem, int) for row in generator_matrix for elem in row):
        raise TypeError("Generator matrix must be a 2D list of integers")
    
    # Check if all elements in message and generator_matrix are binary (0 or 1)
    if not all(elem in (0, 1) for row in message for elem in row):
        raise ValueError("Message must be binary (contain only 0s and 1s)")
    
    if not all(elem in (0, 1) for row in generator_matrix for elem in row):
        raise ValueError("Generator matrix must be binary (contain only 0s and 1s)")
    
    num_rows_message = len(message)
    num_cols_message = len(message[0])
    num_rows_generator = len(generator_matrix)
    num_cols_generator = len(generator_matrix[0])

    # Validate dimensions
    if not all(len(row) == num_cols_message for row in message):
        raise ValueError("All rows in the message matrix must have the same number of columns")
    
    if num_cols_message != num_rows_generator:
        raise ValueError("Number of rows in generator matrix mush be equal to number of columns in message")
    
    if not all(len(row) == num_cols_generator for row in generator_matrix):
        raise ValueError("All rows in generator matrix must have the same number of columns")
    
    # Initialize the codeword matrix with zeros
    codeword_matrix = [[0]*num_cols_generator for _ in range(num_rows_message)]

    # Compute the codeword matrix using matrix multiplication (mod 2)
    for i in range(num_rows_message):
        for j in range(num_cols_generator):
            for k in range(num_rows_generator):
                codeword_matrix[i][j] += message[i][k] * generator_matrix[k][j]
            codeword_matrix[i][j] %= 2
            
    return codeword_matrix

def hamming_distance(codeword1: List[int], codeword2: List[int]) -> int:
    """
    Compute the Hamming distance between two binary codeword.

    :param codeword1: First 1D list (binary vector) where each element is binary (0 or 1)
    :param codeword2: Second 1D list (binary vector) where each element is binary (0 or 1)
    :return: The Hamming distance between codeword1 and codeword2
    :raise TypeError: If input are not 1D lists or containe non-integer elements
    :raise ValueError: If elements are not binary or codewords have different lengths
    """

    # Check if both inputs are 1D lists
    if not (isinstance(codeword1, list) and isinstance(codeword2, list)):
        raise TypeError("Both arguments must be 1D lists")
    
    # Check if all elements in codeword1 and codeword2 are integers
    if not all(elem in (0, 1) for elem in codeword1) or not all(elem in (0, 1) for elem in codeword2):
        raise ValueError("Codewords must be binary (contain only 0s and 1s)")
    
    # Check if codeword1 and codeword2 have the same length
    if len(codeword1) != len(codeword2):
        raise ValueError("Codeword must be of the same length")
    
    # Compute the Hamming distance
    hamming_distance = 0
    length = len(codeword1)
    for i in range(length):
        if codeword1[i] != codeword2[i]:
            hamming_distance += 1

    return hamming_distance


def minimum_hamming_distance(code: List[List[int]]) -> int:
    """
    Determine the minimum Hamming distance of a binary code (a collection of binary codewords).

    :param code: 2D list (matrix of binary codewords) where each row is a binary vector
    :return: Minimum Hamming distance among all pairs of codewords
    :raise TypeError: If code is not a 2D list or contains non-integer elements
    :raise ValueError: If elements are not binary or rows are of different lengths
    """

    # Check if code is a 2D list and contains only binary elements
    if not all(isinstance(row, list) for row in code) or not all(isinstance(elem, int) for row in code for elem in row):
        raise TypeError("Code must be a 2D list of integers")
    
    if not all(elem in (0, 1) for row in code for elem in row):
        raise ValueError("Code must be binary (contain only 0s and 1s)")
    
    # Validate that all rows have the same length
    num_cols = len(code[0])
    if not all(len(row) == num_cols for row in code):
        raise ValueError("All codeword must have the same length")

    min_distance = float('inf')
    num_codewords = len(code)

    # Compute the minimum Hamming distance
    for i in range(num_codewords):
        for j in range(i+1, num_codewords):
            distance = hamming_distance(code[i], code[j])
            if distance < min_distance:
                min_distance = distance

    return min_distance

def weight_codeword(codeword: List[int]) -> int:
    """
    Calculate the weight of a binary vector.
    The weight is the number of non-zero elements in the codeword.

    :param codeword: 1D list (binary vector) where each element is binary (0 or 1)
    :return: The weight of the codeword, which is the number of 1s in the codeword
    :raise TypeError: If the input is not a 1D list or contains non-integer elements
    :raise ValueError: If elements are not binary
    """

    # Check if input is a 1D list
    if not isinstance(codeword, list):
        raise TypeError("Input must be a 1D list")
    
    # Check if all element in the codeword are integers
    if not all(isinstance(elem, int) for elem in codeword):
        raise TypeError("All elements in the codeword must be integers")
    
    # Check if all element in the codeword are binary (0 or 1)
    if not all(elem in (0, 1) for elem in codeword):
        raise ValueError("Codeword must be binary (contain only 0s and 1s)")
    
    # Compute the weigth of the codeword
    weight = sum(1 for i in codeword if i != 0)

    return weight

def weight_code(code: List[List[int]]) -> List[int]:
    """
    Calculate the weight of each binary codeword in a code (a collection of binary codeword).
    The weight of a codeword is the number of non-zero elements (1s) in the codeword.

    :param code: 2D list (a collection of binary codewords) where each row is a binary vectors
    :return: A list of weight, where each weight corresponds to the weight of a codewords
    :raise TypeError: If the input is not a 2D list or contains non-integers elements
    :raise ValueError: If elements are not binary or rows have different lengths
    """

    # Check if input is a 2D list
    if not all(isinstance(row, list) for row in code):
        raise TypeError("Input must be a 2D list of binary codewords")
    
    # Check if all elements in the 2D list are integers
    if not all(isinstance(elem, int) for row in code for elem in row):
        raise TypeError("All elements in the codeword must be integers")
    
    # Check if all elements in the 2D list are binary (0 or 1)
    if not all(elem in (0, 1) for row in code for elem in row):
        raise ValueError("Codewords must be binary (contain only 0s and 1s)")
    
    # Validate that all rows have the same length
    num_cols = len(code[0])
    if not all(len(row) == num_cols for row in code):
        raise ValueError("All codewords must have the same length")
    
    # Calculate the weight of each codeword
    list_wt = [sum(1 for elem in codeword if elem != 0) for codeword in code]

    return list_wt


def reverse_codeword(codeword: List[int]) -> List[int]:
    """
    Reverse the given binary codeword according to a specific pattern:
    - For even indices (1-based), reverse the position by subtracting the current index minus 2 from the length of the codeword
    - For odd indices (1-based), reverse the position by subtracting the current index from the length of the codeword.
    Ensures that the codeword has an even length and is binary

    :param codeword: A 1D list of binary integers (0 or 1)
    :return: The reversed codeword as a new list of binary integers
    :raise TypeError: If the input is not a 1D list or contains non-integer elements
    :raise ValueError: If elements are not binary or if the length of the codeword is not even
    """

    # Check if input is a 1D list
    if not isinstance(codeword, list):
        raise TypeError("Input must be a 1D list")
    
    # Check if all elements in the list are integers
    if not all(isinstance(elem, int) for elem in codeword):
        raise TypeError("All elements in the codeword must be integers")
    
    # Check if all elements in the list are binary (0 or 1)
    if not all(elem in (0, 1) for elem in codeword):
        raise ValueError("Codeword must be binary (contain only 0s and 1s)")
    
    # Ensure that the length of the codeword is even
    if len(codeword) % 2 != 0:
        raise ValueError("The length of the codeword must be even")
    
    length = len(codeword)
    reverse_codeword_ = []

    # Reverse the codeword according to the specified pattern
    for i in range(1, length + 1):
        if i%2 == 0:
            idx_reverse = length - (i - 2)
        else:
            idx_reverse = length - i
        reverse_codeword_.append(codeword[idx_reverse - 1])

    return reverse_codeword_

def reverse_code(code: List[List[int]]) -> List[List[int]]:
    """
    Reverse each codeword in the binary code using the reverse_codeword function
    Ensures that each codeword is binary, has the same length, and that length is even

    :param code: A 2D list where each row is a binary codeword
    :return: A new 2D list where each codeword has been reversed
    :raise TypeError: If the input is not a 2D list or contains con-integers elements
    :raise ValueError: If elements are not binary, rows have different lengths, or codeword length is not even
    """

    # Check if input is a 2D list
    if not all(isinstance(row, list) for row in code):
        raise TypeError("Input must be a 2D list of binary codeword")
    
    # Check if all elements in the 2D list are integers
    if not all(isinstance(elem, int) for row in code for elem in row):
        raise TypeError("All elements in the codewords must be integers")
    
    # Check if all elements in the 2D list are binary (0 or 1)
    if not all(elem in (0, 1) for row in code for elem in row):
        raise ValueError("Codewords must be binary (containt only 0s and 1s)")
    
    # Validate that all rows have the same length
    num_cols = len(code[0])
    if not all(len(row) == num_cols for row in code):
        raise ValueError("All codewords must have the same length")
    
    # Ensure that the length of each codeword is even
    if num_cols % 2 != 0:
        raise ValueError("The length of each codeword must be even")
    
    reverse_code_ = []

    # Apply reverse_codeword function to each row (codeword) in the code
    for row in code:
        reverse_row = reverse_codeword(row)
        reverse_code_.append(reverse_row)

    return reverse_code_

def complement_codeword(codeword: List[int]) -> List[int]:
    """
    Calculate the complement of the given binary codeword.
    Ensures that the codeword is a 1D list of binary integers with an even length

    :param codeword: A 1D list of binary integers (0 or 1)
    :return: A new list representing the complement of the input codeword
    :raise TypeError: If the input is not a 1D list or contains non-integer elements
    :raise ValueError: If elements are not binary of if the length of the codeword is not even
    """

    # Check if input is a 1D list
    if not isinstance(codeword, list):
        raise TypeError("Input must be a 1D list")
    
    # Check if all elements in the list are integers
    if not all(isinstance(elem, int) for elem in codeword):
        raise TypeError("All elements in the codeword must be integers")
    
    # Check if all elements is the list are binary (0 or 1)
    if not all(elem in (0, 1) for elem in codeword):
        raise ValueError("Codeword must be binary (contain only 0s and 1s)")
    
    # Ensure that the length of the codeword is even
    if len(codeword) % 2 != 0:
        raise ValueError("The length of the codeword must be even")
    
    length = len(codeword)

    # Calculate the complement by flipping each bit
    complement = [(elem + 1)%2 for elem in codeword]

    return complement

def complement_code(code: List[List[int]]) -> List[List[int]]:
    """
    Calculate the complement of each codeword in the code.
    Ensure that the code is a 2D list of binary integers with each codeword having an even length.

    :param code: A 2D list where each row is a binary codeword
    :return: A new 2D list where each codeword is complemented
    :raise TypeError: If the input is not a 2D list or contains non-integers elements
    :raise ValueError: If elements are not binary, rows have different lengths, or codeword length is not even
    """

    # Check if input is a 2D list
    if not all(isinstance(row, list) for row in code):
        raise TypeError("Input must be a 2D list of binary codewords")
    
    # Check if all elmeent in the 2D list are integers
    if not all(isinstance(elem, int) for row in code for elem in row):
        raise TypeError("All elements in the codewords must be integers")
    
    # Check if all elements in the 2d list are binary (0 or 1)
    if not all(elem in (0, 1) for row in code for elem in row):
        raise ValueError("Codeword must be binary (contain only 0s and 1s)")
    
    # Validate that all codeword have the same length
    num_cols = len(code[0])
    if not all(len(row) == num_cols for row in code):
        raise ValueError("All codewords must have the same length")
    
    # Ensure that the length of each codeword is even
    if num_cols % 2 != 0:
        raise ValueError("The length of each codeword must be even")
    
    # Apply complement_codeword function to each row (codeword) in the code
    complement = [complement_codeword(row) for row in code]

    return complement

def weight_gc_codeword(codeword: List[int]) -> int:
    """
    Calculate the GC-content weight of the given binary codeword.
    The weight is defined as the number of 'GC' (01) or 'CG' (10) pairs in the codeword.

    :param codeword: A 1D list representing a binary codeword
    :return: The GC-content weight of the codeword
    :raises ValueError: If the codeword's length is not even or contains non-binary values
    """
    # Ensure the length of the codeword is even
    if len(codeword) % 2 != 0:
        raise ValueError("The length of the codeword must be even")
    
    # Check if all elements in the codeword are binary (0 or 1)
    if not all(bit in (0, 1) for bit in codeword):
        raise ValueError("Codeword must be binary (contain only 0s and 1s)")
    
    weight_gc = 0
    
    # Calculate the GC-content weight
    for i in range(0, len(codeword), 2):
        if [codeword[i], codeword[i + 1]] in ([0, 1], [1, 0]):
            weight_gc += 1
    
    return weight_gc

def weight_gc_code(codewords: List[List[int]]) -> List[int]:
    """
    Calculate the GC-content weight for each codeword in a list of binary codewords.
    The weight is defined as the number of 'GC' (01) or 'CG' (10) pairs in each codeword.

    :param codewords: A 2D list where each row is a binary codeword
    :return: A list of GC-content weights corresponding to each codeword
    :raises ValueError: If any codeword has an odd length or contains non-binary values
    """
    
    # Calculate the GC-content weight for each codeword in the list
    weight_gc_list = []
    for codeword in codewords:
        weight_gc_list.append(weight_gc_codeword(codeword))
    
    return weight_gc_list

def weight_gc_enumerator(codewords: List[List[int]]) -> str:
    """
    Calculate the GC-content weight enumerator for a set of binary codewords.
    The enumerator is expressed as a polynomial where the exponents represent 
    the GC-content and the coefficients represent the number of codewords with that GC-content.

    :param codewords: A 2D list where each row is a binary codeword
    :return: A string representation of the GC-content weight enumerator
    :raises ValueError: If any codeword has an odd length or contains non-binary values
    """

    term_counts: Dict[int, int] = {}
    weights = weight_gc_code(codewords)
    length = len(codewords[0])

    # Count occurrences of each GC-content weight
    for weight_gc in weights:
        if weight_gc in term_counts:
            term_counts[weight_gc] += 1
        else:
            term_counts[weight_gc] = 1

    GCW = []

    # Sort the terms and format the polynomial
    for weight_gc, count in sorted(term_counts.items(), key=lambda item: (-item[0], item[1])):
        a = (length / 2) - weight_gc
        b = weight_gc

        if count == 1:
            GCW.append(f"a^{int(a)} b^{int(b)}")
        else:
            GCW.append(f"{count}a^{int(a)} b^{int(b)}")

    return " + ".join(GCW)

def dna_code(generator_matrix: List[List[int]],
             constraints: List[str] = ['reverse', 'reverse_complement', 'gc_content'],
             gc_weight: Optional[int] = None) -> List[List[int]]:
    """
    Generates a DNA code based on the provided generator matrix and constraints.

    :param generator_matrix: A 2D list representing the generator matrix
    :param constraints: A list of constraints that must be applied; can include 'reverse', 
                        'reverse complement', 'gc-content'
    :param gc_weight: Optional parameter required if 'gc-content' is one of the constraints.
    :return: A list of codewords satisfying the given constraints.
    :raises ValueError: If 'gc-content' is selected without specifying gc_weight, or if an invalid constraint is provided.
    """

    # Validate the constraints
    valid_constraints = {'reverse', 'reverse_complement', 'gc_content'}
    if not set(constraints).issubset(valid_constraints):
        raise ValueError(f"Constraints must be a subset of {valid_constraints}")
    
    # Check if 'gc-content' constraint is selected but gc_weight is not provided
    if 'gc_content' in constraints and gc_weight is None:
        raise ValueError("The 'gc_content' constraint requires a gc_weight parameter.")
    
    length = len(generator_matrix)
    message_ = message(length=length)
    code_ = codewords(message=message_, generator_matrix=generator_matrix)

    def reverse_constraint(code = code_):
        reverse_code_ = reverse_code(code)
        counts = len(code)
        code_no_sr = []
        
        for i in range(counts):
            if code[i] != reverse_code_[i]:
                if reverse_code_[i] not in code_no_sr:
                    code_no_sr.append(code[i])
            

        return code_no_sr
            

    def reverse_complement_constraint(code=code_):
        complement_code_ = complement_code(code)
        reverse_complement_code_ = reverse_code(complement_code_)
        counts = len(code)
        code_no_src = []

        for i in range(counts):
            if code[i] != reverse_complement_code_[i]:
                if reverse_complement_code_[i] not in code_no_src:
                    code_no_src.append(code[i])

        return code_no_src
    
    def gc_content_constraint(code=code_, gc_weight=gc_weight):
        code_gc = []
        counts = len(code)

        for i in range(counts):
            gc_weight_codeword_ = weight_gc_codeword(code[i])
            if gc_weight_codeword_ == gc_weight:
                code_gc.append(code[i])
        
        return code_gc

    # With reverse constraint
    if 'reverse' in constraints and 'reverse_complement' not in constraints and 'gc_content' not in constraints:
        code_dna_ = reverse_constraint(code=code_)
        return code_dna_

    # With reverse complement constraint
    elif 'reverse' not in constraints and 'reverse_complement' in constraints and 'gc_content' not in constraints:
        code_dna_ = reverse_complement_constraint(code=code_)
        return code_dna_
    
    # With gc content constraint
    elif 'reverse' not in constraints and 'reverse_complement' not in constraints and 'gc_content' in constraints:
        code_dna_ = gc_content_constraint(code=code_)
        return code_dna_
    
    # With reverse constraint and reverse complement constraint
    elif 'reverse' in constraints and 'reverse_complement' in constraints and 'gc_content' not in constraints:
        code_dna_ = reverse_constraint(code=code_)
        code_dna_ = reverse_complement_constraint(code=code_dna_)
        return code_dna_
    
    # with reverse constraint and gc content constraint
    elif 'reverse' in constraints and 'reverse_complement' not in constraints and 'gc_content' in constraints:
        code_dna_ = reverse_constraint(code=code_)
        code_dna_ = gc_content_constraint(code=code_dna_)
        return code_dna_
    
    # with reverse complement constraint and gc content constraint
    elif 'reverse' not in constraints and 'reverse_complement' in constraints and 'gc_content' in constraints:
        code_dna_ = reverse_complement_constraint(code=code_)
        code_dna_ = gc_content_constraint(code=code_dna_)
        return code_dna_
    
    # with reverse contraint, reverse complement constraint, and gc content constraint
    elif 'reverse' in constraints and 'reverse_complement' in constraints and 'gc_content' in constraints:
        code_dna_ = reverse_constraint(code=code_)
        code_dna_ = reverse_complement_constraint(code=code_dna_)
        code_dna_ = gc_content_constraint(code=code_dna_)
        return code_dna_

    