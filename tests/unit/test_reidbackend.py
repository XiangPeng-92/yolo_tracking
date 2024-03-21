from pathlib import Path

import cv2
import numpy as np
import pytest

from boxmot.appearance.reid_multibackend import ReIDDetectMultiBackend
from boxmot.utils import ROOT

REID_MODELS = [Path("osnet_x0_25_msmt17.pt"), Path("osnet_x1_0_dukemtmcreid.pt")]


@pytest.mark.parametrize("reid_model", REID_MODELS)
def test_reidbackend_output(reid_model):
    r = ReIDDetectMultiBackend(weights=reid_model, device="cpu", fp16=False)

    img = cv2.imread(
        str(ROOT / "assets/MOT17-mini/train/MOT17-04-FRCNN/img1/000001.jpg")
    )
    dets = np.array([[144, 212, 578, 480, 0.82, 0], [425, 281, 576, 472, 0.56, 65]])

    embs = r.get_features(dets[:, 0:4], img)
    assert embs.shape[0] == 2  # two crops should give two embeddings
    assert embs.shape[1] == 512  # osnet embeddings are of size 512
