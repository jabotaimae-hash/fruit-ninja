"""Regression checks without opening a camera or a game window.

Run with the game's Python: python -B -m unittest discover -s tests
"""

import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

import mediapipe as mp
import numpy as np
import pygame


class HandTrackingTests(unittest.TestCase):
    def setUp(self):
        # Load the real camera functions without running the top-level game loop.
        source_path = Path(__file__).resolve().parent.parent / "fruit_ninja.py"
        if not source_path.exists():
            source_path = Path(__file__).with_name("fruit_ninja.py")
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        functions = ast.Module(
            body=[node for node in tree.body if isinstance(node, ast.FunctionDef)],
            type_ignores=[],
        )
        self.frame = pygame.Surface((640, 480))
        for color, rect in [
            ((255, 0, 0), (0, 0, 320, 240)),
            ((0, 255, 0), (320, 0, 320, 240)),
            ((0, 0, 255), (0, 240, 320, 240)),
            ((255, 255, 0), (320, 240, 320, 240)),
        ]:
            pygame.draw.rect(self.frame, color, rect)
        self.camera = Mock()
        self.camera.query_image.return_value = True
        self.camera.get_image.return_value = self.frame
        self.tracker = Mock()
        self.tracker.detect_for_video.return_value = SimpleNamespace(
            hand_landmarks=[], handedness=[]
        )
        self.state = {
            "pygame": pygame, "np": np, "mp": mp,
            "WIDTH": 1000, "HEIGHT": 600,
            "camera_capture": self.camera, "camera_surface": None,
            "camera_error": "", "camera_frame_counter": 0,
            "hand_landmarker": self.tracker, "hand_timestamp": 0,
        }
        exec(compile(functions, str(source_path), "exec"), self.state)
        self.state["reset_hand_sensor"]()

    def update_frame(self):
        for _ in range(3):
            self.state["update_camera"]()
        self.assertEqual(self.state["camera_error"], "")

    def test_tracker_receives_the_same_pixels_as_the_camera_preview(self):
        self.update_frame()
        image, _ = self.tracker.detect_for_video.call_args.args
        mirrored = pygame.transform.flip(self.frame, True, False)
        expected = pygame.surfarray.array3d(mirrored).transpose(1, 0, 2)
        np.testing.assert_array_equal(image.numpy_view(), expected)

    def test_fingertip_movement_hits_fruit_and_lost_hand_clears_blade(self):
        def result(x):
            landmarks = [SimpleNamespace(x=x, y=0.5) for _ in range(21)]
            return SimpleNamespace(
                hand_landmarks=[landmarks],
                handedness=[[SimpleNamespace(category_name="Right")]],
            )

        self.tracker.detect_for_video.return_value = result(0.2)
        self.update_frame()
        self.assertEqual(self.state["hand_positions"][1], (200, 300))
        self.assertEqual(self.state["hand_blade_segments"], [])
        self.tracker.detect_for_video.return_value = result(0.8)
        self.update_frame()
        start, end = self.state["hand_blade_segments"][0]
        fruit = SimpleNamespace(x=500, y=300, radius=35)
        self.assertTrue(self.state["check_blade_collision"](fruit, start, end))
        self.tracker.detect_for_video.return_value = SimpleNamespace(
            hand_landmarks=[], handedness=[]
        )
        self.update_frame()
        self.assertEqual(self.state["hand_blade_segments"], [])
        self.assertEqual(self.state["hand_positions"], [None, None])
        self.assertEqual(self.state["hand_trails"], [[], []])


if __name__ == "__main__":
    unittest.main()
