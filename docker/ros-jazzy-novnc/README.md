# ROS 2 Jazzy noVNC Docker
based on https://github.com/cire21st/ros-jazzy-novnc-docker

Docker를 이용해 **ROS 2 Jazzy + Ubuntu 24.04 데스크톱 환경**을 별도의 ROS 2 설치 없이 실행할 수 있는 Docker 환경입니다.

웹 브라우저를 통해 Ubuntu 데스크톱에 접속할 수 있으며, Docker만 설치되어 있다면 Windows / macOS / Linux에서 사용할 수 있습니다.

> **사용자는 Docker만 설치하면 됩니다.**
> Dockerfile을 직접 빌드하거나 ROS 2를 별도로 설치할 필요가 없습니다.

---

## 🖥️ 제공 환경

* Ubuntu 24.04
* ROS 2 Jazzy
* noVNC 기반 웹 브라우저 원격 데스크톱
* ROS 2 개발 환경
* 터미널
* VSCodium
* Firefox
* `ROS_DOMAIN_ID=30`
* Linux AMD64 환경

Docker 이미지:

```text
eric321kr/ros-jazzy-full:latest
```

---

# 🚀 빠른 시작

## 1. Docker 설치

### Windows / macOS

[Docker Desktop](https://www.docker.com/products/docker-desktop/)을 설치합니다.

설치 후 Docker Desktop을 실행해 주세요.

```bash
docker --version
docker compose version
```

두 명령 모두 버전 정보가 출력되면 정상입니다.

---

## 2. 저장소 다운로드

터미널에서 다음 명령을 실행합니다.

```bash
git clone https://github.com/cire21st/kiosk-drone.git
cd docker\ros-jazzy-novnc
```

---

## 3. Docker 환경 실행

다음 명령 하나만 실행하면 됩니다.

```bash
docker compose up -d
```

처음 실행할 때는 Docker 이미지를 다운로드하기 때문에 시간이 조금 걸릴 수 있습니다.

이미지를 다운로드한 이후에는 빠르게 실행됩니다.

실행 상태를 확인하려면:

```bash
docker compose ps
```

다음과 같이 컨테이너가 `Up` 상태라면 정상적으로 실행된 것입니다.

```text
NAME               STATUS
ros-jazzy-novnc    Up
```

---

# 🌐 4. 웹 브라우저로 접속

컨테이너가 실행되면 웹 브라우저에서 다음 주소로 접속합니다.

```text
http://localhost:8080
```

Ubuntu 데스크톱 화면이 나타나면 정상적으로 실행된 것입니다.

별도의 VNC 프로그램이나 SSH 접속은 필요하지 않습니다.

---

# 📁 실습 파일 저장

저장소의 `workspace` 폴더는 Docker 컨테이너 내부의 Ubuntu 바탕화면과 연결됩니다.

```text
ros-jazzy-novnc-docker/
├── docker-compose.yaml
├── README.md
└── workspace/
```

컨테이너 내부:

```text
/home/ubuntu/Desktop
```

와 로컬 컴퓨터의:

```text
./workspace
```

가 연결되어 있습니다.

따라서:

```text
로컬 workspace
      ↕
컨테이너의 ~/Desktop
```

으로 파일이 동기화됩니다.

### 예시

Windows에서:

```text
workspace/test.py
```

를 만들면 Docker 내부 Ubuntu의 바탕화면에서도:

```text
~/Desktop/test.py
```

로 확인할 수 있습니다.

반대로 Docker 내부 바탕화면에서 만든 파일도 로컬 `workspace` 폴더에 저장됩니다.

> **실습 코드와 과제 파일은 반드시 ****`~/Desktop`**** 또는 그 하위 폴더에 저장하는 것을 권장합니다.**

컨테이너를 삭제하거나 다시 실행해도 `workspace`에 저장된 파일은 유지됩니다.

---

# 🐳 Docker 환경 종료

실행 중인 컨테이너를 종료하려면:

```bash
docker compose down
```

다시 실행하려면:

```bash
docker compose up -d
```

하면 됩니다.

---

# 🔄 자주 사용하는 명령어

### 실행

```bash
docker compose up -d
```

### 종료

```bash
docker compose down
```

### 실행 상태 확인

```bash
docker compose ps
```

### 실시간 로그 확인

```bash
docker compose logs -f
```

### 컨테이너 재시작

```bash
docker compose restart
```

---

# 🛠️ 문제 해결

## 1. `docker: command not found`

Docker가 설치되어 있지 않거나 PATH가 설정되지 않은 경우입니다.

Docker가 정상적으로 설치되어 있는지 확인하세요.

```bash
docker --version
```

Windows / macOS에서는 Docker Desktop이 실행 중인지 확인하세요.

---

## 2. `docker compose` 명령어가 실행되지 않는 경우

다음 명령어를 실행해 보세요.

```bash
docker compose version
```

버전 정보가 나오지 않는다면 Docker Desktop 또는 Docker Compose Plugin 설치 상태를 확인하세요.

---

## 3. `localhost`에 접속할 수 없는 경우

먼저 컨테이너가 실행 중인지 확인합니다.

```bash
docker compose ps
```

컨테이너가 실행되고 있지 않다면:

```bash
docker compose up -d
```

를 다시 실행합니다.

그래도 문제가 발생한다면 로그를 확인합니다.

```bash
docker compose logs
```

---

## 4. 8080 포트를 사용할 수 없다는 오류가 발생하는 경우

다른 프로그램이 이미 8080번 포트를 사용하고 있을 수 있습니다.

`docker-compose.yaml`의:

```yaml
ports:
  - "8080:80"
```

부분을 다음과 같이 변경할 수 있습니다.

```yaml
ports:
  - "XXXX:80"
```

그 후:

```bash
docker compose up -d
```

를 실행하고 웹 브라우저에서 다음 주소로 접속합니다.

```text
http://localhost:XXXX
```

---

# 🧹 Docker 환경을 완전히 삭제하고 싶은 경우

컨테이너를 종료하고 삭제합니다.

```bash
docker compose down
```

Docker 이미지까지 삭제하려면:

```bash
docker rmi eric321kr/ros-jazzy-full:latest
```

> `workspace` 폴더는 Docker 컨테이너와 별도로 로컬 컴퓨터에 존재하므로 이미지나 컨테이너를 삭제해도 파일이 삭제되지 않습니다.

---

## License

This project is provided for educational and development purposes.
