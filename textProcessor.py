import os
import sys

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
def tokenize(TextFilePath):
    tokens = []
    with open(TextFilePath, 'rb') as f:
        byte = f.read(1)
        currentWord = []
        while byte != b'':
            letter = byte.decode('utf-8')
            if letter.isalpha() or letter.isdigit():
                currentWord.append(letter)
            elif len(currentWord) != 0:
                word = "".join(currentWord).lower()
                tokens.append(word)
                currentWord = []
            byte = f.read(1)
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

if __name__ == "__main__":
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
        if os.path.exists(fileName):
            tokenList = tokenize(fileName)
            tokenDict = computeWordFrequencies(tokenList)
            printFrequencies(tokenDict)
        else:
            print("File not found")
    else:
        print("Wrong number of Arguments")