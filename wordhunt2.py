from typing import List,Optional
import pygame as pg
import sys

R = C = 4 # rows, cols
N = R * C # n squares

W, H = 600, 700 # screen width, height
SPACING = 5 # square spacing
SIZE = W // max(R,C) - 2*SPACING # square size

DIRECTIONS = [
    (1,  0, 'D'),
    (0,  1, 'R'),
    (-1, 0, 'U'),
    (0, -1, 'L'),
    (1,  1, 'DR'),
    (-1,-1, 'UL'),
    (1, -1, 'DL'),
    (-1, 1, 'UR')
]
DIRS = dict( (move, (r,c)) for r,c,move in DIRECTIONS )

def getBoard(board: List[List[str]]):
    user_input = ''
    while len(user_input) != N:
        user_input = input(f"Input board ({N} letters): ").replace(' ','')
    for r in range(R):
        for c in range(C):
            board[r][c] = user_input[r * C + c]

def printBoard(board: List[List[str]]):
    for row in board:
        print(' '.join(row))

# trie class
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        curr = self.root

        for char in word:
            char_idx = ord(char) - ord('a')
            if not (0 <= char_idx < 26): continue

            if curr.children[char_idx] is None:
                curr.children[char_idx] = TrieNode()

            curr = curr.children[char_idx]

        curr.is_end_of_word = True

def makeTrie(trie: Trie):
    with open("wordbank.txt", "r") as file:
        while line:=file.readline():
            trie.insert(line.strip())

class Word:
    def __init__(self, word: str, path: List[str]):
        self.word = word
        r0, c0 = path[0].split(' ')[2].split(',')
        self.sequence = []
        r, c = int(r0), int(c0)
        for dir in path[1:]:
            dr, dc = DIRS[dir]
            r += dr
            c += dc
            self.sequence.append((r,c))

# search for words
def dfs(row: int, col: int, word: str, path: List[str], visited: List[List[bool]],
        node: Optional[TrieNode], visited_words: set,
        ans: List[tuple[str, List[str], Word]]):
    if not (0 <= row < R and 0 <= col < C)\
        or visited[row][col]\
        or word in visited_words\
        or node is None:
        return

    letter = board[row][col]
    visited[row][col] = True

    if len(word) > 3 and node.is_end_of_word and word not in visited_words:
        visited_words.add(word)
        ans.append((word, path, Word(word, path)))

    for x,y,move in DIRECTIONS:
        rnext, cnext = row+x, col+y
        if 0 <= row + x < R and 0 <= cnext < C:
            if not visited[rnext][cnext]:
                letter = board[rnext][cnext]
                next_node = node.children[ord(letter) - ord('a')]
                dfs(rnext, cnext, word + letter, path + [move], visited, next_node, visited_words, ans)

    visited[row][col] = False

def idx_to_point(r: int, c: int, center: bool = False) -> (int, int):
    x = SPACING + c * (SIZE + 2*SPACING)
    y = SPACING + r * (SIZE + 2*SPACING)
    if center:
        x += SIZE // 2
        y += SIZE // 2
    return (x,y)

if __name__ == '__main__':
    trie = Trie()
    board = [['']*C for _ in range(R)]
    ans = []

    makeTrie(trie)
    getBoard(board)
    printBoard(board)
    

    visited = [[False] * C for _ in range(R)]
    visited_words = set()

    # dfs on each cell
    for r in range(R):
        for c in range(C):
            letter = board[r][c]
            index = ord(letter)-ord('a')
            if trie.root.children[index]:
                dfs(r, c, '', [f"Start at {str(r)},{str(c)} \nPath:"], visited, trie.root, visited_words, ans)

    # sort words (longer words first)
    ans = sorted(ans, key=lambda x: len(x[0]), reverse=True)

    # print results
    for word, path, obj in ans:
        print(f"{word}:\n{' '.join(path)}\n")

    # display words
    pg.init()

    SCREEN = pg.display.set_mode((W, H))
    pg.display.set_caption("Solutions")
    CLK = pg.time.Clock()
    font = pg.font.Font(None, SIZE)

    curr_word_idx = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                else:
                    curr_word_idx += 1
                    if curr_word_idx >= len(ans): 
                        pg.quit()
                        sys.exit()

        SCREEN.fill((196,196,196))

        _, _, curr_word = ans[curr_word_idx]
        # draw grid
        for r in range(R):
            for c in range(C):
                x,y = idx_to_point(r,c)
                # square
                pg.draw.rect(SCREEN, 'white', (x, y, SIZE, SIZE), 1)
                # letter
                start_letter = ((r,c) == curr_word.sequence[0])
                letter = board[r][c]
                text = font.render(letter, True, 'green' if start_letter else 'black')
                text_rect = text.get_rect(center=(x + SIZE//2, y + SIZE//2))
                SCREEN.blit(text, text_rect)

        # draw word
        text = font.render(curr_word.word, True, 'green')
        text_rect = text.get_rect(center=(W // 2, H - 50))
        SCREEN.blit(text, text_rect)
        # draw word path
        r0,c0 = curr_word.sequence[0]
        for r,c in curr_word.sequence[1:]:
            pg.draw.line(
                SCREEN, 'green',
                idx_to_point(r0,c0,center=True), idx_to_point(r,c,center=True),
                SPACING
            )
            r0,c0 = r,c

        pg.display.flip()
        CLK.tick(60)