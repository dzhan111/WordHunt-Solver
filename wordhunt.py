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
                # Handle invalid characters (optional)
                continue

            if current_node.children[char_index] is None:
                current_node.children[char_index] = TrieNode()

            current_node = current_node.children[char_index]

        current_node.is_end_of_word = True

trie = Trie()
ans = []  # Use a list instead of a dictionary
def makeTrie():
    with open("wordbank.txt", "r") as file:
        #first line
        line = file.readline()

        # While there are more lines in the file (line is not an empty string)
        while line:
            trie.insert(line.strip())  # Strip to remove leading/trailing whitespaces
            line = file.readline()

# dfs method to traverse

def explore(row, col, word, path, visited, node):
    if(row < 0 or row > 3 or col < 0 or col > 3):
        return
    if(visited[row][col]):
        return

    letter = board[row * 4 + col + 1]
    if node is None or node.is_end_of_word:
        return

    word = word + letter
    visited[row][col] = True

    if len(word) > 3 and node.is_end_of_word:
        ans.append((word, path))

    directions = [((1, 0), 'D'), ((0, 1), 'R'), ((-1, 0), 'U'), ((0, -1), 'L'),
                ((1, 1), 'DR'), ((-1, -1), 'UL'), ((1, -1), 'DL'), ((-1, 1), 'UR')]

    for dir in directions:
        x = dir[0][0]
        y = dir[0][1]
        move = dir[1]
        if(row + x < 4 and row + x >= 0 and col + y < 4 and col + y >= 0):
            if(not visited[row + x][col + y]):
                next_node = node.children[ord(letter) - ord('a')]
                explore(row + x, col + y, word, path + ' ' + move, visited, next_node)

    visited[row][col] = False

# main
getBoard()
printBoard()
makeTrie()

visited = [[False] * 4 for _ in range(4)]

for i in range(4):
    for j in range(4):
        explore(i, j, '', 'Path: ', visited, trie.root)

# sort words
ans.sort()
print(ans)
# print results
for (word, path) in ans:
    print(f"{word}: {path}")
