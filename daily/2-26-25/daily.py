import string

def char_freq(text):
    text = text.lower()

    output = {}

    for i in text:
        if not i in string.ascii_lowercase: continue
        if not i in output.keys(): output[i] = 0
        output[i] += 1
    
    return output

def determine_winner(votes):
    output = {}

    for i in votes:
        if not i in output.keys(): output[i] = 0
        output[i] += 1
    
    ties = []
    winning_votes = max(output.values())
    
    for i in output:
        if output[i] == winning_votes:
            ties.append(i)
    
    if len(ties) == 1: return ties[0]
    else:
        m = "Z" * 60

        for i in ties:
            if i < m:
                m = i
        
        return m

print(char_freq("burger"))