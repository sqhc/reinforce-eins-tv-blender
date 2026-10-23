# -*- coding: utf-8 -*-
"""Reinforce Eins (TV) - frozen spec. Units: meters, +Z up, -Y front."""
H = 1.680
Z_CHIN = 1.456
Z_HEAD_TOP = 1.680
Z_HEAD_C = 1.568
HEAD_H = 0.224
HEAD_W = 0.170
HEAD_D = 0.200
Z_SHOULDER = 1.344
Z_CHEST = 1.232
Z_WAIST = 1.008
Z_HIP = 0.840
Z_KNEE = 0.448
Z_ANKLE = 0.045
Z_SOLE = 0.0
SHOULDER_X = 0.165
HIP_X = 0.090
CHEST_W = 0.300
WAIST_W = 0.210
HIP_W = 0.320
CHEST_D = 0.190
WAIST_D = 0.150
HIP_D = 0.200
# arm chain (A-pose)
ARM = {
    "L": [(0.165, 0.000, 1.344), (0.335, 0.000, 1.110), (0.475, 0.000, 0.905), (0.525, -0.005, 0.815)],
    "R": [(-0.165, 0.000, 1.344), (-0.335, 0.000, 1.110), (-0.475, 0.000, 0.905), (-0.525, -0.005, 0.815)],
}
ARM_R = [0.056, 0.040, 0.030, 0.026]
LEG = {
    "L": [(0.090, 0.000, 0.870), (0.085, 0.005, 0.448), (0.075, 0.000, 0.060)],
    "R": [(-0.090, 0.000, 0.870), (-0.085, 0.005, 0.448), (-0.075, 0.000, 0.060)],
}
LEG_R = [0.088, 0.058, 0.040]
# wings: side -> (upper root, upper tip, lower root, lower tip)
WING = {
    "L": {"uroot": (0.070, 0.090, 1.290), "utip": (1.200, 0.420, 2.100),
          "lroot": (0.080, 0.090, 1.180), "ltip": (1.100, 0.380, 0.880)},
    "R": {"uroot": (-0.070, 0.090, 1.290), "utip": (-1.200, 0.420, 2.100),
          "lroot": (-0.080, 0.090, 1.180), "ltip": (-1.100, 0.380, 0.880)},
}
COLORS = {
    "skin": "#F0D2C1",
    "hair": "#D7DCE4",
    "dress": "#16171D",
    "dress2": "#1C1D24",
    "white": "#E8E8EA",
    "gold": "#D8B24A",
    "stocking": "#0E0F14",
    "boot": "#0B0C10",
    "wing": "#14131B",
    "wing2": "#1B1A24",
    "iris": "#B01F2B",
    "pupil": "#26080C",
    "lash": "#17171A",
    "eye_white": "#F7F4F0",
    "mouth": "#7A3A3E",
}
