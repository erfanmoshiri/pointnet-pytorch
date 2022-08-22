import torch.utils.data as data
import torch.utils.data as data
import os
import os.path
import torch
import numpy as np


class MyDataset(data.Dataset):
    def __init__(self,
                 root,
                 npoints=2500,
                 classification=False,
                 class_choice=None,
                 split='train',
                 data_augmentation=True):
        self.npoints = npoints
        self.root = root
        self.catfile = os.path.join(self.root, 'synsetoffset2category.txt')
        self.cat = {}
        self.data_augmentation = data_augmentation
        self.classification = classification
        self.seg_classes = {}

        self.cat = {
            'Airplane': 0, 
            'Bag': 1, 
            'Cap': 2, 
            'Car': 3, 
            'Chair': 4, 
            'Earphone': 5, 
            'Guitar': 6, 
            'Knife': 7, 
            'Lamp': 8, 
            'Laptop': 9, 
            'Motorbike': 10, 
            'Mug': 11, 
            'Pistol': 12, 
            'Rocket': 13, 
            'Skateboard': 14, 
            'Table': 15
        }
        self.id2cat = {v: k for k, v in self.cat.items()}

        self.classes = dict(zip(sorted(self.cat), range(len(self.cat))))
        print(self.classes)

    # ---------------------------------------------------------#
    def __getitem__(self, index):
        point_set = np.loadtxt(self.root).astype(np.float32)

        choice = np.random.choice(len(point_set), len(point_set), replace=True)
        #resample
        point_set = point_set[choice, :]

        point_set = point_set - np.expand_dims(np.mean(point_set, axis = 0), 0) # center
        dist = np.max(np.sqrt(np.sum(point_set ** 2, axis = 1)),0)
        point_set = point_set / dist #scale

        if self.data_augmentation:
            theta = np.random.uniform(0,np.pi*2)
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
            point_set[:,[0,2]] = point_set[:,[0,2]].dot(rotation_matrix) # random rotation
            point_set += np.random.normal(0, 0.02, size=point_set.shape) # random jitter

        point_set = torch.from_numpy(point_set)

        return point_set, torch.tensor(1)

    def __len__(self):
        return 1