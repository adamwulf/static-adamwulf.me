# adamwulf-hugo

Hugo static site migration from WordPress HTML export.

## Migration Setup

This site was migrated from a WordPress static HTML export using a custom Python script.

### Dependencies

- Hugo (installed via Homebrew: `brew install hugo`)
- Python 3 with BeautifulSoup4

### Python Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install beautifulsoup4
```

### Running the Migration

```bash
# Activate virtual environment
source venv/bin/activate

# Run migration script
python migrate.py <wordpress_export_dir> <hugo_site_dir>

# Example:
python migrate.py /path/to/wordpress-export /path/to/adamwulf-hugo
```

### Development

```bash
# Serve site locally
hugo server -D
```

## Site Structure

- `/content/posts/YYYY/MM/` - Blog posts organized by date
- `/content/` - Static pages (about.html, projects.html, etc.)
- `/static/` - All static assets copied from WordPress export
- `/themes/adamwulf/` - Custom minimal theme

## Migration Features

- Preserves HTML content (no Markdown conversion)
- Maintains URL structure from WordPress
- Extracts metadata from HTML (title, date, tags, categories)
- Copies all static assets
- Reuses existing WordPress CSS/JS