# pinterest-sites

AI side-business execution repository (Pinterest-related sites).

## Operating principle

Cost-optimized multi-AI command chain. Full design: [docs/AI_OS.md](docs/AI_OS.md).

- **Codex** — commander (司令塔): overall task priorities, final escalation authority
- **GPT / Sol** — deputy commander (副司令塔): task decomposition, AI assignment, senior review, business/quality gate
- **Free/cheap AI layer** — first execution force (第1実行部隊): OpenRouter free, Qwen, Kimi, Gemini free tier, DeepSeek (low-cost only), MiniMax, local Qwen, etc. — bulk/routine work, tried first
- **Claude Code** — execution lead (実行部長, second execution force): ordinary implementation, GitHub work, debug, test, refactoring, recovery of tasks the free layer fails
- **Astra** — Principal/Architect: architecture and irreversible technical decisions only, when GPT/Sol review escalates

Use the cheapest capable worker first. Escalate only when quality, permissions, or architectural judgment requires it — not simply because a task is nontrivial.

Implementation work should prioritize revenue-producing tasks over AI infrastructure work.
