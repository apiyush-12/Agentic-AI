---
name: report-writer
description: Write a structured report summarizing the work done and the final answer whenever the deep agent completes a task or answers a user's query. Use this at the end of every task — after research, code changes, or multi-step work — to produce a consistent, skimmable report of what was done, what was found, and what (if anything) remains.
metadata:
  type: output-format
---

# Report Writer Skill

## When to Use
- Always, at the end of a deep agent task, right before delivering the final answer to the user.
- Applies regardless of task type: research, coding, analysis, or multi-step orchestration.

## How to Use
1. Read `INSTRUCTIONS.md` for the required report structure and formatting rules.
2. Read `EXAMPLES.md` for worked example reports across different task types.
3. Generate the final report following that structure, then present it as the deep agent's answer to the user (write it to a file under `deepagent/projects/` if the user's workflow expects persisted reports, in addition to returning it inline).

## Quick Reference
- Every report has: a one-line summary, key findings/changes, and next steps (or "none" if the task is fully complete).
- Keep the report proportional to the task — a small task gets a short report, not padded sections.
- Never fabricate results; if something wasn't verified, say so explicitly.
