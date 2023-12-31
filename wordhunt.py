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

# trie class
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current_node = self.root

        for char in word:
            char_index = ord(char) - ord('a')
            if char_index < 0 or char_index >= 26:
                continue

            if current_node.children[char_index] is None:
                current_node.children[char_index] = TrieNode()

            current_node = current_node.children[char_index]

        current_node.is_end_of_word = True

trie = Trie()
ans = []
def makeTrie():
    with open("real.txt", "r") as file:
        #first line
        line = file.readline()

        # While there are more lines in the file (line is not an empty string)
        while line:
            trie.insert(line.strip())  # Strip to remove leading/trailing whitespaces
            line = file.readline()


#dfs to traverse
#12/30 6:49 for some reason, extra letter gets added onto valid words -> more words than actual
def explore(row, col, word, path, visited, node,visited_words):
    if(row < 0 or row > 3 or col < 0 or col > 3):
        return
    if(visited[row][col] or word in visited_words):
        return

    letter = board[row * 4 + col + 1]
    if node is None:
        return

    
    visited[row][col] = True

    if len(word) > 3 and node.is_end_of_word and word not in visited_words:
        visited_words.add(word)
        ans.append((word, path))

    
    
    directions = [((1, 0), 'D'), ((0, 1), 'R'), ((-1, 0), 'U'), ((0, -1), 'L'),
                ((1, 1), 'DR'), ((-1, -1), 'UL'), ((1, -1), 'DL'), ((-1, 1), 'UR')]

    for dir in directions:
        x = dir[0][0]
        y = dir[0][1]
        move = dir[1]
        if(row + x < 4 and row + x >= 0 and col + y < 4 and col + y >= 0):
            if(not visited[row + x][col + y]):
                letter = board[(row + x) * 4 + col + y + 1]
                next_node = node.children[ord(letter) - ord('a')]
                explore(row + x, col + y, word + letter, path + ' ' + move, visited, next_node, visited_words)

    visited[row][col] = False




# main
getBoard()
printBoard()
makeTrie()

visited = [[False] * 4 for _ in range(4)]
visited_words = set()

for i in range(4):
    for j in range(4):
        letter = board[i * 4 + j + 1]
        index = ord(letter)-ord('a')
        #TRIE ROOT NODDESKJFLDSJKLF:J
        if not(trie.root.children[index] == None):
            explore(i, j,'', 'Start at ' + str(i)+ ','+str(j)+'\nPath:', visited, trie.root ,visited_words)

# sort words (print longer words last)
ans = sorted(ans, key=lambda x: len(x[0]))


# print results
for (word, path) in ans:
    print()
    print(f"{word}:\n{path}")
    print()
