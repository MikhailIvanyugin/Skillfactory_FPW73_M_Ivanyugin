from random import randint

class FieldException(Exception):
    pass

class FieldOutOfException(FieldException):
    def __str__(self):
        return "Выстрел вне поля!"

class FieldExistException(FieldException):
    def __str__(self):
        return "Сюда стрелять уже нельзя, выберите другие координаты!"

class FieldWrongShipException(FieldException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x},{self.y})"

class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation
        self.lifes = length

    @property
    def shipform(self):
        ship_form = []
        for i in range(self.length):
            current_x = self.bow.x
            current_y = self.bow.y

            if self.orientation == 0:
                current_x += i
            elif self.orientation == 1:
                current_y += i

            ship_form.append(Dot(current_x, current_y))

        return ship_form

    def crackshot(self, shot):
        return shot in self.shipform

class Battlefield:
    def __init__(self, hide=False, size=6):
        self.hide = hide
        self.size = size
        self.newfield = [[" "]*size for _ in range(size)]
        self.count = 0
        self.occupied = []
        self.ships = []

    def __str__(self):
        new_field = ""
        new_field += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.newfield):
            new_field += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hide:
            new_field = new_field.replace("■", " ")
        return new_field

    def outofbattlefield(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        surroundings = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.shipform:
            for dx, dy in surroundings:
                current = Dot(d.x + dx, d.y + dy)
                if not(self.outofbattlefield(current)) and current not in self.occupied:
                    if verb:
                        self.newfield[current.x][current.y] = "."
                    self.occupied.append(current)

    def add_ship(self, ship):
        for d in ship.shipform:
            if self.outofbattlefield(d) or d in self.occupied:
                raise FieldWrongShipException()
        for d in ship.shipform:
            self.newfield[d.x][d.y] = "■"
            self.occupied.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.outofbattlefield(d):
            raise FieldOutOfException()

        if d in self.occupied:
            raise FieldExistException()

        self.occupied.append(d)

        for ship in self.ships:
            if ship.crackshot(d):
                ship.lifes -= 1
                self.newfield[d.x][d.y] = "X"
                if ship.lifes == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.newfield[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.occupied = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except FieldException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            your_shot = input("Ваш ход: ").split()

            if len(your_shot) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = your_shot

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.hide = True

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def try_board(self):
        length_of_ships = [3, 2, 2, 1, 1, 1, 1]
        new_battlefield = Battlefield()
        attempts = 0
        for lens in length_of_ships:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, 5), randint(0, 5)), lens, randint(0, 1))
                try:
                    new_battlefield.add_ship(ship)
                    break
                except FieldWrongShipException:
                    pass
        new_battlefield.begin()
        return new_battlefield

    def random_board(self):
        new_battlefield = None
        while new_battlefield is None:
            new_battlefield = self.try_board()
        return new_battlefield

    def greet(self):
        print(f"""
    Добро пожаловать в игру "морской бой"!
    Для выстрела введите две координаты поля боя,
    сначала по горозинтали, затем по вертикали.
    Удачи!
        """)

    def gameplay(self):
        num = 0
        while True:
            print()
            print("Доска игрока:")
            print(self.us.board)
            print()
            print("Доска компьютера:")
            print(self.ai.board)
            print()
            if num % 2 == 0:
                repeat = self.us.move()
            else:
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == len(self.ai.board.ships):
                print()
                print("Доска игрока:")
                print(self.us.board)
                print()
                print("Доска компьютера:")
                print(self.ai.board)
                print()
                print("Вы выиграли!")
                break

            if self.us.board.count == len(self.ai.board.ships):
                print()
                print(self.us.board)
                print(self.ai.board)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.gameplay()

game = Game()
game.start()
