# GitHub

---

## 2026-06-19 - How we built an internal data analytics agent

link: https://github.blog/ai-and-ml/github-copilot/how-we-built-an-internal-data-analytics-agent/
authors: Matteo Vasirani, Cynthia Joseph
type: blog
tags: text-to-sql, evals, agent-harness, semantic-layer, mcp
retrieved: 2026-09-21
content: original summary; full article available at the source link

---

### Summary

GitHub’s internal Qubot agent answers exploratory analytics questions through Slack, VS Code, and Copilot CLI. Its Slack integration runs a Copilot Cloud Agent and saves reports in pull requests. MCP tools provide access to Kusto and Trino, with the agent choosing between them according to the question.

Its context combines product telemetry documentation, analyst-maintained query guidance, and business-owned metric definitions. A context agent organizes contributions from multiple repositories. Changes to context or agent configuration pass through offline evaluations that measure accuracy, completion, and duration. GitHub reports that curated context improved answer accuracy and made correct responses three times faster in its experiments.
