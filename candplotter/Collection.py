

class MyCollection(object):

    def __init__(self, df):
        self._df = df
        self._orig_df = df
        self.symbols = [".", "o", "+", "x", "v", "^", "*", "s"]
        self.colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
        self.alpha = 0.75
        #self.mask = ~(self.df == np.nan)
        self.keys = list(self.df.keys())
        self._X_label = self.keys[0]
        self._Y_label = self.keys[0]
        self.size_label = self.keys[0]
        self.color_label = self.keys[1]

    @property
    def df(self):
        return self._df
    
    def reset_df(self):
        self._df = self._orig_df

    def save_region_mask(self, x1, x2, y1, y2):
        self.mask = (x1 < self.df[self.X_label]) &\
                    (self.df[self.X_label] < x2) &\
                    (y1 < self.df[self.Y_label]) &\
                    (self.df[self.Y_label] < y2)
        
    def select_mask(self):
        self._df = self.df[self.mask]

    def deselect_mask(self):
        self._df = self.df[~self.mask]
        
    @property
    def X_label(self):
        return self._X_label

    def set_X_label(self, new_label):
        if new_label not in self.keys:
            raise ValueError(f"New X label {new_label} not in self.keys: {self.keys}")
        self._X_label = new_label

    @property
    def Y_label(self):
        return self._Y_label

    def set_Y_label(self, new_label):
        if new_label not in self.keys:
            raise ValueError(f"New Y label {new_label} not in self.keys: {self.keys}")
        self._Y_label = new_label

    def set_size_label(self, axis_label):
        if axis_label not in self.keys:
            raise ValueError(f"New size label (axis_label) not in self.keys: {self.keys}")
        self.size_label = axis_label

    def set_color_label(self, axis_label):
        if axis_label not in self.keys:
            raise ValueError(f"New color label (axis_label) not in self.keys: {self.keys}")
        self.color_label = axis_label
        
    def on_pick(self, event):
        ind = event.ind
        print(self.df.iloc[ind])
