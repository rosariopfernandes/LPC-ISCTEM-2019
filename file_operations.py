import outputs


def read_lines_from_file(filename: str):
    try:
        return [line.rstrip('\n') for line in open(filename)]
    except FileNotFoundError:
        outputs.print_file_not_found()
        return []
