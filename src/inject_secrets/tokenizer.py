LEFT_DELIMITER = '{{'
RIGHT_DELIMITER = '}}'

class TokenizationError(Exception):
    def __init__(self, message):
        super().__init__(message)

def tokenize(input: str):
    template = input

    intermediate_result, remaining_template = tokenize_next_secret_path(template)
    result = intermediate_result

    while remaining_template:
        intermediate_result, remaining_template = tokenize_next_secret_path(remaining_template)
        result += intermediate_result

    return result


def tokenize_next_secret_path(template: str):
    if not template:
        return [], None

    split_result = template.split(LEFT_DELIMITER, 1)

    if len(split_result) == 1:
        return [('literal', template)], None

    literal, remaining_template = split_result

    result = []
    if literal:
        result.append(('literal', literal))

    split_result = remaining_template.split(RIGHT_DELIMITER, 1)
    if len(split_result) == 1:
        raise TokenizationError("Missing right delimiter at '{remaining_template[:30]}'")

    secret_path, remaining_template = split_result
    result.append(('secret_path', secret_path.strip()))

    return result, remaining_template

