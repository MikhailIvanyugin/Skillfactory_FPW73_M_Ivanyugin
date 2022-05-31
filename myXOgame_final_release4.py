def print_welcome_text():
    print(f"""
    Добро пожаловать в игру крестики-нолики! 
    Правила ввода данных: укажите желаемую клетку из таблицы - сначала букву, затем цифру, например, a3 или B2 
    Удачи!
        """)

def create_battlefield():
    print()
    print(f'  | A | B | C |')
    print('----------------')
    for first_column in range(1, 4):
        row = " | ".join(battlefield[first_column-1])
        print(f'{first_column} | {row} |')
        print('----------------')
    print()

def input_coordinates():
    while True:
        global cell
        cell = input('Введите клетку поля: ').upper()
        print()
        coordinates = list(cell)
        if len(coordinates) != 2:
            print('Неверный ввод, читайте правила! ')
            continue

        if 'A' not in coordinates[0] and 'B' not in coordinates[0] and 'C' not in coordinates[0]:
            print('Неверный ввод, читайте правила! ')
            continue

        if coordinates[0] == 'A':
            coordinates[0] = 1
        elif coordinates[0] == 'B':
            coordinates[0] = 2
        elif coordinates[0] == 'C':
            coordinates[0] = 3       # приводим буквенные значения координат к формату int

        if '1' not in coordinates[1] and '2' not in coordinates[1] and '3' not in coordinates[1]:
            print('Неверный ввод, читайте правила! ')
            continue

        coordinates[0], coordinates[1] = int(coordinates[1]), coordinates[0]
        # приводим строки 1 2 3 к формату int и меняем местами координаты для корректной работы с ними

        if battlefield[(coordinates[0]-1)][(coordinates[1]-1)] != ' ':
            print('Данная клетка уже занята! ')
            continue

        return coordinates

def get_winner():
    winning_combinations = [
                            ['A1', 'A2', 'A3'], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3'],
                            ['A1', 'B1', 'C1'], ['A2', 'B2', 'C2'], ['A3', 'B3', 'C3'],
                            ['A1', 'B2', 'C3'], ['A3', 'B2', 'C1']
                            ]
    for every_variant in winning_combinations:
        variant = set(every_variant)
        if variant.issubset(current_set_X):
            print('Победа крестиков! ')
            return True
        elif variant.issubset(current_set_O):
            print('Победа ноликов! ')
            return True
    return False

print_welcome_text()

battlefield = [[' '] * 3 for i in range(3)]
total_number_of_moves = 0
current_set_X = set()   # создаем множество, в которое будем записывать все ходы крестиков
current_set_O = set()   # то же для ноликов

while True:

    total_number_of_moves += 1

    create_battlefield()

    if total_number_of_moves % 2 == 1:
        print('Ход крестика ')
    else:
        print('Ход нолика ')

    coordinate_1, coordinate_2 = input_coordinates()

    if total_number_of_moves % 2 == 1:
        battlefield[coordinate_1 - 1][coordinate_2 - 1] = "X"
        current_set_X.add(cell)   # добавляем в соответствующее множество введенную пользователем клетку
        if get_winner():          # и сразу проверяем, входит ли какая-нибудь выигрышная комбинация в наше множество
            create_battlefield()
            break
    else:
        battlefield[coordinate_1 - 1][coordinate_2 - 1] = "O"
        current_set_O.add(cell)
        if get_winner():
            create_battlefield()
            break

    if total_number_of_moves == 9:
        create_battlefield()
        print('Ничья! Победила дружба! ')
        break

# для большей реалистичности можно реализовать досрочную ничью по согласию игроков,
# так как игра может быть сведена в ничью до того, как произойдет 9 ходов.
