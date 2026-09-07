# Report Writer Skill — Instructions

## Purpose
Give every deep agent answer a consistent shape so the user can scan it quickly, regardless of which sub-skill (python, langgraph, aws, or none) produced the underlying work.

## Required Report Structure

```markdown
## Summary
<1-2 sentences: what was asked, what was done, and the bottom-line result.>

## Details
<The substantive answer/findings/changes. Use whatever format fits the content —
prose for research, a diff/file list for code changes, a table for comparisons.
This is the main body; size it to the task.>

## Files Changed / Created
<Bulleted list of paths touched, or "None" if no files were modified.>

## Verification
<What you actually checked (tests run, code executed, output inspected) to confirm
correctness. If nothing could be verified (e.g., no test suite, UI not run), say so
explicitly rather than implying it was checked.>

## Next Steps
<Bulleted list of remaining work, open questions, or follow-ups the user may want.
Use "None — task is complete." if there is nothing outstanding.>
```

## Formatting Rules
- Keep the `Summary` to 1-2 sentences — it must stand alone if the user reads nothing else.
- Omit a section entirely (don't write "N/A") only if it truly doesn't apply; otherwise state explicitly why it's empty (e.g., "No files changed — this was a read-only analysis.").
- Scale section length to the task: a one-line bug fix does not need multi-paragraph `Details`.
- Never claim something was tested/verified unless it actually was in this session. State assumptions and unverified claims plainly.
- Use concrete references (`file_path:line_number`, command output, specific numbers) over vague claims ("it works now").
- Do not pad the report with restated instructions, apologies, or meta-commentary about the process.

## When the Underlying Task Used Another Skill
- If the python, langgraph, or aws skill was used to do the work, the report's `Details` section should reflect the outcome of that work (code written, graph behavior, AWS resource state) — not re-explain that skill's own instructions.
- If a sub-agent was delegated to, summarize only its final result in the report, not its intermediate tool trace.

## Persisting Reports
- For tasks whose outputs should be durable (per this project's convention of writing intermediate/final artifacts to `deepagent/projects/`), also write the report to a Markdown file under `deepagent/projects/` (e.g., `deepagent/projects/reports/<short-task-slug>.md`) in addition to returning it as the chat answer.
- Skip persisting to disk for trivial one-off questions where no artifact is expected.
