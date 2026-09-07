# 드론 시뮬레이션 개발환경 구축 기록

환경: WSL2 Ubuntu 24.04 (WSLg), ROS2 Jazzy, PX4-Autopilot main (v1.18.0-beta1 기준),
기체 Holybro X500 v2 → 시뮬 모델 `gz_x500`.

## 1. ROS2 Jazzy
24.04에서는 Humble이 지원되지 않아 Jazzy 설치. `/opt/ros/jazzy/setup.bash` 소싱.

## 2. PX4-Autopilot
`~/PX4-Autopilot` 클론, `make px4_sitl gz_x500` 빌드 완료.
Gazebo(gz sim 8.14.0)에 x500 스폰 확인.

**주의(중요): 백그라운드 실행 시 pty 필요**
`make px4_sitl gz_x500`를 stdin이 `/dev/null`인 상태로 백그라운드 실행하면
PX4 쉘(pxh>)이 tty 부재를 감지하지 못하고 프롬프트를 무한 재출력하며
로그가 수 GB로 폭주하는 문제가 있었다 (실측: 20초 만에 600MB+).
`script` 명령으로 pty를 붙여서 우회함:

```bash
cd ~/PX4-Autopilot
setsid bash -c "HEADLESS=1 script -qec 'make px4_sitl gz_x500' ~/kiosk_drone_ws/logs/px4_sitl.log" \
  < /dev/null > /dev/null 2>&1 &
disown
```

## 3. Micro XRCE-DDS Agent
`/usr/local/bin/MicroXRCEAgent` 설치 완료.
v2.4.2는 GCC13 환경에서 Fast-DDS 2.12.2의 `<cstdint>` 누락으로 빌드 실패 →
**master(v3.0.1)** 로 빌드하여 해결. (v2.4.2 재시도 금지)

실행:
```bash
setsid bash -c 'MicroXRCEAgent udp4 -p 8888 > ~/kiosk_drone_ws/logs/agent.log 2>&1' \
  < /dev/null > /dev/null 2>&1 &
disown
```

## 4. ROS2 워크스페이스 (px4_msgs / px4_ros_com)

**브랜치 선택 근거**: PX4가 `main` (v1.18.0-beta1 기준) 이므로, uORB 메시지
필드 레이아웃이 XRCE-DDS로 그대로 브리지되는 `px4_msgs`는 PX4 버전과
필드 단위로 맞아야 함. 태그가 정확히 일치하는 브랜치가 없어 가장 근접한
**`release/1.18`** 을 사용. `px4_ros_com`은 메시지 정의에 의존하지 않는
브리지/example 코드라 버전 민감도가 낮아 **`main`** 사용.

```bash
mkdir -p ~/kiosk_drone_ws/src && cd ~/kiosk_drone_ws/src
git clone https://github.com/PX4/px4_msgs.git -b release/1.18
git clone https://github.com/PX4/px4_ros_com.git   # main

cd ~/kiosk_drone_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
```
결과: `px4_msgs` 2min40s, `px4_ros_com` 9.7s — 둘 다 성공.

## 5. 검증 (진짜 성공 판정)
PX4 SITL + Micro XRCE-DDS Agent를 띄운 상태에서:
```bash
source /opt/ros/jazzy/setup.bash
source ~/kiosk_drone_ws/install/setup.bash
ros2 topic list | grep fmu
```
`/fmu/out/vehicle_local_position_v1`, `/fmu/out/vehicle_status_v4`,
`/fmu/out/vehicle_attitude` 등 확인됨 → **성공**.

## 6. Python 환경
24.04는 PEP 668(externally-managed-environment)로 시스템 pip가 막혀 있음.
`test_offboard.py`는 mavsdk만 사용하고 rclpy(ROS2)는 필요 없으므로,
시스템 파이썬(ROS2 apt 패키지들이 의존)을 건드리지 않는 **venv**를 선택
(`--break-system-packages`는 지양).

```bash
sudo apt-get install -y python3-venv python3-full   # 최초 1회, 미설치 상태였음
python3 -m venv ~/kiosk_drone_ws/venv
source ~/kiosk_drone_ws/venv/bin/activate
pip install mavsdk opencv-contrib-python numpy
```
설치 확인: mavsdk OK, opencv-contrib-python 5.0.0, numpy 2.5.2.

## 7. test_offboard.py
`~/kiosk_drone_ws/test_offboard.py` — MAVSDK 비동기 API.

- `udp://:14540` 연결 (PX4 SITL 기본 MAVSDK 포트)
- offboard 진입 전 `set_position_ned`를 10회(0.1s 간격) 먼저 스트리밍
  → 안 하면 `Offboard::Start()`가 REJECTED됨 (PX4가 최근 setpoint 없으면 거부)
- NED 좌표계이므로 고도 1.5m = `z = -1.5`
- 경로: 이륙(1.5m) → 북 2m → 동 1m + yaw 90° → 원점 복귀 → 착륙

실행 (SITL + Agent가 떠 있는 상태에서):
```bash
source ~/kiosk_drone_ws/venv/bin/activate
python3 ~/kiosk_drone_ws/test_offboard.py
```
2026-08-15 실측 로그: Connected → Armed → Offboard 진입(에러 없음) →
Takeoff → North 2m → East 1m+yaw90 → Return → Landed → Done. **전 구간 성공.**

참고: mavsdk가 `udp://` 문법이 deprecated라는 경고를 출력함(`udpin://`/`udpout://`
권장). 동작에는 문제 없으나 추후 문법을 갱신할 것.

## 8. 실행 순서 요약 (매번 반복 시)
```bash
# 1) PX4 SITL
cd ~/PX4-Autopilot
setsid bash -c "HEADLESS=1 script -qec 'make px4_sitl gz_x500' ~/kiosk_drone_ws/logs/px4_sitl.log" \
  < /dev/null > /dev/null 2>&1 & disown

# 2) Micro XRCE-DDS Agent
setsid bash -c 'MicroXRCEAgent udp4 -p 8888 > ~/kiosk_drone_ws/logs/agent.log 2>&1' \
  < /dev/null > /dev/null 2>&1 & disown

# 3) (선택) ROS2 토픽 확인
source /opt/ros/jazzy/setup.bash
source ~/kiosk_drone_ws/install/setup.bash
ros2 topic list | grep fmu

# 4) offboard 테스트
source ~/kiosk_drone_ws/venv/bin/activate
python3 ~/kiosk_drone_ws/test_offboard.py
```

## 9. 뒷정리
설정 중 임시로 걸어둔 NOPASSWD sudoers를 제거할 것:
```bash
sudo rm /etc/sudoers.d/90-temp-nopasswd
```
