# 테스트 에셋 목록 (정답지)

규칙 위반 에셋을 의도적으로 심어두고, 검사 도구가 정확히 잡아내는지 측정하기 위한 목록입니다.
Starter Content나 에픽 무료 샘플 에셋을 복제한 뒤 이름과 설정만 바꾸면 대부분 금방 만들 수 있습니다.

## 폴더 구조

```
/Game/Characters/Hero/
/Game/Environment/Props/
/Game/Environment/Architecture/
/Game/VFX/
/Game/UI/
```

## A. 위반 에셋 (잡혀야 하는 것)

| # | 에셋 경로 | 만드는 방법 | 기대 규칙 |
|---|---|---|---|
| 1 | /Game/Environment/Props/Chair_01 | 스태틱 메시 복제 후 접두사 없이 이름 변경 | NAME-001 |
| 2 | /Game/Environment/Props/SM_Rock_Copy | 메시 복제 시 붙는 이름 그대로 두기 | NAME-002 |
| 3 | /Game/Environment/Architecture/T_Wall | 텍스처 복제 후 접미사 없이 이름 변경 | NAME-003 |
| 4 | /Game/Environment/Props/T_Crate_D | 1000x1000 이미지 임포트 | TEX-001 |
| 5 | /Game/Environment/Props/T_Barrel_D | 4096x4096 이미지 임포트 (Props 최대 1024) | TEX-002 |
| 6 | /Game/Environment/Architecture/T_Brick_N | 노멀맵인데 Compression을 Default로 변경 | TEX-003 |
| 7 | /Game/Environment/Architecture/T_Metal_ORM | sRGB 체크 켜기 | TEX-003 |
| 8 | /Game/Environment/Architecture/T_Floor_D | Mip Gen Settings를 NoMipmaps로 변경 | TEX-004 |
| 9 | /Game/Environment/Architecture/SM_Statue | 트라이앵글 5만 개 이상 메시, Nanite 끄기 | MESH-001 |
| 10 | /Game/Environment/Props/SM_Pillar | 트라이앵글 약 3천 개, Nanite 끄고 LOD 1개만 | MESH-002 |
| 11 | /Game/Environment/Props/SM_Cart | 머티리얼 슬롯 6개 | MESH-003 |
| 12 | /Game/Environment/Props/M_Heavy | 노이즈, 삼각함수 노드를 많이 연결해 인스트럭션 300 초과 | MAT-001 |
| 13 | /Game/Environment/Props/M_ManyTextures | 텍스처 샘플 노드 10개 연결 | MAT-002 |
| 14 | /Game/Environment/Architecture/M_Glass | Blend Mode를 Translucent로 설정 | MAT-003 |
| 15 | /Game/Environment/Props/SM_Table | 원본 머티리얼(M_Wood)을 직접 할당 | MAT-004 |
| 16 | /Game/Environment/Props/tree_final | 접두사 없음 + 금지 단어 + LOD 부족 (복합 위반) | NAME-001, NAME-002, MESH-002 |

## B. 정상 에셋 (잡히면 안 되는 것, 오탐 측정용)

| # | 에셋 경로 | 설정 | 확인 포인트 |
|---|---|---|---|
| 17 | /Game/Environment/Props/SM_Bench_01 | 규칙을 모두 지킨 정상 메시 | 아무 규칙도 걸리지 않아야 함 |
| 18 | /Game/UI/T_Icon_Sword_D | 300x300, 밉맵 없음 | UI 카테고리라 TEX-001, TEX-004 통과 |
| 19 | /Game/VFX/M_Smoke | Translucent | VFX 카테고리라 MAT-003 통과 |
| 20 | /Game/Characters/Hero/T_Hero_Armor_D | 4096x4096 | 예외 목록에 있으므로 TEX-002 통과 |
| 21 | /Game/Environment/Architecture/SM_Wall_Large | 트라이앵글 5만 개, Nanite 켜짐 | MESH-001, MESH-002 통과 |

## 측정 표 (3일차에 채우기)

| 항목 | 결과 |
|---|---|
| 심어둔 위반 수 | 18건 (복합 위반 포함) |
| 탐지한 위반 수 | |
| 놓친 위반 | |
| 오탐 (B 목록에서 걸린 것) | |
| 전체 검사 소요 시간 | |
| 변경 파일만 검사 시 소요 시간 | |
| 수동 검수 예상 시간 (에셋당 약 1분 가정) | |
| 에이전트 설명과 수정 제안 1회 토큰 비용 | |

## 구현 메모

- 테스트용 이미지(1000x1000, 4096x4096 등)는 Pillow로 단색이나 노이즈 이미지를 만드는 짧은 스크립트로 생성하면 빠릅니다.
- 머티리얼 인스트럭션 수와 샘플러 수는 에디터 Python의 머티리얼 통계 조회 기능(`unreal.MaterialEditingLibrary`)으로 가져올 수 있는지 먼저 확인하세요. 5.8에서 함수 이름이나 반환 필드가 다를 수 있으니 문서 기준으로 검증이 필요합니다.
- 예외 목록 판정은 에셋 경로와 규칙 ID가 둘 다 일치할 때만 적용하고, 만료일이 지난 예외는 무시하도록 구현하세요.
