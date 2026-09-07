# 협업 방법

복잡한 규칙 없음. **포크 → 브랜치 → PR** 세 단계가 전부다.

작게 자주 올릴 것. 완성 안 됐어도 Draft PR로 올려서 방향을 확인받는 게 나중에 통째로 갈아엎는 것보다 낫다.

---

## 처음 한 번만

### 1. 포크
이 저장소 우측 상단 **Fork** 클릭.

### 2. 클론
```bash
git clone https://github.com/<본인계정>/kiosk-drone.git
cd kiosk-drone
```

### 3. 원본 저장소 연결
```bash
git remote add upstream https://github.com/joheeho/kiosk-drone.git
git remote -v
```

`origin`(내 포크)과 `upstream`(원본) 두 개가 보이면 됨.

---

## 작업할 때마다

### 1. 최신 상태로 맞추기
```bash
git checkout main
git pull upstream main
```

작업 시작 전 항상. 안 하면 나중에 충돌난다.

### 2. 브랜치 만들기
```bash
git checkout -b vision/aruco-pnp
```

브랜치 이름은 `영역/작업내용`:

| 예시 | 설명 |
|---|---|
| `vision/aruco-pnp` | 위치 계산부 |
| `vision/mono-multiview` | 단안 다중뷰 |
| `control/approach-loop` | 제어부 |
| `agent/rule-based` | 판단부 (규칙) |
| `agent/llm-path-planning` | 판단부 (LLM) |
| `screen/paddle-ocr` | 화면 이해부 |
| `sim/marker-4corner` | 시뮬 환경 |
| `docs/error-measurement` | 문서·측정 기록 |

### 3. 커밋
```bash
git add .
git commit -m "ArUco 4점 통합 PnP 구현"
```

한국어로 편하게. **무엇을 했는지**만 알 수 있으면 된다.

### 4. 푸시
```bash
git push origin vision/aruco-pnp
```

### 5. PR 올리기

GitHub 가면 노란 배너에 **Compare & pull request** 버튼이 떠 있다. 클릭하고 템플릿 채워서 제출.

라벨을 붙일 것:
- 주제: `topic-llm-planning` 또는 `topic-mono-vision`
- 트랙: `track-A` ~ `track-E`

---

## PR 규칙

**작게.** 파일 10개씩 바꾸지 말고 하나씩 나눠서. 리뷰가 빨라지고 문제 생겼을 때 되돌리기 쉽다.

**Draft 적극 활용.** 진행 중이면 Draft PR. "이 방향 맞나요?" 물어보기 좋다.

**팀장 리뷰 후 머지.** 승인되면 Squash merge.

**충돌나면** 당황 말고 물어볼 것. 혼자 해결하려다 꼬이는 경우가 더 많다.

---

## 커밋하면 안 되는 것

- 가상환경 (`venv/`)
- 빌드 산출물 (`build/`, `*.pyc`)
- 대용량 로그 (`*.ulg`, `logs/`)
- API 키, 비밀번호 → `.env`에 두고 커밋 금지
- 큰 이미지·영상 → 노션이나 드라이브에

실수로 올렸으면 바로 말할 것. 히스토리에서 지워야 한다.

---

## 자주 쓰는 명령

```bash
git branch                      # 내 브랜치 목록
git status                      # 현재 상태
git log --oneline -10           # 최근 커밋
git checkout -- <파일>           # 변경 취소 (커밋 전)
git branch -d vision/aruco-pnp  # 브랜치 삭제 (머지 후)
```

---

## 막히면

- Git 문제 → 팀 단톡방에 스크린샷
- 코드 문제 → Issue 등록
- 방향 문제 → Draft PR 올리고 코멘트로 질문

혼자 오래 붙잡지 말 것. 30분 넘어가면 물어보는 게 빠르다.
