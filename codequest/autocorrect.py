def hamming_distance(a, b):
    difference = abs(len(a) - len(b))

    for i in range(len(a)):
        try:
            if a[i] != b[i]:
                difference += 1
        
        except IndexError:
            difference += 1
    
    return difference

correctly_spelled = []

def compute_closest(input_word):
    differences = []

    for i in correctly_spelled:
        differences.append(hamming_distance(input_word, i))

    min_diff = min(differences)
    closest_word = differences.index(min_diff)

    print(correctly_spelled[closest_word])

test_cases = int(input())

for i in range(test_cases):
    line_1 = input().split(" ")

    to_correct = []

    correctly_spelled_words_length = int(line_1[0])
    to_correct_length = int(line_1[1])

    for i in range(correctly_spelled_words_length):
        correctly_spelled.append(input().lower().strip())
    
    for i in range(to_correct_length):
        to_correct.append(input().lower().strip())
    
    for i in to_correct:
        compute_closest(i)