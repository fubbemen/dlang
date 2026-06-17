def read(filename):
    with open(filename, 'r', encoding='utf-8') as file:

        file_string = file.read()
    return file_string

