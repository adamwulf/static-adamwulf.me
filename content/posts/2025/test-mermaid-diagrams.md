---
title: "Test: Mermaid Diagram Support"
date: 2025-01-16
draft: true
---

This post demonstrates Mermaid.js diagram support with a toggle between diagram and code views.

## Simple Flowchart

```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Awesome!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
```

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Server
    User->>Browser: Click toggle button
    Browser->>Browser: Toggle view
    Browser->>User: Show diagram/code
    User->>Server: Request page
    Server->>User: Return HTML
```

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    class Cat {
        +boolean indoor
        +meow()
    }
    Animal <|-- Dog
    Animal <|-- Cat
```

Each diagram above has a toggle button in the top-right corner. Click "View Code" to see the Mermaid syntax, or "View Diagram" to see the rendered visualization.
