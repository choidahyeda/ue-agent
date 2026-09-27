# UE 5.8 언리얼 MCP 조사 노트

## 알려진 사실 (2026-09-27 조사)

- UE 5.8부터 에디터 프로세스 안에 MCP 서버를 내장하는 **언리얼 MCP** 플러그인 제공 (실험 기능)
- Claude Code, Cursor, MCP Inspector 등 MCP 호환 클라이언트가 로컬 HTTP로 에디터를 제어
- 실제 툴은 언리얼 MCP 자체가 아니라 **All Toolsets** 플러그인으로 활성화
- **Toolset Registry** 를 통해 팀이 Python, C++ 툴을 직접 추가 가능
- 설정: Edit > Plugins 에서 Unreal MCP, All Toolsets 활성화 → Editor Preferences > General > Model Context Protocol 에서 Auto Start Server → 에디터 재시작 (또는 콘솔 `ModelContextProtocol.StartServer`)
- 클라이언트 설정 예: `"serverUrl": "http://127.0.0.1:[PORT]/mcp"`
- 에픽이 강조하는 방향: 개발자가 판단, LLM은 조작 담당
- 별도로 AI Assistant 플러그인(언리얼 특화 질의응답)도 있음
- 커뮤니티 확장: ue-mcp(공식 툴세트 래핑), dcc-mcp-unreal(여러 DCC 공통 게이트웨이) 등

## 이번 프로젝트에서의 위치

- 공식 MCP = 에디터 연결 통로와 범용 툴
- 이 킷 = 스튜디오 규칙을 반영한 **커스텀 툴세트 + 워크플로우 + 안전장치**
- 범용 플러그인이 해줄 수 없는 부분(팀 규칙, 예산, 승인 절차)에 집중

## 직접 써보고 채울 것 (D1-2)

- 연결 방법과 걸린 시간:
- 기본 툴로 되는 것:
- 기본 툴로 안 되는 것:
- 큰 결과(스크린샷 등) 반환 시 문제:
- 실험 기능이라 불안정했던 점:
- 커스텀 툴 등록 방법과 소요 시간:

## 참고 링크

- 언리얼 에디터의 언리얼 MCP (Epic 5.8 문서): https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=ko
- Unreal MCP Plugin (UE 5.8) 설정과 한계 (Ludus AI): https://ludusengine.com/blog/unreal-mcp-plugin-ue5-8-setup
- dcc-mcp-unreal (PyPI): https://pypi.org/project/dcc-mcp-unreal/
- UE5.8 MCP 활용 게임 개발기 (게임뷰): https://www.gamevu.co.kr/news/articleView.html?idxno=60827
