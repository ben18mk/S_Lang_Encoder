from sympy import primerange

LABELS = ['A', 'B', 'C', 'D', 'E']
VARIABLES = ['Y', 'X', 'Z']
PRIMES = list(primerange(2, 10 ** 6))

class s_lang_to_godel:
    sfilecontent : list

    def __init__(self):
        self.sfilecontent = []
    
    pair = lambda self, x, y: 2 ** x * (2 * y + 1) - 1

    def load_S(self, sfilename):
        self.sfilecontent = [l.strip() for l in open(sfilename).readlines()]

    def check_line(self, line):
        splitted = line.split()

        if splitted[0][0] == '[':
            splitted = ['[', splitted[0].replace('[', '').replace(']', ''), ']'] + splitted[1:]

        is_label = lambda raw: raw[0] in LABELS and \
                                (raw[1:] == '' or raw[1:].isnumeric()) and \
                                raw[1:] != '0'

        is_variable = lambda raw: raw[0] in VARIABLES and \
                                    (raw[1:] == '' or raw[1:].isnumeric()) and \
                                    raw[1:] != '0' and \
                                    (raw[0] == VARIABLES[0] and raw[1:] == '' or \
                                     raw[0] != VARIABLES[0] and raw[1:] != '' or \
                                     raw[0] != VARIABLES[0] and raw[1:] == '')

        if splitted[0] == '[':
            if splitted[2] != ']' and not is_label(splitted[1]):
                raise Exception(f'LABEL_ERROR: line: "{line}"')
            elif splitted[3] == 'IF':
                if len(splitted) < 9:
                    raise Exception(f'COMMAND_LENGTH_ERROR: "{line}"')

                if not is_variable(splitted[4]) or \
                    splitted[5] != '!=' or \
                    splitted[6] != '0' or \
                    splitted[7] != 'GOTO' or \
                    not is_label(splitted[8]):
                    raise Exception(f'IF_GOTO_ERROR: line "{line}"')
                return
            if is_variable(splitted[3]):
                if len(splitted) < 6:
                    raise Exception(f'COMMAND_LENGTH_ERROR: "{line}"')

                if splitted[4] != '<-' or \
                    not is_variable(splitted[5]) or \
                    splitted[3] != splitted[5]:
                    raise Exception(f'COMMAND_ERROR: line "{line}"')
                elif len(splitted) > 6 and \
                    (splitted[6] not in ['-', '+'] or \
                     splitted[7] != '1'):
                    raise Exception(f'COMMAND_TYPE_ERROR: line "{line}"')
                return
            return
        elif splitted[0] == 'IF':
            if len(splitted) < 3:
                raise Exception(f'COMMAND_LENGTH_ERROR: "{line}"')

            if not is_variable(splitted[1]) or \
                splitted[2] != '!=' or \
                splitted[3] != '0' or \
                splitted[4] != 'GOTO' or \
                not is_label(splitted[5]):
                raise Exception(f'IF_GOTO_ERROR: line "{line}"')
            return
        elif is_variable(splitted[0]):
            if len(splitted) < 3:
                raise Exception(f'COMMAND_LENGTH_ERROR: "{line}"')
            if splitted[1] != '<-' or \
                not is_variable(splitted[2]) or \
                splitted[0] != splitted[2]:
                raise Exception(f'COMMAND_ERROR: line "{line}"')
            elif len(splitted) > 3 and \
                (splitted[3] not in ['-', '+'] or \
                 splitted[4] != '1'):
                raise Exception(f'COMMAND_TYPE_ERROR: line "{line}"')
            return
        raise Exception(f'ERROR: line "{line}"')

    def code_line(self, line):
        self.check_line(line)

        def code_label(label_raw):
            label = label_raw[0]
            label_i = 1 if label_raw[1:] == '' else int(label_raw[1:])
            return LABELS.index(label) + 1 + len(LABELS) * (label_i - 1)

        def code_variable(variable_raw):
            if variable_raw == VARIABLES[0]: # Y
                return 0

            index = VARIABLES.index(variable_raw[0])
            var_i = 1 if variable_raw[1:] == '' else int(variable_raw[1:])
            return index + 2 * (var_i - 1)

        splitted = line.split()

        if splitted[0][0] == '[':
            splitted = ['[', splitted[0].replace('[', '').replace(']', ''), ']'] + splitted[1:]

        a = code_label(splitted[1]) if splitted[0] == '[' else 0

        if '<-' in splitted:
            if '+' in splitted:
                b = 1
            elif '-' in splitted:
                b = 2
            else:
                b = 0

            c = code_variable(splitted[0]) if a == 0 else code_variable(splitted[3])
        else:
            b = 2 + code_label(splitted[-1])
            c = code_variable(splitted[1]) if a == 0 else code_variable(splitted[4])

        return self.pair(a, self.pair(b, c))

    def code_program(self):
        godel = 1

        for i, line in enumerate(self.sfilecontent):
            godel *= PRIMES[i] ** self.code_line(line)

        return godel - 1

if __name__ == '__main__':
    try:
        s2g = s_lang_to_godel()
        s2g.load_S('code.s')
        print(s2g.code_program())
    except Exception as e:
        print(e)