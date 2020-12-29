class ColorDict(object):
    def __init__(self):
        self.rgbDict = {'white': [0,0,0], 
                    'black': [1,1,1]
                    }
        
        self.strDict = self.getStrDict()

    def getStrDict(self, rgbDict=None):
        if rgbDict == None:
            rgbDict = self.rgbDict
        
        return { key: '\definecolor{' + str(key) + '}{rgb}{' + ','.join([str(v) for v in val]) + '}' for key, val in rgbDict.items()}