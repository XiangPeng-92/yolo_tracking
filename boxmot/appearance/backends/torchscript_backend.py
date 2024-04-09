from pathlib import Path

import numpy as np
import torch

from boxmot.appearance.backends.base_backend import BaseModelBackend
from boxmot.utils import logger as LOGGER
from boxmot.utils.checks import TestRequirements

tr = TestRequirements()


class TorchscriptBackend(BaseModelBackend):
    def __init__(self, weights, device, half):
        super().__init__(weights, device, half)
        self.nhwc = False
        self.half = half

    def load_model(self, w):
        LOGGER.info(f"Loading {w} for TorchScript inference...")
        self.model = torch.jit.load(w)
        self.model.half() if self.half else self.model.float()

    def forward(self, im_batch):
        features = self.model(im_batch)
        return features
