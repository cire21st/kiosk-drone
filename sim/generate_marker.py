#!/usr/bin/env python3
"""Generate a kiosk wall texture: 1m x 1m panel with four 150mm DICT_4X4_50
ArUco markers, one in each corner, 50mm inset from the panel edge.

ID layout (as authored in the PNG, viewer facing the wall):
    0 --- 1
    |     |
    3 --- 2

Object points for solvePnP
---------------------------
Wall-local frame: origin at panel center, X to the right / Z up, as seen by
a camera facing the wall (this matches the drone's approach in
fly_to_marker_and_capture.py: it moves north toward the wall and should see
image-left -> wall -X, image-right -> wall +X). This mapping depends on how
gz-sim/Ogre applies the box's PBR albedo UVs and has NOT been visually
verified yet -- confirm against the first captured RGB frame (ID0 should
appear top-left in-frame) before trusting signs below. Getting this backwards
is a silent mirroring bug, the geometric analog of the +34% distance bias
we hit from the wrong 85mm marker-size assumption.

Marker center = MARGIN_MM + MARKER_MM/2 = 50 + 75 = 125mm in from each edge.
Panel half-size = 500mm, so center offset from panel center = 500-125 = 375mm.

MARKER_CENTERS_MM = {
    0: (-375, 375),   # top-left      (wall_x_mm, wall_z_mm), wall_y=0 (marker plane)
    1: (375, 375),    # top-right
    2: (375, -375),   # bottom-right
    3: (-375, -375),  # bottom-left
}
Per-corner object points for marker `i` (axis-aligned, no in-plane rotation):
    top-left     = (cx - MARKER_MM/2, cy + MARKER_MM/2, 0)
    top-right    = (cx + MARKER_MM/2, cy + MARKER_MM/2, 0)
    bottom-right = (cx + MARKER_MM/2, cy - MARKER_MM/2, 0)
    bottom-left  = (cx - MARKER_MM/2, cy - MARKER_MM/2, 0)
"""

import cv2
import numpy as np

PANEL_M = 1.0
MARKER_MM = 150
MARGIN_MM = 50  # inset from panel edge to marker edge
PX_PER_MM = 2  # 2000x2000 canvas for a 1m panel

CORNER_IDS = {
    "top_left": 0,
    "top_right": 1,
    "bottom_right": 2,
    "bottom_left": 3,
}

canvas_px = int(PANEL_M * 1000 * PX_PER_MM)
marker_px = MARKER_MM * PX_PER_MM
margin_px = MARGIN_MM * PX_PER_MM

dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

canvas = np.full((canvas_px, canvas_px), 255, dtype=np.uint8)

# (row_off, col_off) of each marker's top-left pixel in the canvas
placements = {
    "top_left": (margin_px, margin_px),
    "top_right": (margin_px, canvas_px - margin_px - marker_px),
    "bottom_right": (canvas_px - margin_px - marker_px, canvas_px - margin_px - marker_px),
    "bottom_left": (canvas_px - margin_px - marker_px, margin_px),
}

for name, marker_id in CORNER_IDS.items():
    marker = cv2.aruco.generateImageMarker(dictionary, marker_id, marker_px)
    row_off, col_off = placements[name]
    canvas[row_off:row_off + marker_px, col_off:col_off + marker_px] = marker

out = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
out_path = "/home/joheeho/PX4-Autopilot/Tools/simulation/gz/models/kiosk_wall/kiosk_wall_marker.png"
cv2.imwrite(out_path, out)
print(f"saved {out_path} ({canvas_px}x{canvas_px}px, {len(CORNER_IDS)} markers "
      f"{marker_px}x{marker_px}px = {MARKER_MM}mm @ {PX_PER_MM}px/mm, margin {MARGIN_MM}mm)")
for name, marker_id in CORNER_IDS.items():
    print(f"  id={marker_id} ({name}) top-left px={placements[name]}")
