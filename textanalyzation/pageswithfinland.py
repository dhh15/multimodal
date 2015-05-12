import os
folder = os.listdir('singlepagetxts')
# Creates a file with a list of all filenames in the directory
print len(folder)
# lentght of fodler, diagnostics purposes only

montako = 0
# for diagnostics purposes, defined firs as empty.

f = open('pageswithfinland.txt', 'w')
# Creates a file for writing

key_words = ['Finland', 'Finnish', 'Suomi']
#key_words = ['yes']
# Defines the keywords we want to search for in the texts

# Next we open each file at the time in the folder and following the 'folder' list.
# The code goes through the content of the txt files.
# Each time a keyword is found, varible 'suomi' is set to true
# When suomi is true, the filename is printed to file 'f' along with a line break
# and montako variable gets plus one
for filename in folder:
    text_file = open('singlepagetxts/'+filename, 'r')
    
    suomi = False

    teksti = text_file.read()
    
    for word in key_words:
        if word in teksti:
            suomi = True

    if suomi:
        montako = montako+1
        if montako < 10:
            print filename
        f.write(filename+'\n')

f.close()
# closes the file 'f'

print montako
# for diagnostics only
