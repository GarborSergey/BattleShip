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
