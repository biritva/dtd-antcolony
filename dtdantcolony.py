import sys
import numpy as np

class Colony(object):
'''Класс отвечающий за решение '''

    def __init__(self, dist, ants, best, iterations, decay, a=1, b=1): 
    ''' Конструктор класса, ввод основных параметров'''
        self.dist  = dist.astype(np.float64) #матрица растояний
        self.dist[self.dist==0] = np.inf
        self.pheromone = np.ones(self.dist.shape) / len(dist) #инициализация матрицы отложений феромона
        self.allind = range(len(dist))
        self.iterations = iterations
        self.decay = decay #коэффициент распада феромона
        self.ants = ants #число муравьев
        self.best = best #число улучшенных муравьев
        self.a = a #коэффициент феромона
        self.b = b #коэффициент растояния      

    def start(self):
    ''' Функция запуска основного цикла расчёта колонии'''
        pathshort = None
        alltimepathshort = ("", np.inf)
        while(self.iterations):            
            pathsall = self.genallpaths()
            self.pheromon(pathsall, self.best, pathshort=pathshort)
            pathshort = min(pathsall, key=lambda x: x[1])            
            if pathshort[1] < alltimepathshort[1]:
                alltimepathshort = pathshort             
            self.pheromone * self.decay        
            self.iterations -= 1         
        return alltimepathshort[1]

    def pheromon(self, pathsall, best, pathshort):
        sortedpaths = sorted(pathsall, key=lambda x: x[1])
        for path, dist in sortedpaths[:best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.dist[move]

    def pathgendst(self, path):
        totaldst = 0
        for el in path:
            totaldst += self.dist[el]
        return totaldst

    def genallpaths(self):
        pathsall = []
        for i in range(self.ants):
            path = self.pathgen(0)
            pathsall.append((path, self.pathgendst(path)))
        return pathsall

    def pathgen(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.dist) - 1):
            move = self.pick(self.pheromone[prev], self.dist[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def pick(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.a * (( 1.0 / dist) ** self.b)
        norm_row = row / row.sum()
        move = np.random.choice(self.allind, 1, p=norm_row)[0]
        return move

ds = list(map(np.float64, input().split()))   
dst = np.zeros((len(ds), len(ds)))
dst[0] += ds
for i in range(1, len(ds)):
    ds = list(map(np.float64, input().split()))
    dst[i] += ds

ac = Colony(dst, 10, 5, 1000, 0.45, a=0.7, b=1.5)
weight = ac.start()
print (str(int(weight)))
