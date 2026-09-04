---
name: aws
description: Guidance for working with AWS services (S3, IAM, Lambda, ECS/EC2, Bedrock, boto3) safely — including credential handling, least-privilege IAM, and typical integration patterns for LLM apps. Use when the user asks to write AWS SDK (boto3) code, design IAM policies, provision or reference AWS infrastructure, or integrate a service (S3, Bedrock, Lambda, etc.) into this project.
metadata:
  type: cloud
  provider: aws
---

# AWS Skill

## When to Use
- The user asks to write or review `boto3` code against AWS services.
- The user asks about IAM policies, roles, or permission scoping.
- The user asks to integrate AWS Bedrock, S3, Lambda, or similar services into this project (e.g., as an alternative model provider or storage backend for deep agent files).
- The user asks about AWS cost, region selection, or deployment topology at a conceptual level.

## How to Use
1. Read `INSTRUCTIONS.md` for credential-handling rules, least-privilege IAM guidance, and this project's conventions for treating AWS as an optional integration.
2. Read `EXAMPLES.md` for boto3 code patterns (S3 read/write, IAM policy JSON, Bedrock invocation).
3. Never hardcode credentials or account IDs; follow the credential-handling section in `INSTRUCTIONS.md` exactly.

## Quick Reference
- Never hardcode AWS access keys/secrets in code, notebooks, or config files — use environment variables, `~/.aws/credentials`, or an assumed role.
- Default to least-privilege IAM policies scoped to specific resources/actions, not `"*"` wildcards.
- Treat any AWS provisioning, deletion, or IAM change as a risky action requiring explicit user confirmation before executing (see the "Executing actions with care" guidance already in effect for this session).
- Prefer `boto3` for SDK calls; use the AWS CLI only when scripting outside Python.
