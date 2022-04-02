from random import randint
# Класс точка
class Dot:
    # Конструктор
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Сравнение точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Вывод
    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


# Классы исключений игры
# Класс - родитель
class BoardException(Exception):
    pass


class OutException(BoardException):
    def __str__(self):
        return 'Нельзя стрелять за пределами доски!'


class UsedException(BoardException):
    def __str__(self):
        return 'В это место уже стреляли! Зачем тратить снаряды напрасно?'

class WrongShipException(BoardException):
    pass

# Класс коробля
class Ship:
    # Конструктор
    def __init__(self, bow, l, o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    # Вычисляет точки корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            pos_x = self.bow.x
            pos_y = self.bow.y

            # Горизонтальный
            if self.o == 0:
                pos_x += i
            # Вертикальный
            elif self.o == 1:
                pos_y += i

            ship_dots.append(Dot(pos_x, pos_y))
        # Возвращает список с точками корабля
        return ship_dots

    # Проверка попадания в корабль
    def hit(self, shot):
        return shot in self.dots


# Класс игровое поле
class Board:
    def __init__(self, hidden=False, size=6):
        self.hidden = hidden
        self.size = size
        self.count = 0  # Количество пораженных кораблей
        self.field = [['0'] * size for _ in range(size)]  # Поле игры
        self.busy = []  # Занятые точки
        self.ships = []  # Список кораблей доски

    # Печать игрового поля
    def __str__(self):
        res = ''
        res += '   | 1 | 2 | 3 | 4 | 5 | 6 |\n----------------------------'
        # Проход по строкам игрового поля с индексом
        for i, row in enumerate(self.field):
            res += f'\n{i+1}  | ' + ' | '.join(row) + " |" + '\n----------------------------'

        if self.hidden:
            res = res.replace("■", '0')
        return res

    # Проверка выходит ли точка за пределы игрового поля
    def out(self, d):
        return not ((0 <= d.x <= self.size) and (0 <= d.y <= self.size))

    # Заполнение соседних точек корабля
    def counter(self, ship, verb=False):
        # Список соседних точек
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1) , (0, 0) , (0, 1),
            (1, -1) , (1, 0) , (1, 1)
        ]
        # Проход по точкам корабля
        for d in ship.dots:
            # Проход по списку near
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = '.'
                    self.busy.append(cur)
    # Размещение корабля
    def add_ship(self, ship):
        for d in ship.dots:
            # Каждая точка корабля не выходит за границы поля и не занята
            if self.out(d) or d in self.busy:
                raise WrongShipException()
        # Отрисовка корабля
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            # Запись точки в список занятых
            self.busy.append(d)

        self.ships.append(ship)
        self.counter(ship)

    # Выстрел
    def shot(self, d):
        # Проверка что выстрел в пределах игрового поля
        if self.out(d):
            raise OutException()
        # Проверка что выстрел не повторяется
        if d in self.busy:
            raise UsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shot(d):
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.counter(ship, verb=True)
                    print('Корабль уничтожен!')
                    return False
                else:
                    print('Корабль ранен!')
                    return True

        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    # Начало игры
    def begin(self):
        self.busy = []

# Класс игрока
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
            except BoardException as e:
                print(e)

# Класс игрока компьютера
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

# Класс игрока пользователя
class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ХОД ---> ').split()

            if len(cords) != 2:
                print('Введите две координаты!')
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа')
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)
b1 = Board()
b1.add_ship(Ship(Dot(1, 2), 4, 0))
print(b1)