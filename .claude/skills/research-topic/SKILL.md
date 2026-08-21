---
name: research-topic
description: Research a topic in depth using both Exa and web search, then produce a synthesized, sourced summary. Use when the user asks to "research X", "look into X", "find out about X", or wants a well-sourced briefing on a topic rather than a quick one-off search.
---

# Research Topic

Research the given topic using **both** Exa and general web search, then synthesize the findings into one coherent, sourced answer. Do not rely on a single source engine — the point of this skill is triangulating across engines to reduce blind spots and single-source bias.

## Steps

1. **Clarify scope fast, don't stall.** If the topic is ambiguous (e.g. could mean a company, a technology, a person), make a reasonable assumption and state it up front rather than asking — unless it's genuinely a coin flip, in which case ask one short question.

2. **Check for Exa.** Run `ToolSearch` with query `"exa"` to see if an Exa MCP tool (e.g. `mcp__exa__web_search_exa`, `mcp__exa__research_paper_search`, or similar) is connected in this session.
   - If found, load it and use it for at least one high-quality pass (Exa is generally strong at neural/semantic search and finding authoritative or less-SEO-optimized sources).
   - If not found, note that Exa isn't connected in this session and proceed with web search only — don't block the research on it.

3. **Run WebSearch.** Use the `WebSearch` tool with 2-4 targeted queries covering different angles of the topic (e.g. overview/definition, recent developments, comparisons/criticism, technical details). Vary phrasing per query rather than repeating the same query.

4. **Deepen key sources.** For the 2-4 most load-bearing or authoritative results from either engine, use `WebFetch` to pull full content when the search snippet isn't enough to answer confidently.

5. **Cross-check.** Where Exa and WebSearch surface conflicting claims, note the discrepancy explicitly rather than silently picking one side.

6. **Synthesize, don't dump.** Produce a single coherent write-up, not a list of search results:
   - Lead with a direct 2-4 sentence answer/summary.
   - Follow with organized sections for key facts, context, and any notable disagreement or uncertainty in sources.
   - Keep it proportional to the topic's complexity — don't pad a simple question into a long report.

7. **Always cite sources.** End with a `Sources:` section listing markdown links `[Title](URL)` for every source actually used (from both Exa and WebSearch). Never state a fact without it being traceable to a source in this list.

## Notes

- This skill is for genuine research/briefing requests, not quick factual lookups — if the user just wants one fact, a single WebSearch call is fine and this skill is unnecessary overhead.
- Prefer primary/authoritative sources (official docs, original announcements, papers) over aggregator blogspam when both are available.
- If the topic touches Claude/Anthropic specifically, still run this skill's process, but also apply the project's `claude-api` skill guidance if relevant to avoid stale model/pricing info.
