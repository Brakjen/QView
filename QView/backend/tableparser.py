import pandas as pd
import numpy as np
from pprint import pprint


class TableParser:
    def __init__(self, tabular, width):
        self.tabular = tabular
        self.width = width

    def parseQueue(self):
        q = []
        for line in self.tabular.splitlines():
            row = []
            for i in range(int(len(line) / self.width)):
                start = i*self.width
                stop = (i+1)*self.width
                item = line[start:stop].strip()
                row.append(item)
            q.append(row)
        return q

    def parseHistory(self):
        table = [line.split('|') for line in self.tabular.splitlines()]
        return table

    def parseTop(self):
        table = [line.split() for line in self.tabular.splitlines()]
        return table
