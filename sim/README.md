# 시뮬레이션

Gazebo 월드, 모델, 마커 생성.

## 알려진 함정

**1. 마커 크기 상수 일치**
`generate_marker.py`와 `vision/` 쪽 상수가 반드시 같아야 한다.
불일치해도 검출은 되고 거리만 틀린다. 조용히 실패하는 유형.

**2. yaw는 절대 방위각**
`PositionNedYaw`의 yaw는 상대 회전량이 아니다. 북쪽 = 0.

**3. `make` 쓰지 말 것**
```bash
# 나쁨 — ninja 컴파일 잡이 메모리를 순식간에 먹는다
make px4_sitl gz_x500_depth

# 좋음 — 빌드된 바이너리 직접 실행
PX4_GZ_WORLD=kiosk PX4_SIM_MODEL=gz_x500_depth ./build/px4_sitl_default/bin/px4
```

**4. 카메라 렌더링 메모리 누수**
WSL에서 GPU 가속 없이(llvmpipe) 카메라 센서를 돌리면 프레임 버퍼가 누적된다.
1920×1080/30Hz에서 초당 150MB. 640×480/5Hz로 낮춰 초당 4.5MB까지 완화함.
`OakD-Lite/model.sdf`에 반영되어 있다. 실기 D435i는 해당 없음.

**5. UV 매핑 방향**
gz-sim PBR albedo가 텍스처를 좌우 반전할 수 있다.
마커 ID 배치를 바꿨다면 첫 캡처에서 ID0이 실제로 좌상단인지 확인할 것.

## 현재 설정

- 벽: 1000×1000mm, 드론 기준 북쪽 3m, 높이 1.5m
- 마커: DICT_4X4_50, 150mm, 4개 (좌상=0, 우상=1, 우하=2, 좌하=3)
- 여백: 가장자리에서 50mm
