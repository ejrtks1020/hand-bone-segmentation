# python native
import os

# external library
import cv2
import numpy as np

# torch
import torch
from torch.utils.data import Dataset


class XRayInferenceDataset(Dataset):
    def __init__(self, args, pngs, transforms=None):
        self.args = args
        self.pngs = pngs

        _filenames = self.pngs
        _filenames = np.array(sorted(_filenames))

        self.filenames = _filenames
        self.transforms = transforms

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, item):
        image_name = self.filenames[item]
        image_path = os.path.join(self.args.test_image_dir, image_name)

        image = cv2.imread(image_path)
        image = image / 255.0

        if self.transforms is not None:
            inputs = {"image": image}
            result = self.transforms(**inputs)
            image = result["image"]

        # to tenser will be done later
        image = image.transpose(2, 0, 1)  # make channel first

        image = torch.from_numpy(image).float()

        return image, image_name
