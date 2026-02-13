#!/usr/bin/env python3
"""
Portfolio Content Updater
This script scans the art directory and automatically updates both:
- Gallery page with all images
- Collections page with images organized by subfolder
"""

import os
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict

# Configuration
ART_FOLDER = "art"  # Relative to the script location
GALLERY_HTML = "pages/gallery.html"
COLLECTIONS_HTML = "pages/collections.html"
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}

# HTML markers
GALLERY_START = "<!-- GALLERY_IMAGES_START -->"
GALLERY_END = "<!-- GALLERY_IMAGES_END -->"
COLLECTIONS_START = "<!-- COLLECTIONS_START -->"
COLLECTIONS_END = "<!-- COLLECTIONS_END -->"


def find_all_images(art_folder: Path) -> List[Tuple[str, str]]:
    """
    Recursively find all supported images in the art folder.
    Returns list of tuples: (relative_path, filename)
    """
    images = []
    
    if not art_folder.exists():
        print(f"Error: Art folder '{art_folder}' does not exist!")
        return images
    
    for file_path in sorted(art_folder.rglob('*')):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            # Get path relative to gallery.html location (pages/)
            relative_path = os.path.relpath(file_path, Path(GALLERY_HTML).parent)
            # Convert to forward slashes for web
            relative_path = relative_path.replace(os.sep, '/')
            
            # Create alt text from filename
            alt_text = file_path.stem.replace('_', ' ').replace('-', ' ').title()
            
            images.append((relative_path, alt_text))
    
    return images


def find_collections(art_folder: Path) -> Dict[str, List[Tuple[str, str]]]:
    """
    Find all images organized by collection (subfolder).
    Returns dict: {collection_name: [(relative_path, alt_text), ...]}
    """
    collections = defaultdict(list)
    
    if not art_folder.exists():
        print(f"Error: Art folder '{art_folder}' does not exist!")
        return collections
    
    # Look for subdirectories in art folder
    for subfolder in sorted(art_folder.iterdir()):
        if subfolder.is_dir():
            collection_name = subfolder.name
            
            # Find all images in this collection
            for file_path in sorted(subfolder.rglob('*')):
                if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                    # Get path relative to collections.html location (pages/)
                    relative_path = os.path.relpath(file_path, Path(COLLECTIONS_HTML).parent)
                    relative_path = relative_path.replace(os.sep, '/')
                    
                    # Create alt text from filename
                    alt_text = file_path.stem.replace('_', ' ').replace('-', ' ').title()
                    
                    collections[collection_name].append((relative_path, alt_text))
    
    return dict(collections)


def generate_gallery_html(images: List[Tuple[str, str]]) -> str:
    """Generate the HTML for gallery grid items."""
    html_items = []
    
    for img_path, alt_text in images:
        item_html = f'''        <div class="gallery-grid-item">
            <img src="{img_path}" alt="{alt_text}">
        </div>'''
        html_items.append(item_html)
    
    return '\n'.join(html_items)


def generate_collections_html(collections: Dict[str, List[Tuple[str, str]]]) -> str:
    """Generate the HTML for collection carousels."""
    html_sections = []
    
    for collection_name, images in collections.items():
        if not images:
            continue
            
        # Format collection name for display (title case with spaces)
        display_name = collection_name.replace('_', ' ').replace('-', ' ').title()
        
        # Generate cards for this collection
        cards_html = []
        for img_path, alt_text in images:
            card_html = f'''                        <div class="collection-card">
                            <div class="card-image">
                                <img src="{img_path}" alt="{alt_text}">
                            </div>
                        </div>'''
            cards_html.append(card_html)
        
        # Build complete collection section
        section_html = f'''        <!-- Collection: {collection_name} -->
        <section class="collection-section" data-collection="{collection_name}">
            <div class="collection-header">
                <h2>{display_name}</h2>
            </div>
            <div class="collection-carousel-container">
                <button class="carousel-btn prev" data-carousel="{collection_name}">‹</button>
                <div class="collection-carousel" id="carousel-{collection_name}">
                    <div class="carousel-track">
{chr(10).join(cards_html)}
                    </div>
                </div>
                <button class="carousel-btn next" data-carousel="{collection_name}">›</button>
            </div>
        </section>'''
        
        html_sections.append(section_html)
    
    return '\n'.join(html_sections)


def update_file_content(file_path: Path, new_content: str, start_marker: str, end_marker: str) -> bool:
    """Update a file with new content between markers."""
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist!")
        return False
    
    # Read current file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if markers exist
    if start_marker not in content or end_marker not in content:
        print(f"Error: Could not find markers in {file_path}")
        print(f"Make sure the file contains both:")
        print(f"  {start_marker}")
        print(f"  {end_marker}")
        return False
    
    # Split content and replace middle section
    start_idx = content.find(start_marker) + len(start_marker)
    end_idx = content.find(end_marker)
    
    new_file_content = (
        content[:start_idx] + 
        '\n' + new_content + '\n        ' +
        content[end_idx:]
    )
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_file_content)
    
    return True


def main():
    """Main execution function."""
    print("🎨 Portfolio Content Updater")
    print("=" * 50)
    
    # Get script directory and set up paths
    script_dir = Path(__file__).parent
    art_folder = script_dir / ART_FOLDER
    gallery_file = script_dir / GALLERY_HTML
    collections_file = script_dir / COLLECTIONS_HTML
    
    print(f"📁 Scanning art folder: {art_folder}")
    
    # === UPDATE GALLERY ===
    print("\n📸 UPDATING GALLERY...")
    all_images = find_all_images(art_folder)
    
    if not all_images:
        print("⚠️  No images found for gallery!")
    else:
        print(f"✅ Found {len(all_images)} total images")
        print("🔨 Generating gallery HTML...")
        gallery_html = generate_gallery_html(all_images)
        
        print(f"📝 Updating {gallery_file}...")
        if update_file_content(gallery_file, gallery_html, GALLERY_START, GALLERY_END):
            print(f"✅ Gallery updated with {len(all_images)} images")
        else:
            print("❌ Failed to update gallery page")
    
    # === UPDATE COLLECTIONS ===
    print("\n📚 UPDATING COLLECTIONS...")
    collections = find_collections(art_folder)
    
    if not collections:
        print("⚠️  No collections found (no subfolders with images)")
    else:
        total_collection_images = sum(len(imgs) for imgs in collections.values())
        print(f"✅ Found {len(collections)} collections with {total_collection_images} images:")
        for name, images in collections.items():
            print(f"   • {name}: {len(images)} images")
        
        print("🔨 Generating collections HTML...")
        collections_html = generate_collections_html(collections)
        
        print(f"📝 Updating {collections_file}...")
        if update_file_content(collections_file, collections_html, COLLECTIONS_START, COLLECTIONS_END):
            print(f"✅ Collections updated with {len(collections)} collections")
        else:
            print("❌ Failed to update collections page")
    
    print("\n" + "=" * 50)
    print("✨ Update complete!")


if __name__ == "__main__":
    main()
