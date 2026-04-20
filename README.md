# Deprecated: Deliveroo Snowflake MCP Server

This repository is **deprecated** and no longer maintained.

It was originally a fork of an early community Snowflake MCP server, created before an official option existed. Since then, Snowflake has released its own MCP server, which is now the supported path.

## What to use instead

1. **Preferred: Deliveroo AI Semantic Layer** (bi-pipeline-v2) — auto-installs and configures the official Snowflake MCP globally on your machine, and gives you a curated semantic layer on top. Setup guide:
   https://docs.google.com/document/d/1UIuu46KGi0MEtEnrmaSgap_BZ-bxbvchOx0rHHgoPSQ/edit?usp=sharing
   Announcement (Slack): https://doordash.slack.com/archives/C0AMY4M47FW/p1776670205405119

2. **Official Snowflake MCP server** (if you want to use it directly without the semantic layer):
   https://github.com/Snowflake-Labs/mcp

## Still need the old code?

The last state of `main` before deprecation is preserved on the [`backup`](https://github.com/deliveroo/mcp-snowflake-server/tree/backup) branch. It is provided as-is and will not receive updates.
