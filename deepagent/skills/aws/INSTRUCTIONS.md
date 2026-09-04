# AWS Skill — Instructions

## Credential Handling
- Never write access keys, secret keys, or session tokens into source code, notebooks, or committed config files.
- Load credentials via one of: environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`), the shared credentials file (`~/.aws/credentials`) with a named profile, or an assumed IAM role (e.g., instance profile, `AWS_PROFILE`, or `sts.assume_role`).
- When a notebook needs AWS access, load config the same way other secrets are loaded in this repo: via `.env` + `python-dotenv`, referencing environment variable names only — never literal values.
- If asked to "hardcode" credentials for convenience, push back and use environment variables instead.

## IAM & Least Privilege
- Scope IAM policies to specific actions and resource ARNs; avoid `"Action": "*"` or `"Resource": "*"` unless the user explicitly requires a broad policy and understands the tradeoff.
- Prefer resource-level conditions (`Condition` blocks) over broad allows when a policy could otherwise be scoped tighter.
- When writing a policy for a new integration, grant only the actions the code actually calls (e.g., `s3:GetObject`, `s3:PutObject` — not `s3:*`) .
- Separate read and write permissions where the use case allows it.

## Safe Execution of AWS Actions
- Treat any action that provisions, modifies, or deletes real AWS resources (creating buckets/roles, deleting objects, changing IAM policies, launching/terminating instances) as a risky, hard-to-reverse action: describe what you're about to do and confirm before executing, consistent with this session's general safety rules.
- Prefer `--dry-run` flags or read-only calls (`describe_*`, `list_*`, `get_*`) to verify state before making a mutating call.
- Never assume a region — use the region already configured in the environment/profile, or ask if none is set and the choice matters.

## Typical Integration Patterns for This Project
- **S3 as a deep agent filesystem backend**: if the project needs persistent, shared storage for agent scratch files beyond local disk, S3 is a reasonable choice — implement it behind the same backend interface used by `FilesystemBackend` rather than calling boto3 directly from agent logic.
- **Bedrock as an LLM provider**: this repo currently integrates OpenAI, Groq, Mistral, and Google GenAI via LangChain provider packages (see root `CLAUDE.md`). Adding Bedrock follows the same pattern — a `langchain-aws` `ChatBedrock` (or equivalent) integration, with credentials loaded via environment variables, not hardcoded.
- **Lambda**: only relevant if the user wants to deploy agent logic as a serverless function; keep the Lambda handler thin and delegate to the same core logic used locally, not a duplicated implementation.

## Workflow Before Writing AWS Code
1. Confirm which AWS service and boto3 client/resource the task actually needs — don't provision broader access than the task requires.
2. Check whether `boto3` (and any `langchain-aws` equivalent) is already a dependency; if not, add it via `uv add` per the Python skill's dependency workflow.
3. Write the minimal IAM policy and boto3 calls needed; avoid wildcard permissions.
4. For any mutating call, state what will change and get confirmation before running it against a real AWS account.
