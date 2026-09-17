# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Claude Code Game Studios

49개의 Claude Code 서브에이전트가 협업하여 인디 게임 개발을 진행합니다.
각 에이전트는 고유한 도메인을 소유하며, 관심사 분리와 품질을 강제합니다.

## 두 가지 모드 — 지금 어느 쪽인지 먼저 확인할 것

이 저장소는 **템플릿 원본**이자 그 템플릿으로 만드는 **게임 프로젝트**이기도 합니다.
작업을 시작하기 전에 반드시 확인하세요.

| 신호 | 의미 |
|------|------|
| `src/`에 `.gitkeep` + `CLAUDE.md`만 있고, 엔진이 `[TO BE CONFIGURED]`이며, `CCGS Skill Testing Framework/`가 존재 | **프레임워크 모드** — 템플릿 자체를 유지보수하는 중. 아래 *프레임워크 아키텍처*를 읽을 것. |
| `src/`에 실제 게임 코드가 있고 *기술 스택*에 엔진이 지정되어 있음 | **게임 모드** — 게임을 만드는 중. 아래 템플릿 섹션이 규칙이 됨. |

프레임워크 모드에서 "코드베이스"란 게임 소스가 아니라 에이전트/스킬/훅/규칙/템플릿
집합을 의미합니다. 이곳의 변경은 이 템플릿을 사용하는 모든 하위 프로젝트로 전파되므로,
스킬과 에이전트 파일을 프로덕션 코드로 취급하십시오.

---

# 프레임워크 아키텍처

## 구성 요소 배치와 파일 계약

| 구성 요소 | 위치 | 계약 |
|-----------|------|------|
| 에이전트 (49) | `.claude/agents/<name>.md` | 프론트매터: `name`, `description`, `tools`, `model`, `maxTurns`. 본문은 시스템 프롬프트이며 협업 프로토콜을 반드시 포함. |
| 스킬 (72) | `.claude/skills/<name>/SKILL.md` | 프론트매터: `name`, `description`, `argument-hint`, `user-invocable`, `allowed-tools`, 선택적 `model`. 스킬당 디렉터리 1개. |
| 훅 (12) | `.claude/hooks/*.sh` | Bash. `.claude/settings.json`에 timeout과 함께 등록. |
| 규칙 (11) | `.claude/rules/*.md` | 프론트매터 `paths:` glob 목록. 본문은 해당 경로에 강제되는 표준. |
| 템플릿 (38) | `.claude/docs/templates/` | 스킬이 실체화하는 문서 양식. |
| 파이프라인 정의 | `.claude/docs/workflow-catalog.yaml` | 단계/스텝 그래프의 유일한 기준. `/help`와 `/gate-check`가 읽음. |
| 게이트 프롬프트 | `.claude/docs/director-gates.md` | 모든 디렉터 리뷰 프롬프트의 단일 출처. 스킬은 게이트 ID를 참조할 뿐, 프롬프트를 인라인으로 복사하지 않음. |
| 테스트 스펙 | `CCGS Skill Testing Framework/` | 행위 스펙 + `catalog.yaml`. 독립적이며 삭제 가능 — `.claude/` 어디서도 이 폴더를 import하지 않음. |

## 7단계 파이프라인

`concept → systems-design → technical-setup → pre-production → production → polish → release`

`.claude/docs/workflow-catalog.yaml`에 정의되어 있으며, 각 스텝은 `command`,
`required` 플래그, 완료 판정에 쓰이는 `artifact` 검사(glob + 선택적 내용 패턴)를
가집니다. **단계 산출물을 만드는 새 스킬은 반드시 이 파일에 등록해야 합니다.**
등록하지 않으면 `/help`와 `/gate-check`가 그 스킬을 인식하지 못합니다.
게이트 판정은 권고(advisory)이며, 다음 단계로 넘어갈지는 언제나 사용자가 결정합니다.

## 스토리 루프

프로덕션 작업은 고정된 스킬 체인을 따릅니다.

```
/qa-plan sprint → /story-readiness → /dev-story → /code-review → /story-done
                                                              → /team-qa (스프린트 종료 시)
```

스토리 파일에는 TR-ID, 담당 ADR 경로, control manifest 버전이 내장됩니다.
`/dev-story`는 TR 레지스트리나 담당 ADR이 없으면 즉시 중단하며, ADR 상태가
아직 `Proposed`이면 해당 스토리를 블록합니다.

## 레지스트리는 추가 전용(append-only) 단일 출처

세 개의 YAML 레지스트리 덕분에 스킬들이 모든 문서를 다시 읽지 않고 grep만으로
충돌을 감지합니다. 각 파일 헤더 주석에 어떤 스킬이 읽고 쓰는지 명시되어 있으니
그 선언을 지키십시오.

| 레지스트리 | 소유 대상 | 절대 규칙 |
|-----------|----------|----------|
| `design/registry/entities.yaml` | GDD 간 공유되는 게임 사실(엔티티, 아이템, 공식, 상수) | 삭제 금지 — `status: deprecated`로 표시. 시스템 경계를 넘는 사실만 등록. |
| `docs/architecture/tr-registry.yaml` | 기술 요구사항 ID (`TR-<system>-NNN`) | ID는 영구적. **재번호 부여 금지** — 스토리가 이 ID를 참조함. 시스템별 목록 끝에만 추가. |
| `docs/registry/architecture.yaml` | 시스템을 가로지르는 아키텍처 입장(상태 소유권, 시그널 계약, 예산, 금지 패턴) | 삭제 금지 — `superseded_by: ADR-NNNN`으로 표시. |

들여쓰기가 중요합니다. 스킬들이 앵커 패턴으로 이 파일들을 grep합니다.

## 리뷰 모드

디렉터 게이트는 `production/review-mode.txt`(`full` | `lean` | `solo`, 기본값
`lean`)로 제어되며, 실행 단위로 `--review <mode>` 인자로 덮어쓸 수 있습니다.
게이트를 띄우는 모든 스킬은 디렉터를 spawn하기 전에 `director-gates.md`의 확인
패턴을 적용해야 합니다. 조건 없이 spawn하는 스킬은 `solo` 모드를 망가뜨립니다.

## 계층화된 지침

지침은 의도적으로 네 계층으로 나뉘어 있습니다. 새 규칙은 적용 범위가 가장 좁은
계층에 넣으십시오.

1. 이 파일 — 프로젝트 전역, 항상 로드됨 (작게 유지하고 `@` import를 활용할 것)
2. `src/CLAUDE.md`, `design/CLAUDE.md`, `docs/CLAUDE.md` — 디렉터리 범위, 해당 위치 작업 시 로드
3. `.claude/rules/*.md` — 경로 glob 범위의 코딩 표준
4. 스킬 및 에이전트 본문 — 작업 범위

## 검증 명령

이 저장소에는 빌드, 린트, CI 파이프라인이 없습니다. 검증은 Claude Code 세션
안에서 실행하는 스킬 프레임워크 자체입니다.

```
/skill-test static all          # 모든 SKILL.md 구조 린트 (7가지 검사)
/skill-test static <name>       # 스킬 하나만 린트
/skill-test spec <name>         # 스펙 파일 기준 행위 검증
/skill-test category <name|all> # quality-rubric.md의 카테고리 루브릭 적용
/skill-test audit               # 커버리지 리포트: 스펙 존재 여부, 마지막 테스트 일자
/skill-improve <name>           # 테스트 → 진단 → 수정 → 재테스트 → 유지 또는 되돌리기
```

`catalog.yaml`이 기준 색인입니다. 스킬의 `spec:`과 `category:`는 경로를
추측하지 말고 이 파일에서 읽으십시오. 스펙은 *이상적인* 동작이 아니라 *현재*
동작을 기술합니다. 어서션 실패는 "확실히 틀렸다"가 아니라 "조사가 필요하다"는
뜻이며, 스킬이 실제로 잘못된 경우에는 스킬을 먼저 고치고 그다음 스펙을 맞추십시오.

`validate-skill-change.sh` 훅이 `.claude/skills/` 하위를 편집할 때마다
`/skill-test` 실행을 권고합니다.

## 훅 작성 규약

- POSIX 호환만 사용 (`grep -E`, `grep -P` 금지) — Windows Git Bash, macOS, Linux에서 검증됨
- 선택적 도구(`jq`, Python 3)가 없어도 정상 종료할 것. 세션을 절대 중단시키지 말 것
- 넓은 matcher를 쓰는 훅은 모든 Bash/Write 호출에서 실행되므로, 관련 없는 명령이나 경로면 즉시 `exit 0`
- 새 훅은 `.claude/settings.json`에 timeout과 함께 등록하고 README 훅 표에도 문서화

## OpenCode 어댑터

이 저장소는 Claude Code 외에 [opencode](https://opencode.ai)에서도 동작합니다.
`.claude/`가 유일한 진실 공급원이고, `.opencode/`는 거기서 **생성**됩니다.

```bash
python3 tools/opencode/generate-adapter.py          # 재생성
python3 tools/opencode/generate-adapter.py --check  # 드리프트 검사
```

- `.opencode/agents/`, `.opencode/commands/`, `.opencode/ccgs-manifest.json` 은 생성물입니다.
  **직접 편집 금지** — 다음 재생성 때 덮어써집니다. 에이전트·스킬·규칙을 고쳤으면
  재생성하고 **opencode를 재시작**하십시오(설정을 핫 리로드하지 않습니다).
- 훅 12개는 `.opencode/plugins/ccgs-hooks.ts` 가 **기존 bash 스크립트를 그대로 호출**합니다.
  훅 로직은 `.claude/hooks/` 에만 존재합니다. 같은 플러그인이 opencode에 없는
  `maxTurns`·경로 스코프 규칙·`.env` 읽기 차단을 재구현합니다.
- 에이전트별 모델(GPT 혼용 포함)은 `tools/opencode/model-map.json` 에서 지정합니다.
  `opencode models` 목록보다 실제 로그인이 허용하는 모델이 적으니, 바꾸기 전에
  `opencode run "Reply OK" --model <id>` 로 탐침하십시오.
- 웹 검색은 Tavily 호스팅 MCP가 담당합니다. 셸 환경변수 `TAVILY_API_KEY` 가 필요하며,
  `opencode.json` 에는 `{env:TAVILY_API_KEY}` 참조만 들어갑니다. **키를 파일에 쓰지 마십시오.**
- opencode는 `CLAUDE.md` 와 `.claude/skills/` 를 직접 읽습니다. **`AGENTS.md`를 만들지
  마십시오** — `CLAUDE.md`를 가려서 진실 공급원이 둘로 갈라집니다.
- 플러그인 모듈의 **모든 export가 플러그인으로 호출**됩니다. 헬퍼 함수를 export하면
  로드가 조용히 실패합니다.

실측 검증 결과, 훅별 매핑, 조용히 실패하는 함정 목록, 아직 열린 갭(스킬별 모델
티어, websearch, statusline)은 `tools/opencode/README.md` 에 있습니다.

## 개수 동기화

에이전트/스킬/훅/규칙/템플릿 개수는 README 배지와 본문, 이 파일,
`CCGS Skill Testing Framework/CLAUDE.md`에 각각 적혀 있습니다. 구성 요소를
추가하거나 제거하면 이 모두를 함께 갱신해야 하며, `catalog.yaml`(새 스킬·에이전트는
스펙 항목 필요)과 `workflow-catalog.yaml`(단계 산출물을 만드는 스킬인 경우)도
갱신해야 합니다. 마지막으로 `generate-adapter.py` 를 재실행해 `.opencode/` 를
맞추십시오.

---

# 게임 프로젝트 설정

## 기술 스택

- **Engine**: [CHOOSE: Godot 4 / Unity / Unreal Engine 5]
- **Language**: [CHOOSE: GDScript / C# / C++ / Blueprint]
- **Version Control**: Git, trunk-based development
- **Build System**: [SPECIFY after choosing engine]
- **Asset Pipeline**: [SPECIFY after choosing engine]

> Godot, Unity, Unreal 각각에 대한 엔진 전문 에이전트와 하위 전문가 세트가
> 준비되어 있습니다. 프로젝트 엔진에 맞는 세트를 사용하십시오. `/setup-engine`이
> 여기에 엔진을 고정하고 아래 버전 import 경로를 함께 바꿔 줍니다.

## 프로젝트 구조

@.claude/docs/directory-structure.md

## 엔진 버전 레퍼런스

@docs/engine-reference/godot/VERSION.md

> 템플릿 기본값입니다. `/setup-engine`이 이 import를 선택한 엔진으로 다시
> 지정합니다. 고정된 엔진 버전은 모델 학습 데이터보다 최신이므로, 엔진 API
> 시그니처를 추측하지 말고 항상 `docs/engine-reference/`에서 먼저 확인하십시오.

## 기술 선호 설정

@.claude/docs/technical-preferences.md

## 조정 규칙

@.claude/docs/coordination-rules.md

## 협업 프로토콜

**자율 실행이 아니라 사용자 주도 협업입니다.**
모든 작업은 **질문 -> 선택지 -> 결정 -> 초안 -> 승인** 순서를 따릅니다.

- 에이전트는 Write/Edit 도구를 쓰기 전에 반드시 "[filepath]에 작성해도 될까요?"라고 물어야 합니다
- 에이전트는 승인을 요청하기 전에 초안이나 요약을 보여 주어야 합니다
- 여러 파일을 변경할 때는 전체 변경 묶음에 대한 명시적 승인이 필요합니다
- 사용자의 지시 없이 커밋하지 않습니다

이 규칙은 프레임워크 모드에도 동일하게 적용됩니다. 스킬과 에이전트 편집도 게임
코드와 같은 승인 절차를 거칩니다.

전체 프로토콜과 예시는 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`를 참고하십시오.

> **첫 세션인가요?** 엔진 설정도 게임 컨셉도 없는 상태라면 `/start`를 실행해
> 가이드 온보딩을 시작하십시오.

## 코딩 표준

@.claude/docs/coding-standards.md

## 컨텍스트 관리

@.claude/docs/context-management.md
