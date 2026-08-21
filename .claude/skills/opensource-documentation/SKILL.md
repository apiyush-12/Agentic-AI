---
name: opensource-documentation
description: Look up current, version-accurate documentation for a specific open source library, framework, SDK, or CLI tool using Context7. Use when the user asks "how do I use X", "what's the API for X", "show me docs/examples for X", or names a library/package and wants to know how something works in it — especially when the concern is that training data might be stale.
---

# Open Source Documentation Lookup

Fetch current documentation for a named open source library using **Context7** as the primary source, instead of answering from training data (which can be stale for fast-moving libraries).

## Steps

1. **Identify the library and the specific question.** Don't just note "user asked about LangChain" — pin down the precise concept (e.g. "how to add subagents", "how to configure rate limiting", "migration from v0.x to v1"). Context7 queries work best scoped to one concept at a time.

2. **Check Context7 is available.** Run `ToolSearch` with query `"context7"` to confirm `mcp__plugin_context7_context7__resolve-library-id` and `mcp__plugin_context7_context7__query-docs` (or equivalently named context7 tools) are loaded.
   - If not available, tell the user Context7 isn't connected in this session and fall back to `WebSearch`/`WebFetch` against the library's official docs site — don't silently answer from memory.

3. **Resolve the library ID.** Call `resolve-library-id` with the library's proper name (e.g. "Next.js" not "nextjs") and a query describing what you're looking up. If multiple candidates come back, prefer the one with higher source reputation and snippet coverage, and matching what the user actually meant (e.g. official docs/reference over a random mirror) — don't just take the first result blindly.

4. **Query the docs.** Call `query-docs` with the resolved library ID and a single, specific concept per call. If the user's question spans multiple distinct concepts (e.g. "how do I set up auth AND configure caching"), make separate calls rather than combining them into one vague query.

5. **Cross-check freshness when it matters.** If the topic concerns a recent version bump, breaking change, or the user explicitly asks "what's new" / "latest version", also run a quick `WebSearch` to confirm Context7's snapshot isn't behind the very latest release notes — Context7 is generally fresh but not guaranteed real-time.

6. **Answer from what the docs actually say.** Quote/paraphrase the retrieved signatures, parameters, and code examples directly — don't blend in remembered API shapes from training data that might not match. If retrieved docs conflict with what you'd expect from memory, trust the retrieved docs and flag the discrepancy if it's material (e.g. "this differs from the pre-v1 API").

7. **Cite sources.** Include the Context7 source URLs returned with the snippets (they come with a `Source: https://...` line) so the user can click through to the canonical docs.

## Notes

- This skill is for **library/framework/SDK/CLI usage questions**, not for general programming concepts, business logic, or code review — don't invoke it for "how do I write a for loop" or "review my code."
- Prefer Context7 over plain WebSearch for anything library-specific (API syntax, config, version migration, setup) since Context7 indexes structured, current docs rather than blog posts that may be outdated or wrong.
- Don't call `resolve-library-id` or `query-docs` more than 3 times each per question — pick the best match and proceed rather than over-searching.
- If the library touches Claude/Anthropic specifically, also apply the project's `claude-api` skill guidance, since that skill has more specific pricing/model-id freshness rules than general Context7 lookups provide.
