import os
import random
import numpy as np

import torch
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler

CIFAR_MEAN = [0.49139968, 0.48215827, 0.44653124]
CIFAR_STD = [0.203, 0.1994, 0.2010]

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

class Cutout(object):#加入Cutout
    """Randomly mask out one or more patches from an image.
    Args:
        n_holes (int): Number of patches to cut out of each image.
        length (int): The length (in pixels) of each square patch.
    """
    def __init__(self, n_holes, length):
        self.n_holes = n_holes
        self.length = length

    def __call__(self, img):
        """
        Args:
            img (Tensor): Tensor image of size (C, H, W).
        Returns:
            Tensor: Image with n_holes of dimension length x length cut out of it.
        """
        h = img.size(1)
        w = img.size(2)

        mask = np.ones((h, w), np.float32)

        for n in range(self.n_holes):
        	# (x,y)表示方形补丁的中心位置
            y = np.random.randint(h)
            x = np.random.randint(w)

            y1 = np.clip(y - self.length // 2, 0, h)
            y2 = np.clip(y + self.length // 2, 0, h)
            x1 = np.clip(x - self.length // 2, 0, w)
            x2 = np.clip(x + self.length // 2, 0, w)

            mask[y1: y2, x1: x2] = 0.

        mask = torch.from_numpy(mask)
        mask = mask.expand_as(img)
        img = img * mask

        return img


def get_test_loader(dataset, data_path, batch_size, num_workers):
    test_transform = _get_test_transform(dataset)
    test_data = _get_dataset(dataset, data_path, test_transform, train=False)

    test_loader = _build_loader(
        test_data,
        False,
        batch_size,
        num_workers,
        sampler=None)
    return test_loader


def get_train_loader(
        dataset,
        data_path,
        batch_size,
        num_workers,
        train_portion=1):
    train_transform = _get_train_transform(dataset)
    train_data = _get_dataset(dataset, data_path, train_transform)

    if train_portion != 1:
        train_len = len(train_data)
        indices = list(range(train_len))
        random.shuffle(indices)
        split = int(np.floor(train_portion * train_len))
        train_idx, val_idx = indices[:split], indices[split:]

        train_sampler = SubsetRandomSampler(train_idx)
        val_sampler = SubsetRandomSampler(val_idx)

        train_loader = _build_loader(
            train_data,
            True,
            batch_size,
            num_workers,
            sampler=train_sampler)
        val_loader = _build_loader(
            train_data,
            False,
            batch_size,
            num_workers,
            sampler=val_sampler)

        return train_loader, val_loader
    else:
        train_loader = _build_loader(
            train_data,
            True,
            batch_size,
            num_workers,
            sampler=None)

        return train_loader


def _build_loader(dataset, shuffle, batch_size, num_workers, sampler=None):
    if sampler is not None:
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            pin_memory=True,
            num_workers=num_workers,
            sampler=sampler
        )
    else:
        return torch.utils.data.DataLoader(
            dataset,
            batch_size=batch_size,
            pin_memory=True,
            num_workers=num_workers,
            shuffle=shuffle,
        )


def _get_dataset(dataset, data_path, transform, train=True):
    if dataset == "cifar10":
        return datasets.CIFAR10(root=data_path, train=train,
                                download=True, transform=transform)

    elif dataset == "cifar100":
        return datasets.CIFAR100(root=data_path, train=train,
                                 download=True, transform=transform)

    elif dataset == "imagenet":
        return datasets.ImageFolder(root=data_path, transform=transform)

    else:
        raise


def _get_train_transform(dataset):
    if dataset[:5] == "cifar":
        # CIFAR transforms
        train_transform = transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(CIFAR_MEAN, CIFAR_STD),
            Cutout(n_holes=1, length=16)
        ])

    elif dataset == "imagenet":
        # Imagenet transforms
        train_transform = transforms.Compose([
            transforms.RandomResizedCrop(224, scale=(0.2, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
        ])

    return train_transform


def _get_test_transform(dataset):
    if dataset[:5] == "cifar":
        # CIFAR transforms
        test_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(CIFAR_MEAN, CIFAR_STD)
        ])

    elif dataset == "imagenet":
        # Imagenet transforms
        test_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
        ])

    return test_transform
