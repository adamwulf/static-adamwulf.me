+++
title = "Private MCP to connect Claude to my email"
date = "2025-09-22T10:27:10+0000"
slug = "private-mcp-to-connect-claude-to-my-email"
type = "post"
draft = true
+++

I'm continuing my [PikaPod](https://www.pikapods.com/) adventures, and I'm loving it!

I've been using Claude Code as my personal assistant for a few months now. I have a custom Mac app MCP server that can relay my calendar events and reminders, contacts, location, weather, as well as simple custom "todo" list and the ability to read/write markdown files to a dedicated folder.

It's been a huge help! I can ask natural language questions about my daily schedule and todo items. It tracks long-running projects in markdown files with additional context. I can ask it to research and write files for large Muse projects for instance. Until now, though, it hasn't been able to access my email.

Apple doesn't provide SDK access to the user's Mail, so if I wanted to add this to my Mac app MCP server, I would have to add a parallel mail client, which is much heavier weight than I want to do.

## Activepieces

PikaPods offers a one-click install of [Activepieces](https://www.activepieces.com/), an open source [Zapier](https://zapier.com/)-like automation tool.

This tool provides a _ton_ of integrations out of the box, including Stripe, Slack, Zoho, Dropbox, Notion, you name it.


## Activepieces Setup

build pod, sign up as a user -> it only allows a single user. must invite for any more users

connect OpenAI, Claude, etc AI providers in admin panel

connect Zoho

## Setup Flow

1. MCP Tool -> set to waiting
2. Fetch Zoho Accounts
3. Fetch Zoho unread emails
4. Filter for tidy JSON
5. reply to MCP

## add to Claude Code

claude mcp -t sse active-pieces-zoho private-url-of-mcp-server

test by asking for unread emails.

bonus to allow for offset/limit