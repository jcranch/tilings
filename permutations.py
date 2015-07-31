def remove_duplicates(list_of_elements):
    unique_elements = []
    for element in list_of_elements:
        if element not in unique_elements:
            unique_elements += [element]
    return unique_elements

def all_permutations(permutable):
    list_of_permutations = []
    for index1 in range(4):
        for index2 in [i for i in range(4) if i != index1]:
            for index3 in [i for i in range(4) if i != index1 and i != index2]:
                for index4 in [i for i in range(4) if i != index1 and i != index2 and i != index3]:
                    list_of_permutations += [[permutable[index1],permutable[index2],permutable[index3],permutable[index4]]]
    return list_of_permutations


def all_permutations_plus_minus(permutable):
    list_of_permutations = []
    for sign1 in [-1,1]:
        for sign2 in [-1,1]:
            for sign3 in [-1,1]:
                for sign4 in [-1,1]:
                    list_of_permutations += all_permutations([permutable[0]*sign1,permutable[1]*sign2,permutable[2]*sign3,permutable[3]*sign4])
    return list_of_permutations
  
    
def cycle_decomposition(permutation, original = None):
    if original == None:
        original = sorted(permutation)
    permutation_dictionary = dict(zip(original,permutation))
    completed = []
    cycle = [[1]]
    i = 1
    for count in range(4):
        completed += [i]
        if count != 3:
            if permutation_dictionary[i] not in completed:
                i = permutation_dictionary[i]
                cycle[::-1][0] += [i]
            else :
                i = min([j for j in original if j not in completed])
                cycle += [[i]]
    return cycle

def cycle_parity(cycle):
    return (-1)**(len(cycle)+1)

def permutation_parity(permutation, original = None):
    cycles = cycle_decomposition(permutation, original)
    sgn = 1.0
    for cycle in cycles:
        sgn *= cycle_parity(cycle)
    return sgn





def only_even_permutations(orignal):
    list_of_even_permutations = [permutation for permutation in all_permutations(orignal) if permutation_parity(permutation)==1]
    return list_of_even_permutations
