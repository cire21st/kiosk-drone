#!/usr/bin/env python3
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyulog import ULog

if len(sys.argv) < 2:
    print('usage: plot_trajectory.py <path.ulg>')
    sys.exit(1)

ulog_path = sys.argv[1]
ulog = ULog(ulog_path, message_name_filter_list=['vehicle_local_position'])

datasets = {d.name: d for d in ulog.data_list}
if 'vehicle_local_position' not in datasets:
    print('vehicle_local_position not found in log')
    sys.exit(1)

d = datasets['vehicle_local_position']
data = d.data
t = data['timestamp'] / 1e6
t = t - t[0]
north = data['x']
east = data['y']
down = data['z']
alt = -down

# 2D trajectory plot
fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(east, north, '-', color='tab:blue', linewidth=1.5, label='trajectory')
ax.plot(east[0], north[0], 'o', color='tab:green', markersize=10, label='start', zorder=5)
ax.plot(east[-1], north[-1], 's', color='tab:red', markersize=10, label='end', zorder=5)
ax.set_xlabel('East (m)')
ax.set_ylabel('North (m)')
ax.set_title('X500 offboard square trajectory')
ax.set_aspect('equal', adjustable='box')
ax.grid(True, which='both')
ax.xaxis.set_major_locator(plt.MultipleLocator(1))
ax.yaxis.set_major_locator(plt.MultipleLocator(1))
ax.legend()
fig.tight_layout()
fig.savefig('/root/trajectory_2d_placeholder.png') if False else None
fig.savefig(sys.argv[2])
plt.close(fig)

# altitude vs time plot
fig2, ax2 = plt.subplots(figsize=(9, 4))
ax2.plot(t, alt, '-', color='tab:purple', linewidth=1.5)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Altitude (m)')
ax2.set_title('Altitude vs Time')
ax2.grid(True)
fig2.tight_layout()
fig2.savefig(sys.argv[3])
plt.close(fig2)

print('north range:', min(north), max(north))
print('east range:', min(east), max(east))
print('alt range:', min(alt), max(alt))
print('duration s:', t[-1])
