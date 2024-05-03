import os
import sys
import hashlib
from difflib import SequenceMatcher

# This function will be given a file path, and return a list of tokens

# Steps:
# Open the file path
# Read input byte by byte
# Decode the byte into Characters, check if its alphanumeric characters
# Add alphanumeric characters into a temporary buffer
# If it's not alphanumeric characters, check if there's new token that needs to be added to the token list
# Repeat reading input byte and perform the check

# If the total character in the file is n, the while loop runs for n times.
# In the case of alphanumeric characters, it just append the character to the currentWord list, which is an O(1) operation.
# In the case of no-alphanumeric characters, it executes function join and lower. Which is all O(m),
# assuming the number of characters in that token is m
# The time complexity of the function is thus O(n)
def tokenize(text):
    tokens = []
    current_word = []
    for char in text:
        if char.isalpha() or char.isdigit():
            current_word.append(char)
        elif len(current_word) != 0:
            word = "".join(current_word).lower()
            tokens.append(word)
            current_word = []
    if current_word:
        word = "".join(current_word).lower()
        tokens.append(word)
    return tokens

# This function is given a list of tokens, and return a dictionary contains each tokens and the number of occurrence

# Let the number of token in tokenList be n, the function iterates through the for loop n times. All the actions performed
# in the for loop such as dictionary loop-up, accessing dictionary, and writing back to dictionary all takes O(1) time.
# Therefore, the time complexity of the function is O(n)
def computeWordFrequencies(tokenList):
    result = {}
    for token in tokenList:
        if token not in result:
            result[token] = 1
        else:
            result[token] += 1
    return result

# This function is given a dictionary of token and its number of occurrence, and it prints out the token and frequency

# The sorting algorithm in Python sorted function using Tim Sort,
# which is a combination of both merge sort and insertion sort. It has a O(n*log(n))time complexity, assuming the
# list iterable being sorted has length n.
# Printing out the tokens take O(n) time.
# Therefore, the time complexity of the function is O(n*log(n))
def printFrequencies(wordCount):
    sortedTokens = sorted(wordCount.items(), key=lambda x: (-x[1], x[0]))
    for token in sortedTokens:
        print(f'{token[0]} - {token[1]}')

def simhash(tokens, hash_bits=128):
    V = [0] * hash_bits
    for word, count in tokens.items():
        hash_value = int(hashlib.md5(word.encode('utf-8')).hexdigest(), 16)
        for i in range(hash_bits):
            # extracts the value of the i-th bit from the right of hash_value
            bit = (hash_value >> i) & 1
            if bit == 1:
                V[i] += count
            else:
                V[i] -= count
    fingerprint = 0
    for i in range(hash_bits):
        if V[i] >= 0:
            # sets the i-th bit of fingerprint to 1 without affecting the other bits
            fingerprint |= (1 << i)
    return fingerprint

def are_similar(hash_a, hash_b, threshold, hash_bits=128):
    # XOR to find differing bits
    differing_bits = hash_a ^ hash_b

    # Count the number of same bits
    same_bits = hash_bits - bin(differing_bits).count('1')

    # Calculate similarity as the fraction of bits that are the same
    similarity = same_bits / hash_bits
    return similarity >= threshold

def is_new_hash_value(new_hash_value, hash_values):
    for value in hash_values:
        if are_similar(new_hash_value, value, 0.9):
            return False
    return True

def is_new_url(new_url, threshold, visited_urls):
    for url in visited_urls:
        similarity_ratio = SequenceMatcher(None, new_url, url).ratio()
        # print(similarity_ratio)
        if similarity_ratio >= threshold:
            return False
    return True

if __name__ == "__main__":
    pass
    # if len(sys.argv) == 2:
    #    fileName = sys.argv[1]
    #    if os.path.exists(fileName):
    #        tokenList = tokenize(fileName)
    #        tokenDict = computeWordFrequencies(tokenList)
    #        printFrequencies(tokenDict)
    #    else:
    #        print("File not found")
    #else:
    #    print("Wrong number of Arguments")
