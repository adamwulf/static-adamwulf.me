+++
title = "Itty Bitty AI Agent Orchestrator"
date = "2026-01-16T10:27:10+0000"
slug = "itty-bitty-ai-agent-orchestrator"
type = "post"
+++

I bet you've heard of [Gas Town](https://github.com/steveyegge/gastown), and if you haven't, you're in for an proper adventure. As I read through [Steve's ~~introduction~~ manifesto](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04), I loved the vision but was overwhelmed by the scale. He's not messing around, Gas Town requires sqlite for holding state, uses [beads](https://github.com/steveyegge/beads) for issue tracking and state management, supports pluggable AI runtimes. Want to wrap your head around it? welcome to the Mayor, rigs, convoys, polecats, crew, hooks, dogs, and so many more metaphors and tv/movie references.

In proper self-nerd-snipe fashion, I thought to myself "surely there's an easier way to do multi-agent coordination?!", and [`ittybitty`](https://github.com/adamwulf/ittybitty) was born.

{{ .TableOfContents }}

## TLDR

Want to just jump in? Clone https://github.com/adamwulf/ittybitty add it to your `$PATH`. Then, from any git repo on your system:

``` bash
# start a new agent
ib new-agent --name hellobot --model haiku "say hello, and then wait for instructions"

# show the agent's status
ib list

# agents can talk to each other
ib new-agent --name friendbot --model haiku "say hello to hellobot by sending them a message"

# see their claude session history
ib look friendbot

# use the interactive dashboard (Ctrl+c to exit)
ib watch

# there's gotta be a better word for this than 'kill'?
ib kill hellobot
ib kill friendbot
```

Want more detail? Here we go!

## Purpose

I use claude code _a lot_. It's always running while I code, either working on a task or helping me debug. I use it as a personal assistant. I use it to run long-running web research tasks. I use it went I'm coding, and when I'm not coding, and everything in-between.

I often want to run multiple instances of `claude` in git worktrees, but don't want to open/close/merge the worktrees myself. I basically want a normal `claude` instance, but one that can spawn and manage many other `claude` instances too. I want 10 agents to _feel_ like 1 agent, which means I need to have easy visibility into what the team is doing.

## What do I want?

I love projects with constraints, that's where the creativity happens, and I set myself some stringent constraints:

### No dependencies

Gas Town requires you to buy into using beads with sqlite as the task coordination layer, and I want a tool that fits into _my_ workflow instead of me fitting into _its_ workflow. That means, no `beads`, no `sqlite`. It should be as close to "just claude" as is possible to get. And I got very close - the only required dependency that doesn't come with macOS is `tmux`.

I went further - no build scripts. "It works out of the box" → Nope, I don't even want a box. It should work while I build it and should work when you download it, those should be the same thing. That means _pure bash_.

### No YOLO

If your tool requires yolo mode, it's a non-starter for me. I need a tool that I can run without needing to spin up a container and still have control over what it can and can't do.


### Easy to understand

The mental model is "it's just `claude`, and you can make lots of them." No metaphors, no stories, no complexity, just AI agents that you tell what to do.


### Agents can make agents

_Yo dawg, I heard you like agents._ Agents should be able to spin up helper agents to run tasks in parallel. You should also be confident they won't [fork bomb](https://en.wikipedia.org/wiki/Fork_bomb) your system.


### Agents can talk to each other

Sometimes agents get stuck, or don't have the full information they need. Or, after spawning a team of 6 agents, I might remember another core requirement, and I don't want to manually message each agent that might be working on it. I should tell the top manager of a task, and it should tell all of its workers that need to know.

### User visibility

I should be able to quickly see how many agents are running, which agents report to which other agents. I want to see their `claude` session history. I should see when an agent tries to use a denied tool and what that tool is incase I want to adjust my pre-approved tool list.


### Staying in control

If I'm going to build a system where an AI can spawn other AIs, I need to have an escape hatch in case _too many_ AIs get spawned. I want two controls: the "oops button" that will immediately close down all running AIs; in ittybitty, this is `ib nuke`. I also want to set a max limit on the number of agents that can be running at any one time. If one of the agents tries to create a new agent, I want it to be rejected if the system is already at the cap.


### Command line interface

This is an extension of the [No dependencies](#no-dependencies) requirement, I don't want to have to use a different tool in order use this tool. It should run in the command line - both the individual commands themselves, as well as a dashboard showing active status.


### Worktree separation

As I was building this, I discovered that teh agents don't quite know how to use git worktrees effectively. Their default is to use git fetch when trying to see other agent's work, even though every agent is already working in a local worktree. Since agents can see which other agents are running, they can discover where on disk those other agent's worktrees are, so instead of using git tools to see diffs between branches, agents were `cd`ing into each others workspaces and forgetting where their 'home' workspace was. The tool needs to enforce boundaries between agents so that they don't wander outside their worktree and start stepping on each other's toes.


### Automatic notifications

The system should somehow monitor agent status so that agents that are stuck and get unstuck, and agents that are complete can have their manager's auto-notified without needing to remember to notify on their own. When an agent completed its work, its manager should know immediately without needing to burn tokens polling its status.


### Minimal steps to get started

I wanted to build something that anyone could download and start using with zero setup. I don't want to build a monolithic system that takes non-trivial setup time, I wanted something _simple_ that could be immediately useful.


## What did I build?


``` mermaid
flowchart LR
A[You - Human] <-->|claude code| B[Primary Claude]
B -->|spawns via ib| C[Manager Agent]
C -->|spawns via ib| D[Worker Agents]
E[ib watch] -->|new agent 'a' key| C
A -->|command line| E
```

``` bash
ib new-agent "testing"
```


Benefits:

Not yolo mode. Permissions auto deny unless approved by you, and you have visibility into denied tools to add later

Worktrees for every agent, no toe stepping

Simple model, easy to understand

Send messages between agents

Send messages to the user running Claude

User Claude has auto visibility into agent status

Nuke option for safety

Command line interface, including interactive status

Agents can move between worktrees, so can’t mess up their cwd

Watchdogs auto notify agents

Minimal requirements to use and run


















# Yegge's Priorities for Building Gas Town

## Executive Summary

Gas Town represents a fundamental shift in software development philosophy: building a multi-agent orchestration system that prioritizes **throughput over perfection**, **persistent state over ephemeral memory**, and **autonomous coordination over human micromanagement**. Yegge's vision is to enable development "where the constraint isn't clock time but rather creativity and dollars in Claude tokens."

---

## Technical Dependencies

Gas Town requires a specific technology stack to operate effectively:

### Core System Requirements

| Dependency | Version | Purpose |
|------------|---------|---------|
| **Go** | 1.23+ | Primary runtime language for Gas Town itself |
| **Git** | 2.25+ | Required specifically for worktree functionality (core to state persistence) |
| **SQLite3** | Default system version | Convoy database queries; pre-installed on macOS/Linux |
| **TMux** | 3.0+ | Recommended for full experience; enables multi-pane agent monitoring |

### Essential AI Runtime

| Dependency | Version | Purpose |
|------------|---------|---------|
| **Claude Code CLI** | Latest | Default and primary coding assistant runtime |
| **Beads (bd)** | 0.44.0+ | **Critical dependency** for task/issue tracking with custom type support |

**Beads** is non-optional — it provides the dual storage system (SQLite + JSONL) that enables persistent work state and Git-tracked task management. Available at: `github.com/steveyegge/beads`

### Optional AI Runtimes

Gas Town supports multiple coding assistant platforms through pluggable runtime configuration:

- **Codex CLI** — Alternative runtime requiring additional config (`~/.codex/config.toml` must include `project_doc_fallback_filenames = ["CLAUDE.md"]`)
- **Gemini** — Google's coding assistant
- **Cursor** — AI-powered code editor
- **Auggie** — Additional runtime option
- **Amp** — Additional runtime option

**Runtime Limitations**: For runtimes lacking hook support (e.g., Codex), Gas Town deploys a startup fallback sequence after session initialization to handle context recovery and mail injection.

### Infrastructure Requirements

**Git Worktrees**: The architecture fundamentally depends on Git 2.25+ worktree support, as each agent operates in an isolated worktree while sharing the same repository. This enables:
- Parallel agent work without conflicts
- Persistent state tied to git branches
- Recovery from crashes via git-backed hooks

**Filesystem Access**: Agents require read/write permissions to:
- Local git repository and worktrees
- `.beads` directory (SQLite + JSONL storage)
- Hook directories for state persistence

**GitHub API Access**: For autonomous operations:
- Branch creation and pushing
- Pull request creation
- PR merging (if configured)

### Developer Maturity Requirement

**Stage 6-7 Developer**: Not a technical dependency, but Gas Town documentation explicitly states users should be "at least Stage 6, or maybe Stage 6 and very brave" to operate the system. This reflects the operational complexity and risk tolerance required.

### Configuration Files

- `settings/config.json` — Per-rig runtime configuration
- `~/.codex/config.toml` — Required if using Codex runtime
- `.beads/` directory — Beads task storage (SQLite + JSONL)
- TOML formula files — Optional for repeatable workflow definitions

---

## Core Design Priorities

### 1. **State Persistence Above All Else**

**Priority**: Solve the fundamental problem that "agents lose context on restart"

**Implementation**:
- Git-backed hooks serve as persistent storage for agent work
- Work state survives crashes and restarts
- Beads integration with dual storage system:
  - SQLite database for fast structured queries
  - JSONL file for Git-tracked version control and conflict resolution
  - 5-second auto-sync debounce between systems

**Philosophy**: "Work persists in git-backed hooks" — treating git worktrees as the source of truth rather than relying on volatile agent sessions.

### 2. **Scaling Through Structured Coordination**

**Priority**: Scale from individual agents to 20-30+ agents without chaos

**Implementation**:
- Acknowledges that "4-10 agents become chaotic"
- Structured coordination through **Convoys** (work tracking units that bundle issues)
- Hierarchical role-based agent structure:
  - **Mayor** 🎩 - Orchestration leader with full workspace context
  - **Deacon** - Operations management
  - **Witness** - Canonical state keeper
  - **Refiner** - Merge authority
  - **Polecats** 🦨 - Ephemeral worker agents for specific tasks

**Philosophy**: "Comfortable scaling to 20-30 agents" through structured work units rather than ad-hoc coordination.

### 3. **Self-Directed Agent Autonomy**

**Priority**: Enable agents to coordinate and make decisions without constant human intervention

**Implementation**:
- Built-in mailboxes, identities, and handoffs between agents
- Mayor serves as AI coordinator rather than requiring humans to route work
- Autonomous capabilities:
  - Creates branches in a disciplined way
  - Pushes branches to GitHub
  - Creates pull requests
  - **Merges PRs autonomously** (noted as surprising in testing)
- Users "tell the Mayor what you want to accomplish" rather than managing individual agents

**Philosophy**: "Creation and correction at the speed of thought" — agents should self-coordinate to maximize throughput.

### 4. **Parallel Execution at Scale**

**Priority**: Enable multiple agents to work simultaneously on different tasks

**Implementation**:
- Agent factory model spawning multiple specialized workers
- Parallel task execution (tested with 4+ agents working concurrently)
- Activity level described as "too much going on for you to reasonably comprehend"
- Mayor interface abstracts away complexity, keeping humans "one layer removed from the nitty gritty"

**Philosophy**: Shift development bottleneck from clock time to creative direction and token budget.

### 5. **Throughput Over Quality Gates**

**Priority**: Maximize velocity and accept that some work may need correction

**Implementation**:
- "Most work gets done; some work gets lost" — accepting imperfection
- Autonomous PR merging even when tests fail (observed behavior)
- "Code held lightly" approach among multiple coders
- Focus on rapid iteration and correction cycles

**Philosophy**: Explicitly prioritizes speed of creation and correction over traditional quality controls. The Mad Max theming acknowledges real risks: "Lots of people will get hurt while we learn how to scale it up."

### 6. **Graceful Degradation and Flexibility**

**Priority**: Support multiple operating modes and infrastructure constraints

**Implementation**:
- Multiple workflow modes:
  - **Mayor Workflow** (recommended): Full orchestration with convoy management
  - **Minimal Mode**: Without tmux, manual runtime management
  - **Manual Convoy**: Direct control over issue distribution
  - **Beads Formula**: TOML-defined repeatable processes
- Pluggable runtime system supporting multiple AI providers:
  - Claude, Gemini, Codex, Cursor, Auggie, Amp
  - Per-rig configuration overrides
  - Per-task runtime selection via `--agent` flags

**Philosophy**: Avoid tight coupling to specific technologies; support evolution and different use cases.

### 7. **Recoverable Work State**

**Priority**: Never lose work due to crashes, disconnections, or agent failures

**Implementation**:
- All work state stored in Beads ledger
- Git worktrees as separate checkouts sharing repository
- Hooks system for persistent agent context
- Work tracking survives agent restarts and system failures

**Philosophy**: Persistent, recoverable state management is non-negotiable for production multi-agent systems.

### 8. **Process Repeatability**

**Priority**: Enable encoding and reusing successful workflows

**Implementation**:
- Beads Formula integration for structured, repeatable processes
- TOML-defined workflows with dependencies
- Predefined processes become "trackable instances" stored as structured data
- Formula workflows provide reusable patterns for common tasks

**Philosophy**: Capture and institutionalize successful patterns rather than reinventing approaches each time.

---

## Architectural Trade-offs

### Accepted Costs

**Token Budget**: Testing showed ~$100/hour in Claude tokens (10x normal Claude Code expense per time unit)
- This is an accepted trade-off for parallel execution velocity
- Cost optimization became a community priority (cheaper inference endpoint PRs)

**Complexity**: The system introduces significant operational complexity
- Multiple worktrees, persistent state, coordination overhead
- Requires Stage 6-7 developer maturity to operate effectively

**Trust Boundaries**: Current design assumes agents have filesystem and GitHub permissions
- Optimistic assumption about "disciplined" branch creation
- Community identified this as a potential security/control concern

### Design Decisions

**Dual Storage System**: Beads uses both SQLite and JSONL
- SQLite for fast queries
- JSONL for Git-friendliness and conflict resolution
- Community noted this "reaches for Dolt without knowing about it"

**Mad Max Theming**: Intentional framing of risks and experimental nature
- Some community members felt this obscured rather than clarified architecture
- Others appreciated the honest acknowledgment of danger

**Human as Bottleneck**: System assumes "human accountability remains the identified bottleneck—not agent capability"
- Mayor abstraction keeps humans focused on direction, not implementation details
- Agents handle mechanical execution at machine speed

---

## Key Architectural Concepts

| Component | Purpose | Priority Addressed |
|-----------|---------|-------------------|
| **Mayor** | AI coordinator with full context | Self-coordination, autonomy |
| **Convoys** | Work bundling units | Scaling without chaos |
| **Hooks** | Persistent git-backed storage | State persistence, recovery |
| **Beads** | Task/issue tracking system | State management, repeatability |
| **Polecats** | Ephemeral worker agents | Parallel execution, scaling |
| **Rigs** | Project containers | Multi-project orchestration |
| **Crew Members** | Personal workspaces | Developer isolation |

---

## Development Philosophy Shifts

### From Traditional Development:
- Single developer → Agent factory
- Sequential execution → Parallel task distribution
- Manual coordination → AI orchestration (Mayor)
- Ephemeral sessions → Persistent work state
- Quality gates → Throughput + correction cycles
- Human doing → Human directing

### Yegge's Vision:
"Development where the constraint isn't clock time but rather creativity and dollars in Claude tokens"

This represents a fundamental reimagining of the software development process, accepting that the transition will be messy ("Lots of people will get hurt") but necessary to unlock agent-scale velocity.

---

## Community Observations

**What's Working**:
- Team structure "has the _team_ side about right"
- Parallel execution demonstrably faster than sequential
- State persistence prevents lost work

**Challenges Identified**:
- Cost per time unit still high (~10x)
- Trust boundary concerns with autonomous GitHub operations
- Terminology overlap creates confusion
- Requires mature developers to operate effectively

**Evolution Path**:
Community suggested "a version of this with normal names and expanded coordination" as system matures and patterns stabilize.

---

## Summary: The Core Bet

Steve Yegge is betting that:

1. **State persistence** solves the biggest blocker to multi-agent systems
2. **Autonomous coordination** (not human micromanagement) is required for agent-scale velocity
3. **Throughput-first** approach will prove more valuable than traditional quality gates
4. **Parallel agent execution** justifies 10x cost increase through radical speedups
5. **Structured roles** (Mayor, Convoy, etc.) provide the right abstraction layer for human oversight
6. The industry will learn to handle the risks and complexity as patterns emerge

The system is explicitly positioned as **experimental and dangerous**, acknowledging that "we're figuring out how to scale this up" rather than presenting a mature, safe solution.

---

*Sources: [GitHub - steveyegge/gastown](https://github.com/steveyegge/gastown), [Welcome to Gas Town - Hacker News Discussion](https://news.ycombinator.com/item?id=46458936), [A Day in Gas Town - DoltHub Blog](https://www.dolthub.com/blog/2026-01-15-a-day-in-gas-town/)*
