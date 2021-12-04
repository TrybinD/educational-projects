import pygame
import numpy as np
import sys


def sigmoid(z):
    """
    Сигмоида
    """
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    """
    Производная сигмоиды по по x
    """
    return sigmoid(z) * (1 - sigmoid(z))

class Screen():
    def __init__(self, m_size = (500, 500), p_size = 1):
        self.screen_matrix = [[0 for _ in range(m_size[0])]
                              for _ in range(m_size[1])]
        self.p_size = p_size
        self.coordinates = (np.array([[x, y] for y in range(m_size[0])
                                for x in range(m_size[1])]) - 25) / 25


    def render(self, win, gradient = True):
        for y, i in enumerate(self.screen_matrix):
            for x, color in enumerate(i):
                if gradient:
                    color = 10*(color - 0.5)
                    color = sigmoid(color)
                else:
                    color = 1 if color > 0.5 else 0

                pygame.draw.rect(win, (255, 255 * color, 255 * color),
                                 pygame.Rect(x * self.p_size,
                                             y * self.p_size,
                                             self.p_size,
                                             self.p_size))


class Points():
    def __init__(self, p_size = 5):
        self.p_size = p_size
        self.points = []
        self.answers = []

    def render(self, win):
        for point, color in self.points:
            pygame.draw.circle(win, color, point,
                               self.p_size)

class Network():
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """
        Вычислить и вернуть выходную активацию нейронной сети
        при получении ``a`` на входе. a - список данных
         [[данные], [данные], [данные]].
        """
        a = a.T
        for b, w in zip(self.biases[:-1], self.weights[:-1]):
            a = sigmoid(w @ a + b)
        output = self.weights[-1] @ a + self.biases[-1]
        output = sigmoid(output)

        return output

    def learn(self, training_data, lr):
        '''На вход подается учебный кортеж
        (coord, 1). Происходит обратное распостраение
        ошибки и смена весов'''
        if training_data:
            nabla_b = [np.zeros(b.shape) for b in self.biases]
            nabla_w = [np.zeros(w.shape) for w in self.weights]
            for x, y in training_data: # из списка данных для обучение берем по 1 значениню
                delta_nabla_b, delta_nabla_w = self.backprop(x, y)
                nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
                nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]

            eps = lr / len(training_data)
            self.weights = [w - eps * nw for w, nw in zip(self.weights, nabla_w)]
            self.biases = [b - eps * nb for b, nb in zip(self.biases, nabla_b)]


    def backprop(self, x, y):
        """
        Возвращает кортеж ``(nabla_b, nabla_w)`` -- градиент целевой функции по всем параметрам сети.
        ``nabla_b`` и ``nabla_w`` -- послойные списки массивов ndarray,
        такие же, как self.biases и self.weights соответственно.
        Бекпроп для каждого примера ОТДЕЛЬНО!!!
        х - координата 1 точки! у - число 0 или 1
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # прямое распространение
        activation = x
        activations = [x]  # лист, хранящий все активации, слой за слоем
        zs = []  # лист, хранящий все z векторы, слой за слоем

        for b, w in zip(self.biases, self.weights):
            z = w @ activation + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)

        # обратное распространение
        delta = (activations[-1] - y) * sigmoid_prime((zs[-1]))
        nabla_b[-1] = delta
        nabla_w[-1] = delta @ activations[-2].T

        #Здесь l = 1 означает последний слой,
        # l = 2 - предпоследний и так далее.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = (self.weights[-l + 1].T @ delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].T)
        return nabla_b, nabla_w

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Classifier")
screen = Screen(m_size=(50, 50), p_size=10)
points = Points()
network = Network([2, 3, 2, 1])
# network.biases = [np.array([[0]])]
# network.weights = [np.array([[1, -1]])]
output = network.feedforward(screen.coordinates)
screen.screen_matrix = output.reshape(50, 50)
while True:

    mp = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            points.points.append((mp, (0, 0, 0)))
            points.answers.append(((np.array([mp]).T//10-25) / 25, 1))
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:
            points.points.append((mp, (0, 0, 255)))
            points.answers.append(((np.array([mp]).T//10-25) / 25, 0))

    network.learn(points.answers, 10)
    output = network.feedforward(screen.coordinates)
    screen.screen_matrix = output.reshape(50, 50)

        # elif ev.type == pygame.MOUSEBUTTONDOWN:
        #     points.points.append(mp)
        #     points.answers.append((np.array(mp)//10, 0))
        #     network.learn(points.answers, 0.1)
        #     output = network.feedforward(screen.coordinates)
        #     screen.screen_matrix = output.reshape(50, 50)

    screen.render(win)
    points.render(win)
    pygame.display.flip()





