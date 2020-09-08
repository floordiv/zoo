from os.path import expanduser


def remove_spaces(text):
    in_string = False
    result = ''

    for letter in text:
        if letter == ' ' and not in_string:
            continue

        if letter == '"':
            in_string = not in_string

        result += letter

    return result


def split_by_equality(text):
    text = remove_spaces(text)
    temp = ['']

    for letter in text:
        if letter == '=':
            temp.append('')
        else:
            temp[-1] += letter

    return temp


def parse_value(value):
    value = value.rstrip()

    if value[0] == '"' and value[-1] == '"':
        return value[1:-1]
    elif value in ('true', 'false'):
        return value == 'true'
    elif value.isdigit():
        return int(value)
    elif value.replace('.', '').isdigit():
        return float(value)

    return value  # also string, but without quotes


def load(path, ignore_case=True):
    data = {}

    with open(path) as fd:
        for line_index, line in enumerate(fd):
            if line.strip().strip('\t') == '':
                continue

            keyvalue = split_by_equality(line)

            if len(keyvalue) != 2:
                return print(f'[CONFIG] Error: service-file "{path}" has bad syntax on line {line_index}')

            key, value = keyvalue

            if ignore_case:
                key = key.lower()

            data[key] = parse_value(value)

    return data
