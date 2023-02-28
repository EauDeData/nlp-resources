import os
import random
from typing import *

class EsposallesTextDataset:

    '''
    
    Expected file tree:

        base_folder:
        |
        |___ gt/*
        |
        |___ transcripcions/*
    
    if ```download``` is True and ```base_folder``` is empty, the class will try to download the data.
        
    '''

    def __init__(self, base_folder: str = 'esposalles', download: bool = True, train_split = 0.9, shuffle = True) -> None:
        
        self.base_folder = base_folder
        self.split = train_split
        if not 'gt' in os.listdir(self.base_folder) and download: self.download_data()
        self.parse_data()
        self.registers = list(self.data.keys())
        self.train()
        if shuffle: random.shuffle(self.registers)
    
    def __len__(self):
        if self.offset: return int(len(self.registers) * (1 - self.split))
        return  int(len(self.registers) * self.split)

    def test(self):
        self.offset = int(len(self.data) * self.split)
    
    def train(self):
        self.offset = 0

    def __iter__(self):
        self.inner_state = 0
        return self

    def __getitem__(self, idx: int) -> Tuple[List[str], List[int]]:
        
        idx += self.offset
        register = self.registers[idx]
        x, gt =  self.data[register]
        
        return x.split(), [None if y == 'other' else y for y in gt.split()]

    def __next__(self):
        
        if self.inner_state > (len(self) - 1):
            self.inner_state += 1
            return self[self.inner_state - 1]
        
        raise StopIteration

    def download_data(self):
        pass

    def parse_data(self):
        
        get_stripped_lines = lambda x: ' '.join([x.strip().split(':')[-1] for x in open(x).readlines()])

        gt_files = sorted([f"{self.base_folder}/gt/{x}" for x in os.listdir(f"{self.base_folder}/gt/")])
        or_files = sorted([f"{self.base_folder}/transcripcions/{x}" for x in os.listdir(f"{self.base_folder}/transcripcions/")])

        self.data = dict()
        for or_, gt_ in zip(or_files, gt_files):
            orlines = get_stripped_lines(or_)
            gtlines = get_stripped_lines(gt_)

            self.data['-'.join((or_.split('_')[:-1])).split('/')[-1]] = (orlines, gtlines)

    def get_class_dict(self) -> Dict:
        pass


E = EsposallesTextDataset()
print(E[0], len(E))
E.test()

print(E[0], len(E))
E.train()

print(E[0], len(E))
