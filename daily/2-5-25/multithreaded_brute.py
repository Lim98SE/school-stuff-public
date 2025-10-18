import threading
import random

def shift_alphabet_decrypt(shift):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(shift):
        alph = list(alphabet)
        last = alph.pop()
        alph.insert(0, last)
        alphabet = "".join(alph)
    
    return alphabet

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

def shift_alphabet_encrypt(shift):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i in range(shift):
        alph = list(alphabet)
        last = alph.pop(0)
        alph.append(last)
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

results = [0] * 26

def force(msg, key, wordlist):
    global results
    found = []
    message = decrypt_message(msg, key)

    for i in wordlist:
        if i.lower() in message.lower():
            found.append(i)

    results[key] = found

with open("wordlist.txt") as file:
    wordlist = file.read().split("\n")

wl_buffer = []

for i in wordlist:
    if len(i.strip()) >= 5: wl_buffer.append(i.strip())

wordlist = wl_buffer.copy()

original_message = ""

with open("text") as file:
    original_message = file.read()

text = encrypt_message(original_message, random.randint(0, 25))

with open("encrypted.txt", "w") as file:
    file.write(text)

threads = []

import time

start_time = time.time()

for i in range(26):
    threads.append(threading.Thread(target=force, args=(text, i, wordlist)))

for i in threads:
    i.start()

for i in threads:
    i.join()

# for i in range(26):
#     print(i)
#     force(text, i, wordlist)

print(time.time() - start_time)

# 7.69
# 7.79

max_found = 0
max_index = 0

for i in range(len(results)):
    if len(results[i]) > max_found:
        max_found = len(results[i])
        max_index = i

print(f"Key is: {max_index}")