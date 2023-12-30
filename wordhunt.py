board = {1: '', 2: '', 3: '', 4: '',
         5: '', 6: '', 7: '', 8: '',
         9: '', 10: '', 11: '', 12: '',
         13: '', 14: '', 15: '', 16: ''
         }

def getBoard():
    user_input = input("Input board: ")
    i = 1
    for letter in user_input:
        board[i] = letter
        i = i + 1

def printBoard():
    for i in range(1, 17):
        print(board[i], end=' ')
        if i % 4 == 0:
            print()



#trie class
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current_node = self.root

        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]

        current_node.is_end_of_word = True


trie = Trie()
def makeTrie():
    with open("wordbank.txt", "r") as file:
        #first line
        line = file.readline()

        # While there are more lines in the file (line is not an empty string)
        while line:
            trie.insert(line.strip())
            line = file.readline

#dfs method to traverse



#main
makeTrie()
getBoard()


        



