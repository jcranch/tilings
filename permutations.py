def remove_duplicates(list_of_elements):
    unique_elements = []
    for element in list_of_elements:
        if element not in unique_elements:
            unique_elements += [element]
    return unique_elements

def all_permutations(original = [1,2,3,4]):
    list_of_permutations = []
    for index1 in range(4):
        for index2 in [i for i in range(4) if i != index1]:
            for index3 in [i for i in range(4) if i != index1 and i != index2]:
                for index4 in [i for i in range(4) if i != index1 and i != index2 and i != index3]:
                    list_of_permutations += [[original[index1],original[index2],original[index3],original[index4]]]
    return list_of_permutations
  
    
def cycle_decomposition(permutation, original = [1,2,3,4]):
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
                try :
                    i = min([j for j in original if j not in completed])
                except:
                    break
                cycle += [[i]]
    return cycle



def cycle_parity(cycle):
    return (-1)**(len(cycle)+1)



def permutation_parity(permutation, original = [1,2,3,4]):
    cycles = cycle_decomposition(permutation, original)
    sgn = 1.0
    for cycle in cycles:
        sgn *= cycle_parity(cycle)
    return sgn


def only_even_permutations(original = [1,2,3,4]):
    list_of_even_permutations = [permutation for permutation in all_permutations(original) if permutation_parity(permutation,original)==1]
    return list_of_even_permutations

def perform_permutation(permutable, permutation): #cycle of the form [1,2,3,4]
    new_set = [None]*4
    cycle_dictionary  = dict(zip(range(1,5),permutation))
    for index in range(1,5):
        new_set[cycle_dictionary[index]-1] = permutable[index-1]
    return new_set


def produce_permutable_plus_minus(permutable):
    '''
    Performs a given permutation on all in  set (+- a, +- b, +- c, +- d).
    '''
    list_of_results = []
    for sgn1 in [-1,1]:
        for sgn2 in [-1,1]:
            for sgn3 in [-1,1]:
                for sgn4 in [-1,1]:
                    considered_permutable = [permutable[0]*sgn1,permutable[1]*sgn2,permutable[2]*sgn3,permutable[3]*sgn4]
                    list_of_results += [considered_permutable]
    return list_of_results

def perform_multiple_permutations_on_multible_permutables(list_of_permutables, list_of_permutations):
    list_of_results = []
    for permutable in list_of_permutables:
        for permutation in list_of_permutations:
            list_of_results += [perform_permutation(permutable, permutation)]
    return list_of_results
