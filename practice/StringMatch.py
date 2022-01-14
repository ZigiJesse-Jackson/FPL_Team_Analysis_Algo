import sys

# function to match string
def matchString(pattern, text):
    pattern = pattern.rstrip()  # strip all trailing spaces
    text = text.rstrip()  # strip all trailing spaces
    pLen = len(pattern)  # take length of pattern for char comparison
    tLen = len(text)  # take length of text for char comparison

    # if len of pattern is longer than text, return -1
    if pLen > tLen:
        return -1

    for i in range(0,tLen-pLen):
        j=0
        while j<len(pattern) and pattern[j] == text[i+j]:  # if j matches char, increment its value
            j+=1
        if j == len(pattern):  # if value of j matches len of pattern, match has been found
            return i  # return index

    return -1  # if match not found, return -1

# Main function for interactive session on commandline
def main():
    text = str(input("Enter text: "))
    pattern = str(input("Enter pattern: "))

    index = matchString(pattern,text)
    if index == -1:
        print("Pattern cannot be found in text")
    else:
        print(index)


# file reading and writing function for file input session on commandline
def textPatternFile(filename):
    file = open(filename, "r+")  # Read file with patterns
    lines = file.readlines()
    numTextPattern = int(lines[0])*2  # Read number of pair of patterns and texts
    list = {}  # create dict to hold pairs
    outIndices = []  # create list to hold indices for string matching

    for i in range(1,numTextPattern,2):
        list[lines[i]] = lines[i+1]  # assigning patterns to relevant text


    for text in list:
        outIndices.append(str(matchString(list[text], text))+'\n')  # holding list of indices for pattern text pairs

    outFileName = filename.split(".")[0]+"Output.txt"  # Output file name
    output = open(outFileName,'w')  # opening output file to write indices
    output.writelines(outIndices)
    output.close()
    file.close()
    print("Open "+outFileName+" !")

arg = sys.argv.pop()

# if command line argument is "interactive" call main function
if arg == "interactive":
    main()
# if command line argument is a file name, call file reading function for patterns
elif len(arg.split('.')) == 2 and arg.split('.')[1] == "txt":
    textPatternFile("input.txt")

