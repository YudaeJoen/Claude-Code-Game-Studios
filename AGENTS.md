# AGENTS.md — Claude Code Game Studios

이 저장소의 규칙은 `CLAUDE.md` 가 기준이다. 작업 전에 반드시 `CLAUDE.md` 를 읽고, 이 파일은 요약으로만 쓴다.

## 프로젝트 정보
- 49개 Claude Code 서브에이전트(`.claude/agents/`), 72개 스킬(`.claude/skills/`), 훅(`.claude/hooks/`), 규칙(`.claude/rules/`), 템플릿(`.claude/docs/templates/`)으로 인디 게임 개발을 진행하는 프레임워크. 외부 오픈소스 템플릿을 가져와 쓰는 중이다.
- **두 가지 모드**를 먼저 판별한다. `src/` 에 `.gitkeep`+`CLAUDE.md` 만 있고 엔진이 `[TO BE CONFIGURED]` 이면 **프레임워크 모드**(템플릿 자체 유지보수), `src/` 에 실제 게임 코드가 있으면 **게임 모드**. 프레임워크 모드에서는 에이전트·스킬·훅·규칙 파일이 곧 프로덕션 코드다.
- 파이프라인: `concept → systems-design → technical-setup → pre-production → production → polish → release` (`.claude/docs/workflow-catalog.yaml` 이 유일한 기준). 단계 산출물을 만드는 새 스킬은 반드시 이 파일에 등록한다.
- 게이트 프롬프트는 `.claude/docs/director-gates.md` 한 곳에만 둔다. 스킬은 게이트 ID 를 참조하고 프롬프트를 복사하지 않는다.
- `CCGS Skill Testing Framework/` 는 독립 테스트 스펙이다. `.claude/` 어디서도 이 폴더를 import 하지 않는다.

## 검증
- 스킬/에이전트 파일을 바꾸면 프론트매터 계약(`name`, `description`, `tools`, `model` 등)을 지켰는지 확인하고, `CCGS Skill Testing Framework/catalog.yaml` 의 해당 스펙을 갱신한다.
- 훅(`.claude/hooks/*.sh`)을 바꾸면 `.claude/settings.json` 등록과 timeout 을 함께 확인한다.

## 규칙
- 이 저장소는 템플릿 원본이므로 변경이 모든 하위 프로젝트로 전파된다. 작은 수정이라도 영향 범위를 적는다.
- 답변은 한국어, 커밋 메시지는 기존 이력(영어 요약)을 따른다.
