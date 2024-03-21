from pathlib import Path

import numpy as np
import pytest
from numpy.testing import assert_allclose

from boxmot import (OCSORT, BoTSORT, BYTETracker, DeepOCSORT, StrongSORT,
                    create_tracker, get_tracker_config)
from boxmot.utils import WEIGHTS

MOTION_ONLY_TRACKING_METHODS = [OCSORT, BYTETracker]
MOTION_N_APPEARANCE_TRACKING_METHODS = [StrongSORT, BoTSORT, DeepOCSORT]
ALL_TRACKERS = ["botsort", "deepocsort", "ocsort", "bytetrack", "strongsort"]


@pytest.mark.parametrize("Tracker", MOTION_N_APPEARANCE_TRACKING_METHODS)
def test_tracker_instantiation(Tracker):
    Tracker(
        model_weights=Path(WEIGHTS / "osnet_x0_25_msmt17.pt"),
        device="cpu",
        fp16=True,
    )


@pytest.mark.parametrize("Tracker", MOTION_ONLY_TRACKING_METHODS)
def test_tracker_instantiation(Tracker):
    Tracker()


@pytest.mark.parametrize("tracker_type", ALL_TRACKERS)
def test_tracker_output_size(tracker_type):
    tracker_conf = get_tracker_config(tracker_type)
    tracker = create_tracker(
        tracker_type=tracker_type,
        tracker_config=tracker_conf,
        reid_weights=WEIGHTS / "mobilenetv2_x1_4_dukemtmcreid.pt",
        device="cpu",
        half=False,
        per_class=False,
    )

    rgb = np.random.randint(255, size=(640, 640, 3), dtype=np.uint8)
    det = np.array([[144, 212, 578, 480, 0.82, 0], [425, 281, 576, 472, 0.56, 65]])

    output = tracker.update(det, rgb)
    assert output.shape == (2, 8)  # two inputs should give two outputs
