# 알아야 할 지식

면접 대비 겸 작업 중 참고용. 이번 3일 작업에 바로 필요한 것은 ★ 표시.

## LLM API 기본
- ★ 시스템 프롬프트, 메시지 구조, temperature
- ★ 구조화된 출력(JSON 스키마), 함수 호출(Tool use)
- 토큰 비용 계산, 프롬프트 캐싱, 스트리밍

## 에이전트 설계
- ★ 에이전트 루프 (모델이 도구 호출 → 결과 → 다시 판단)
- ★ 좋은 도구 설계: 이름, 설명, 입력 스키마를 모델이 이해하기 쉽게
- 워크플로우(정해진 순서) vs 에이전트(모델이 판단), 언제 무엇을 쓸지
- 서브에이전트, 오케스트레이션, 컨텍스트 관리
- ★ "규칙으로 되는 건 규칙으로, 애매한 것만 LLM으로"

## MCP
- ★ 호스트, 클라이언트, 서버 구조
- Tools, Resources, Prompts 차이
- 전송 방식: stdio, Streamable HTTP
- Python SDK(FastMCP), TypeScript SDK

## Claude Code / Codex / Cursor 활용
- ★ CLAUDE.md, 서브에이전트, 스킬, 훅, 슬래시 커맨드, 권한 설정
- 플러그인, 헤드리스 실행으로 스크립트나 CI에 붙이기
- Cursor Rules, Codex AGENTS.md 비교

## 평가(Eval)
- ★ 테스트 세트(정답지) 만들기, 정확도, 오탐, 회귀 측정
- LLM-as-judge
- 환각 탐지와 대응

## HuggingFace
- transformers pipeline 추론
- LoRA(PEFT) 파인튜닝 개념
- 양자화, 로컬 추론(Ollama, vLLM)

## RAG 기초
- 임베딩, 벡터 검색, 청킹
- "학습"(파인튜닝)과 "검색해서 끼워 넣기"(RAG) 용어 구분

## 언리얼 자동화
- ★ 에디터 Python 스크립팅 (`unreal` 모듈, EditorAssetLibrary, AssetRegistry)
- ★ 텍스처, 스태틱 메시, 머티리얼 속성 조회
- Remote Control API
- Editor Utility Widget, Data Validation 플러그인
- 커맨드렛, 빌드 자동화, Gauntlet(자동화 테스트), Horde(빌드 인프라)

## 렌더링과 최적화
- 텍스처 스트리밍, 밉맵, 압축 방식(BC1, BC5, BC7 등), sRGB
- Nanite, LOD, 드로우콜, 머티리얼 슬롯
- 셰이더 인스트럭션, 샘플러, 셰이더 퍼뮤테이션, static switch
- 반투명과 오버드로우
- stat unit, stat gpu, Unreal Insights, CSV 프로파일러

## Python 툴링 실무
- 가상환경, uv, 타입 힌트, pydantic
- asyncio, HTTP 클라이언트
- CLI 도구 배포

## 보안
- API 키 관리
- 프롬프트 인젝션
- 에이전트 권한 범위 설계 (읽기 전용 에이전트, 승인 필요 작업)
