def shift_alphabet_encrypt(shift):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(shift):
        alph = list(alphabet)
        last = alph.pop(0)
        alph.append(last)
        alphabet = "".join(alph)
    
    return alphabet

def shift_alphabet_decrypt(shift):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(shift):
        alph = list(alphabet)
        last = alph.pop()
        alph.insert(0, last)
        alphabet = "".join(alph)
    
    return alphabet

def encrypt_message(message, shift):
    message = message.upper()
    base_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shifted = shift_alphabet_encrypt(shift)

    new_message = ""

    for i in message:
        index = base_alphabet.find(i)

        if index != -1:
            char = shifted[index]
        
        else:
            char = i
        
        new_message += char
    
    return new_message.lower()

def decrypt_message(message, shift):
    message = message.upper()
    base_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    shifted = shift_alphabet_decrypt(shift)

    new_message = ""

    for i in message:
        index = base_alphabet.find(i)

        if index != -1:
            char = shifted[index]
        
        else:
            char = i
        
        new_message += char
    
    return new_message.lower()

cases = int(input())

outputs = []

for i in range(cases):
    key = int(input())
    text = input().upper()

    outputs.append(decrypt_message(text, key))

for i in outputs:
    print(i.lower().strip())