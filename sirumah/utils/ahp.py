import numpy as np

class AHP:
    def __init__(self, scoring=None):
        self.matrix = None
        self.scoring = scoring
        self.n = len(self.scoring)
    
    def __call__(self):
        if self.matrix is not None:
            return self._from_matrix(self.matrix)
        elif self.scoring is not None:
            return self._from_scoring(self.scoring)
        else:
            raise ValueError("Either matrix or scoring must be provided.")
        
    @property
    def weights(self):
        return self.__calculate_weights()

    def __comparsion(self):
        M = np.zeros((self.n, self.n))

        if self.n < 6:
            for i in range(self.n):
                for j in range(self.n):
                    M[j, i] = self.scoring[i] / self.scoring[j]
                    
        else:
            for i in range(self.n):
                for j in range(self.n):
                    M[i, j] = self.scoring[i] - self.scoring[j]
        
        self.matrix = M

        return M
    
    def __transform(self):
        M = np.zeros((self.n, self.n))
        
        if self.n < 6:
            for i in range(self.n):
                for j in range(self.n):
                    if self.matrix[i, i] / self.matrix[i ,j] < 1:
                        M[i, j] = ((self.matrix[i, j] / self.matrix[i, i] - 1) * 8 / (self.n - 1)) + 1
                    elif self.matrix[i, i] / self.matrix[i, j] == 1:
                        M[i, j] = 1
                    else:
                        M[i, j] = 1 / (((self.matrix[i, i] / self.matrix[i, j] - 1) * 8 / (self.n - 1)) + 1)
        else:
            for i in range(self.n):
                for j in range(self.n):
                    if self.matrix[i, j] < 0:
                        M[i, j] = (8 / (self.n - 1)) * np.abs(self.matrix[i, j]) + 1
                    elif self.matrix[i, j] == 0:
                        M[i, j] = 1
                    else:
                        M[i, j] = 1 / ((8 / (self.n - 1)) * np.abs(self.matrix[i, j]) + 1)

        self.matrix = M
        return M
    
    def __calculate_weights(self):
        self.__comparsion()
        pairwise_matrix = self.__transform()

        M = pairwise_matrix / pairwise_matrix.sum(axis=0)
        weights = M.mean(axis=1)

        return weights.tolist()