#!/usr/bin/env python3
"""
WordPress to Hugo Migration Script

Extracts blog posts and pages from WordPress HTML export and creates Hugo content files.
Preserves HTML content without converting to Markdown for maximum compatibility.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
import html
from bs4 import BeautifulSoup


def clean_slug(path_parts):
    """Create a clean slug from URL path parts"""
    return path_parts[-2] if len(path_parts) > 1 else 'index'


def extract_post_metadata(soup, file_path):
    """Extract metadata from WordPress HTML"""
    metadata = {}
    
    # Extract title
    title_elem = soup.find('h1', class_='entry-title')
    if title_elem:
        metadata['title'] = title_elem.get_text().strip()
    else:
        # Fallback to page title
        title_elem = soup.find('title')
        if title_elem:
            metadata['title'] = title_elem.get_text().replace(' – Adam Wulf', '').strip()
        else:
            metadata['title'] = 'Untitled'
    
    # Extract date from time element
    date_elem = soup.find('time', class_='entry-date')
    if date_elem:
        date_str = date_elem.get('datetime')
        if date_str:
            try:
                # Parse ISO date format
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                metadata['date'] = date_obj.strftime('%Y-%m-%dT%H:%M:%S%z')
            except ValueError:
                # Fallback to text content
                metadata['date'] = date_elem.get_text().strip()
        else:
            metadata['date'] = date_elem.get_text().strip()
    else:
        # Try to extract date from URL path
        path_parts = str(file_path).split('/')
        year_pattern = re.search(r'/(\d{4})/', str(file_path))
        month_pattern = re.search(r'/(\d{4})/(\d{2})/', str(file_path))
        if year_pattern and month_pattern:
            year = year_pattern.group(1)
            month = month_pattern.group(1)
            metadata['date'] = f'{year}-{month}-01T00:00:00+00:00'
        else:
            metadata['date'] = '2008-01-01T00:00:00+00:00'  # Default fallback
    
    # Extract categories and tags
    article_elem = soup.find('article')
    if article_elem:
        classes = article_elem.get('class', [])
        categories = []
        tags = []
        for cls in classes:
            if cls.startswith('category-') and cls != 'category-uncategorized':
                categories.append(cls.replace('category-', '').replace('-', ' ').title())
            elif cls.startswith('tag-'):
                tags.append(cls.replace('tag-', '').replace('-', ' ').title())
        
        if categories:
            metadata['categories'] = categories
        if tags:
            metadata['tags'] = tags
    
    # Generate slug from file path
    path_parts = str(file_path).split('/')
    metadata['slug'] = clean_slug(path_parts)
    
    return metadata


def extract_post_content(soup):
    """Extract the main content from WordPress HTML"""
    content_elem = soup.find('div', class_='entry-content')
    if content_elem:
        # Remove WordPress-specific elements we don't want
        for elem in content_elem.find_all(['script', 'noscript']):
            elem.decompose()
        
        # Get the HTML content
        content_html = str(content_elem)
        
        # Clean up the content div wrapper
        content_html = re.sub(r'^<div[^>]*class="entry-content"[^>]*>', '', content_html)
        content_html = re.sub(r'</div>$', '', content_html.rstrip())
        
        return content_html.strip()
    
    return ''


def create_hugo_content_file(metadata, content, output_path):
    """Create a Hugo content file with front matter and HTML content"""
    
    # Create directory if it doesn't exist
    os.makedirs(output_path.parent, exist_ok=True)
    
    # Create front matter
    front_matter = ['+++']
    front_matter.append(f'title = "{metadata.get("title", "").replace('"', '\\"')}"')
    front_matter.append(f'date = "{metadata.get("date", "")}"')
    front_matter.append(f'slug = "{metadata.get("slug", "")}"')
    
    if 'categories' in metadata:
        categories_str = ', '.join(f'"{cat}"' for cat in metadata['categories'])
        front_matter.append(f'categories = [{categories_str}]')
    
    if 'tags' in metadata:
        tags_str = ', '.join(f'"{tag}"' for tag in metadata['tags'])
        front_matter.append(f'tags = [{tags_str}]')
    
    front_matter.append('type = "post"')
    front_matter.append('+++')
    
    # Write the file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(front_matter))
        f.write('\n\n')
        f.write(content)


def process_blog_post(html_file, hugo_content_dir):
    """Process a single blog post HTML file"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Skip if this doesn't look like a blog post
    if not soup.find('article') or not soup.find('div', class_='entry-content'):
        return False
    
    # Extract metadata and content
    metadata = extract_post_metadata(soup, html_file)
    content = extract_post_content(soup)
    
    if not content.strip():
        print(f"Warning: No content found in {html_file}")
        return False
    
    # Extract year, month, and slug from path
    year_match = re.search(r'/(\d{4})/', str(html_file))
    month_match = re.search(r'/(\d{4})/(\d{2})/', str(html_file))
    
    if year_match and month_match:
        year = year_match.group(1)
        month = month_match.group(1)
        slug = metadata['slug']
        
        # Create Hugo content path: content/posts/YYYY/MM/slug.html
        output_path = hugo_content_dir / 'posts' / year / month / f'{slug}.html'
    else:
        # Fallback for non-dated content
        output_path = hugo_content_dir / 'posts' / f'{metadata["slug"]}.html'
    
    create_hugo_content_file(metadata, content, output_path)
    print(f"Migrated: {html_file} -> {output_path}")
    return True


def process_static_page(html_file, hugo_content_dir):
    """Process a static page (about, projects, etc.)"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract page content - look for main content area
    content_elem = soup.find('div', class_='entry-content') or soup.find('main') or soup.find('div', class_='site-content')
    if not content_elem:
        print(f"Warning: No content found for page {html_file}")
        return False
    
    # Extract metadata
    metadata = extract_post_metadata(soup, html_file)
    content = extract_post_content(soup) or str(content_elem)
    
    # Clean up content if we got the full site-content div
    if 'site-content' in str(content_elem.get('class', [])):
        # Find the actual content within site-content
        inner_content = content_elem.find('div', class_='entry-content') or content_elem.find('main')
        if inner_content:
            content = str(inner_content)
    
    # Determine page name from file path
    page_name = os.path.basename(os.path.dirname(html_file))
    if page_name in ['about', 'projects', 'open-source']:
        output_path = hugo_content_dir / f'{page_name}.html'
        metadata['type'] = 'page'
        create_hugo_content_file(metadata, content, output_path)
        print(f"Migrated page: {html_file} -> {output_path}")
        return True
    
    return False


def main():
    if len(sys.argv) != 3:
        print("Usage: python migrate.py <wordpress_export_dir> <hugo_site_dir>")
        sys.exit(1)
    
    wp_dir = Path(sys.argv[1])
    hugo_dir = Path(sys.argv[2])
    
    if not wp_dir.exists():
        print(f"Error: WordPress export directory {wp_dir} does not exist")
        sys.exit(1)
    
    if not hugo_dir.exists():
        print(f"Error: Hugo site directory {hugo_dir} does not exist")
        sys.exit(1)
    
    hugo_content_dir = hugo_dir / 'content'
    hugo_content_dir.mkdir(exist_ok=True)
    
    # Process blog posts
    print("Processing blog posts...")
    post_count = 0
    
    # Find all blog post HTML files (in year/month/day or year/month/title structure)
    for html_file in wp_dir.glob('**/index.html'):
        # Skip root index and pagination
        if str(html_file).endswith('/index.html'):
            path_parts = str(html_file).split('/')
            # Look for year/month/slug/index.html pattern
            if len(path_parts) >= 4 and re.match(r'\d{4}', path_parts[-4]):
                if process_blog_post(html_file, hugo_content_dir):
                    post_count += 1
    
    print(f"Migrated {post_count} blog posts")
    
    # Process static pages
    print("Processing static pages...")
    page_count = 0
    for page_dir in ['about', 'projects', 'open-source']:
        page_file = wp_dir / page_dir / 'index.html'
        if page_file.exists():
            if process_static_page(page_file, hugo_content_dir):
                page_count += 1
    
    print(f"Migrated {page_count} static pages")
    print(f"Total migration complete: {post_count} posts, {page_count} pages")


if __name__ == '__main__':
    main()