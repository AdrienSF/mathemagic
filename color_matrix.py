import random
import numpy as np
from pylatex import NoEscape

class ColorMatrix(object):
    def __init__(self):
        self.rgbDict = {'white': [0,0,0],
                    'black': [1,1,1],
                    'red': [255/255, 46/255, 21/255],
                    'yellow': [254/255, 215/255, 43/255],
                    'turquoise': [122/255, 187/255, 129/255],
                    'blue': [36/255, 135/255, 255/255],
                    'purple': [183/255, 133/255, 254/255],
                    'pink': [255/255, 83/255, 201/255],
                    'orange': [254/255, 141/255, 0/255],
                    'green': [65/255, 192/255, 27/255],
                    'light_blue': [70/255, 205/255, 237/255],
                    'rust': [139/255, 13/255, 0/255],
                    'brown': [124/255, 70/255, 5/255],
                    'dark_green': [3/255, 98/255, 40/255],
                    'dark_blue': [12/255, 80/255, 203/255]
                    }
        
        self.strDict = self.get_strDict()

    def get_strDict(self, rgbDict=None):
        if rgbDict == None:
            rgbDict = self.rgbDict
        
        return { key: '\definecolor{' + str(key) + '}{rgb}{' + ','.join([str(v) for v in val]) + '}' for key, val in rgbDict.items()}


    def get_color_matrix(self, n: int, m: int):
        color_list = list(self.strDict.keys())
        random.shuffle(color_list)
        color_iter = iter(color_list)
        matrix = []
        for i in range(n):
            to_add = []
            for j in range(m):
                color_name = next(color_iter, None)
                if color_name == None:
                    color_name = random.choice(color_list)
                to_add.append(NoEscape(color_name))
            matrix.append(to_add)

        return np.array(matrix)


    def get_doctored_matrix(self, matrix: np.array, coord_dict: dict):
        # for coords in coord_dict:
        #     matrix[coords] = coord_dict[coords]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                for coords, color in coord_dict.items():
                    if matrix[i][j] == color:
                       matrix[i][j] = matrix[coords]

        for coords, color in coord_dict.items():
            matrix[coords] = color 

        return matrix
