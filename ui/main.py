import requests


base_url = "http://127.0.0.1:8000"

fields = {}

def menu():
    print('Tables')
    print('1: connection')
    print('2: connection_operator')
    print('3: subscriber')

    table = input('Pick a table: ')

    match table:
        case "connection" | "connection_operator" | "subscriber":
            do_operations(table)
        case _:
            print('Wrong table. Pick another one.')


def main():
    while True:
        menu()

if __name__ == '__main__':
    main()
