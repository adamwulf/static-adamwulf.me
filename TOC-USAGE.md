# Table of Contents Usage

## How to Use

To add a table of contents to any post or page, use the `toc` shortcode in your Markdown content:

```markdown
{{< toc >}}
```

## Example

```markdown
---
title: "My Post"
date: 2026-01-16
---

{{< toc >}}

## Introduction

This is the introduction...

## Main Section

### Subsection 1

Content here...

### Subsection 2

More content...

## Conclusion

Final thoughts...
```

## Configuration

The table of contents configuration is set in `hugo.toml`:

```toml
[markup.tableOfContents]
  startLevel = 1    # Start from H1 headings
  endLevel = 3      # Include up to H3 headings
  ordered = false   # Use unordered list (bullets)
```

## How It Works

- The `{{< toc >}}` shortcode renders Hugo's built-in `{{ .Page.TableOfContents }}`
- Hugo automatically generates the TOC from your Markdown headings (H1, H2, H3, etc.)
- The TOC is generated at build time and includes anchor links to each heading
- Configure which heading levels to include using the `startLevel` and `endLevel` settings

## Styling

The TOC is rendered as an HTML `<nav>` element with an `<ul>` list. You can style it with CSS by targeting:

```css
nav#TableOfContents {
  /* Your styles here */
}
```
