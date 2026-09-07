#!/usr/bin/env python3
"""
PX4 SITL (gz_x500) offboard test via MAVSDK.
Route (NED, altitude 1.5m => z=-1.5):
  origin -> takeoff 1.5m -> north 2m -> east 1m (+yaw 90) -> origin -> land
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw
from mavsdk.telemetry import LandedState

ALT = -1.5  # NED z for 1.5m altitude
HOLD_SEC = 8


async def goto(drone, north, east, yaw, label):
    print(f"-- {label}")
    await drone.offboard.set_position_ned(PositionNedYaw(north, east, ALT, yaw))
    await asyncio.sleep(HOLD_SEC)


async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone connection...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected")
            break

    print("Waiting for global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    # Must stream setpoints BEFORE starting offboard, or PX4 rejects the mode switch.
    print("-- Priming setpoint stream")
    for _ in range(10):
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(0.1)

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Offboard start failed: {error._result.result}")
        await drone.action.disarm()
        return

    await goto(drone, 0.0, 0.0, 0.0, "Takeoff to 1.5m")
    await goto(drone, 2.0, 0.0, 0.0, "North 2m")
    await goto(drone, 2.0, 1.0, 90.0, "East 1m, yaw 90")
    await goto(drone, 0.0, 0.0, 0.0, "Return to origin")

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Offboard stop failed: {error._result.result}")

    print("-- Landing")
    await drone.action.land()

    async for state in drone.telemetry.landed_state():
        if state == LandedState.ON_GROUND:
            print("-- Landed")
            break

    print("-- Done")


if __name__ == "__main__":
    asyncio.run(run())
