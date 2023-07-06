from sympy import primerange
from hashlib import sha1

LABELS = ['A', 'B', 'C', 'D', 'E']
VARIABLES = ['Y', 'X', 'Z']
PRIMES = list(primerange(2, 10 ** 6))

class godel_to_s_lang:
    godel : int
    lines : list
    line_codes : list

    def __init__(self):
        self.godel = -1
        self.lines = []
        self.line_codes = []

    def get_line_codes(self, godel, i = 0, lookahead = 5):
        if godel <= 0:
            raise Exception('Godel nust be a positive number')

        if self.line_codes == []:
            godel += 1

        if lookahead == 0:
            self.line_codes = self.line_codes[:-5]
            return self.line_codes

        self.line_codes.append(0)

        if godel % PRIMES[i] != 0:
            lookahead -= 1

        while godel % PRIMES[i] == 0:
            lookahead = 5
            self.line_codes[i] += 1
            godel //= PRIMES[i]

        return self.get_line_codes(godel, i + 1, lookahead)

    def get_line_abc(self, line_code):
        def unpair(pair):
            x = y = 0

            pair += 1
            while pair % 2 == 0:
                x += 1
                pair //= 2

            pair -= 1
            y = pair // 2

            return x, y

        a, bc = unpair(line_code)
        b, c = unpair(bc)

        return a, b, c

    def construct_line(self, a, b, c):
        def get_label(id):
            id -= 1
            label = LABELS[id % len(LABELS)]

            if id >= len(LABELS):
                label += str((id + 1) // len(LABELS) + 1)

            return label

        def get_variable(id):
            if id == 0:
                return VARIABLES[id]

            id += 1
            variable = VARIABLES[id % (len(VARIABLES) - 1) + 1]

            if id > len(VARIABLES):
                variable += str(id // (len(VARIABLES) - 1) + 1)

            return variable

        line = '' if a == 0 else f'[{get_label(a)}] '

        variable = get_variable(c)
        if b == 0:
            self.lines.append(line + f'{variable} <- {variable}')
        elif b == 1:
            self.lines.append(line + f'{variable} <- {variable} + 1')
        elif b == 2:
            self.lines.append(line + f'{variable} <- {variable} - 1')
        else:
            self.lines.append(line + f'IF {variable} != 0 GOTO {get_label(b - 2)}')

    def construct_program(self, godel):
        if self.line_codes != []:
            self.line_codes = []
        if self.lines != []:
            self.line = []

        if (tp := type(godel)) is str:
            godel = open(godel).readline().strip()
            
            if not godel.isnumeric():
                raise Exception('Godel must be a positive number')
            
            self.godel = int(godel)
        elif tp is int:
            self.godel = godel
        else:
            raise Exception('Godel must be a positive number')

        self.get_line_codes(self.godel)
        for lc in self.line_codes:
            a, b, c = self.get_line_abc(lc)
            self.construct_line(a, b, c)
    
    def print(self):
        for line in self.lines:
            print(line)
    
    def write(self):
        filename = self.godel if len(str(self.godel)) <= 30 else sha1(str(self.godel).encode()).hexdigest()

        with open(f'{filename}.s', 'w') as file:
            file.write('\n'.join(self.lines))

if __name__ == '__main__':
    g2s = godel_to_s_lang()
    g2s.construct_program('godel.txt')
    g2s.print()
    g2s.write()