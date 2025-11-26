+++
title = "Easily creating MCP servers that fit my workflow"
date = "2025-11-26T10:27:10+0000"
slug = "easily-creating-mcp-servers-that-fit-my-workflow"
type = "post"
+++

I'm continuing my [PikaPod](https://www.pikapods.com/) adventures, and I'm loving it!

I've been using Claude Code as my personal assistant for a few months now. I have a custom Mac app MCP server that can relay my calendar events and reminders, contacts, location, weather, as well as simple custom "todo" list and the ability to read/write markdown files to a dedicated folder.

It's been a huge help! I can ask natural language questions about my daily schedule and todo items. It tracks long-running projects in markdown files with additional context. I can ask it to research and write files for large Muse projects for instance. Until now, though, it hasn't been able to access my email.

Apple doesn't provide SDK access to the user's Mail, so if I wanted to add this to my Mac app MCP server, I would have to add a parallel mail client, which is much heavier weight than I want to do.

## Activepieces

<img src="/wp-content/uploads/2025/11/Activepieces-MCP.png" alt="A screenshot showing an MCP configuration for fetching my email" width="200" align="left"/>

PikaPods offers a one-click install of [Activepieces](https://www.activepieces.com/), an open source [Zapier](https://zapier.com/)-like automation tool.

This tool provides a _ton_ of integrations out of the box, including Stripe, Slack, Zoho, Dropbox, Notion, you name it. What's more, it has an MCP feature that lets you turn any workflow into an MCP endpoint.

I've created MCP tools for fetching emails, writing draft replies, marking emails as read/unread, and I've started building tools to integrate into my bug tracker Notion database.

## Why Activepieces and PikaPods?

It's very important for me to know where my data is being processed, how it's being processed, and most importantly of all: who has access to it.

Just by using Claude Code, I know that Anthropic has access to my data, and I pay to make sure they don't use my data for training. Using PikaPods and Activepieces lets me create custom workflows that otherwise wouldn't be possible without giving my data to some random startup.

I'm able to build careful and useful AI tools for myself, bespoke to my workflow, all while knowing exactly how my data is being processed and accessed. Having this control and visibility is very important to me, espeically when so much of AI is "it's invisible and just works, probably™️."

## Add to Claude Code

Activepieces provides an sse endpoint for the MCP servers you define. While I was able to add the see endpoint into Claude with the following command:

```
claude mcp -t sse active-pieces-zoho private-url-of-mcp-server
```

For some reason, this stopped working for me with a recent Claude Code update. Instead, I now add the server through a local stdio proxy:

```
claude mcp add --transport stdio pikapod-remote -- npx -y mcp-remote private-url-of-mcp-server
```

If you've been looking for an easy way to play with custom MCP servers, I highly recommend spinning up Activepieces on a Pikapod.