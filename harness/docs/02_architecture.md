# 아키텍처

## 전체 구조

```
[규칙 파일 asset_rules.yaml]
          │  (검사 기준, 위반 이유, 수정 방법)
          ▼
[1. Python 결정적 검사]  ── 에디터 Python / 커맨드렛
   네이밍, 텍스처, 메시, 머티리얼, (코드)
          │  JSON 리포트
          ▼
[2. 에이전트 레이어]  ── Claude Code + 공식 언리얼 MCP
   - asset-auditor: 검사 실행, 위반 이유 설명, 우선순위 정리 (읽기 전용)
   - asset-fixer: 수정안 작성 (dry-run 결과 제시)
          │
          ▼
[3. 사람 승인]  ── 훅으로 파괴적 작업 전 정지
          │
          ▼
[4. 제출 관문 /submit]
   변경 파일만 검사 → error 있으면 중단 → 통과 시 커밋 메시지 초안 → 확인 후 커밋
```

## 설계 원칙

1. **규칙은 한 곳에**: 검사 기준과 설명 근거 모두 `asset_rules.yaml` 에서 읽음
2. **판정은 코드, 설명은 LLM**: 위반 여부는 Python이 결정. LLM은 이유 설명, 우선순위, 수정 방법 안내만 담당
3. **사람이 최종 결정**: 수정과 커밋은 사람 승인 후 실행
4. **증분 우선**: 제출 시에는 변경된 에셋만 검사
5. **예외는 기록과 함께**: 예외마다 사유, 담당자, 만료일 필수. 무기한 예외 금지
6. **부서 확장 가능**: 같은 구조(규칙 파일 → 검사 → 설명 → 승인)로 코드, 기획, QA 모듈 추가

## 포트폴리오 저장소 폴더 구성 (제안)

```
ta-asset-guard/
├─ README.md                  # 아키텍처 그림, 설치, 데모, 측정 결과, 로드맵
├─ CLAUDE.md                  # 에이전트용 스튜디오 규칙
├─ rules/
│  └─ asset_rules.yaml
├─ checks/                    # Python 검사 모듈
│  ├─ rule_loader.py          # YAML 로드, 카테고리 판별, 예외 적용
│  ├─ naming.py
│  ├─ texture.py
│  ├─ mesh.py
│  ├─ material.py
│  ├─ code_uproperty.py       # (여유 시)
│  └─ report.py               # JSON 리포트 생성
├─ scripts/
│  ├─ run_audit.py            # 전체 또는 지정 경로 검사 진입점
│  └─ changed_assets.py       # Git 변경 파일 → 에셋 경로 변환
├─ toolsets/                  # 공식 언리얼 MCP 커스텀 툴세트 등록
├─ .claude/
│  ├─ agents/
│  │  ├─ asset-auditor.md
│  │  └─ asset-fixer.md
│  ├─ commands/
│  │  ├─ audit.md
│  │  └─ submit.md
│  └─ settings.json           # 훅 설정
├─ tests/
│  └─ expected_violations.json   # test_assets_plan.md 정답지를 JSON으로
└─ docs/
   └─ demo.gif / 측정 결과
```

## JSON 리포트 형식 (제안)

```json
{
  "run_id": "2026-09-28T10:00:00",
  "scope": "changed | full | path",
  "summary": { "checked": 21, "errors": 14, "warnings": 5, "exempted": 1, "duration_sec": 3.2 },
  "violations": [
    {
      "asset": "/Game/Environment/Props/T_Barrel_D",
      "class": "Texture2D",
      "category": "props",
      "rule_id": "TEX-002",
      "severity": "error",
      "actual": 4096,
      "expected": "<= 1024",
      "title": "카테고리 최대 해상도 초과"
    }
  ],
  "exempted": [
    { "asset": "/Game/Characters/Hero/T_Hero_Armor_D", "rule_id": "TEX-002", "reason": "...", "expires": "2026-12-31" }
  ]
}
```

`why`, `fix` 는 리포트에 넣지 않고 에이전트가 규칙 ID로 YAML에서 찾아 설명한다. (리포트를 가볍게 유지, 토큰 절약)
