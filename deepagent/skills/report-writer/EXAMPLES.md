# Report Writer Skill — Examples

## Example 1: Code change task

```markdown
## Summary
Fixed the `load_config` function to raise a clear error when the config file is missing, instead of silently returning an empty dict.

## Details
`load_config` in `app/config.py:12` previously called `path.read_text()` without
checking existence, which raised an unhelpful `FileNotFoundError` from deep inside
`pathlib`. Added an explicit existence check that raises
`FileNotFoundError(f"Config file not found: {path}")` before attempting to read.

## Files Changed / Created
- `app/config.py` — added existence check in `load_config`

## Verification
Ran `uv run pytest tests/test_config.py` — all 4 tests pass, including a new test
for the missing-file case.

## Next Steps
None — task is complete.
```

## Example 2: Research/question-answering task

```markdown
## Summary
LangGraph's `Store` API provides cross-thread memory, distinct from a checkpointer which is per-thread.

## Details
- `MemorySaver` / other checkpointers persist state **per thread**, enabling resume of a single conversation.
- `Store` (e.g., `InMemoryStore`, or a persistent backend) persists key-value data **across threads**, suitable for long-term memory shared between separate sessions with the same user.
- In this repo, `deepagent/3-backends.ipynb` demonstrates both, but currently only wires up the in-memory checkpointer — no `Store` is configured yet.

## Files Changed / Created
None — this was a read-only research question.

## Verification
Confirmed against the current LangGraph docs and cross-checked with the imports
already present in `deepagent/3-backends.ipynb`.

## Next Steps
- If cross-session memory is needed, wire up a `Store` implementation (see the
  langgraph skill's EXAMPLES.md for a snippet).
```

## Example 3: Multi-step task with a sub-agent delegation

```markdown
## Summary
Added an `aws` skill for boto3/IAM guidance and verified it loads correctly via the deep agent's SkillsMiddleware.

## Details
Created `deepagent/skills/aws/{SKILL.md,INSTRUCTIONS.md,EXAMPLES.md}` covering
credential handling, least-privilege IAM, and boto3 patterns. A sub-agent verified
the YAML frontmatter parses correctly and the skill name matches its directory
name (a hard requirement of the Agent Skills spec).

## Files Changed / Created
- `deepagent/skills/aws/SKILL.md`
- `deepagent/skills/aws/INSTRUCTIONS.md`
- `deepagent/skills/aws/EXAMPLES.md`

## Verification
Sub-agent parsed the frontmatter with `yaml.safe_load` and confirmed `name: aws`
matches the `aws/` directory name, and both `name` and `description` are present
and within the spec's length limits.

## Next Steps
None — task is complete.
```

## Example 4: Task with an unverifiable claim (be explicit about it)

```markdown
## Summary
Updated the Bedrock integration example to use `ChatBedrock`; the exact model ID string could not be verified against a live account.

## Details
Added a `ChatBedrock` usage example using model ID
`anthropic.claude-sonnet-5-v1:0`. This ID was not verified against an actual AWS
Bedrock account/region, since no AWS credentials are configured in this
environment.

## Files Changed / Created
- `deepagent/skills/aws/EXAMPLES.md`

## Verification
Not verified against a live AWS account — no credentials available in this
environment. Confirm the exact model ID string in the AWS Bedrock console before
relying on this example.

## Next Steps
- Verify the Bedrock model ID against the target AWS account/region before use.
```
