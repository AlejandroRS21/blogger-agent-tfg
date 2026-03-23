"""
HTMLBuilder Agent - Converts Markdown content to structured HTML/JSX.

This agent takes generated blog content in Markdown format and converts it
to clean, semantic HTML/JSX ready for Next.js integration.
"""

import re
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

try:
    import markdown
    from markdown.extensions import fenced_code, tables, toc, codehilite
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from ..llm import create_llm_provider, LLMProvider
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


logger = logging.getLogger(__name__)


@dataclass
class HTMLOutput:
    """Structured HTML output from HTMLBuilder."""
    html: str
    full_page: str
    meta_title: str
    meta_description: str
    meta_keywords: List[str]
    reading_time: int  # minutes
    word_count: int
    headings: List[Dict[str, str]]  # [{"level": "h2", "text": "...", "id": "..."}]


class HTMLBuilder:
    """
    Agent for converting Markdown content to HTML/JSX.
    
    Features:
    - Markdown to HTML conversion
    - Complete HTML5 page generation
    - Semantic HTML structure
    - Image placeholder integration
    - Meta tags generation
    - Table of contents extraction
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        provider: str = "auto"
    ):
        """
        Initialize HTMLBuilder agent.
        
        Args:
            api_key: API key for LLM provider (optional)
            model: Model to use. If None, uses provider defaults.
            provider: "huggingface", "openai", or "auto"
        """
        self.model = model
        self.provider_name = provider
        
        if LLM_AVAILABLE:
            try:
                self.llm = create_llm_provider(
                    provider=provider,
                    api_key=api_key,
                    model=model,
                    temperature=0.7,
                    max_tokens=200
                )
                logger.info(f"HTMLBuilder initialized with LLM provider: {provider}")
            except Exception as e:
                logger.warning(f"Failed to initialize LLM provider: {e}. Using fallback mode.")
                self.llm = None
        else:
            self.llm = None
            logger.info("HTMLBuilder initialized in fallback mode")
        
        if not MARKDOWN_AVAILABLE:
            logger.warning("python-markdown not installed. Using basic conversion.")
    
    def build(
        self,
        content: str,
        topic: str,
        images: Optional[List[Dict]] = None,
        style_profile: Optional[Dict] = None
    ) -> HTMLOutput:
        """
        Convert Markdown content to structured HTML/JSX.
        
        Args:
            content: Markdown content to convert
            topic: Blog post topic (for meta tags)
            images: List of image placements from ImageSelectorAgent
            style_profile: Style profile from StyleAnalyzer (optional)
            
        Returns:
            HTMLOutput with html, full_page, and metadata
        """
        logger.info(f"Building HTML/JSX for topic: {topic}")
        
        # Convert Markdown to HTML
        html = self._markdown_to_html(content)
        
        # Insert image placeholders
        if images:
            html = self._insert_image_placeholders(html, images)
        
        # Extract headings for TOC
        headings = self._extract_headings(html)
        
        # Calculate reading time and word count
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)  # ~200 words per minute
        
        # Generate meta tags
        meta_title = self._generate_meta_title(topic, content)
        meta_description = self._generate_meta_description(content)
        meta_keywords = self._extract_keywords_for_meta(content, style_profile)
        
        # Generate full HTML page
        full_page = self.generate_full_html_page(
            html_content=html,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            reading_time=reading_time,
            word_count=word_count
        )
        
        output = HTMLOutput(
            html=html,
            full_page=full_page,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            reading_time=reading_time,
            word_count=word_count,
            headings=headings
        )
        
        logger.info(f"HTML build complete: {word_count} words, {len(headings)} headings")
        return output
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert Markdown to HTML."""
        if MARKDOWN_AVAILABLE:
            # Use python-markdown for proper conversion
            md = markdown.Markdown(extensions=[
                'fenced_code',
                'tables',
                'toc',
                'codehilite',
                'nl2br'
            ])
            html = md.convert(markdown_content)
        else:
            # Fallback: basic conversion
            html = self._basic_markdown_to_html(markdown_content)
        
        # Wrap in article tag
        html = f'<article class="blog-post">\n{html}\n</article>'
        
        return html
    
    def _basic_markdown_to_html(self, content: str) -> str:
        """Basic Markdown to HTML conversion (fallback)."""
        lines = content.split('\n')
        html_lines = []
        in_code_block = False
        in_list = False
        
        for line in lines:
            # Code blocks
            if line.startswith('```'):
                if in_code_block:
                    html_lines.append('</code></pre>')
                    in_code_block = False
                else:
                    lang = line[3:].strip() or 'text'
                    html_lines.append(f'<pre><code class="language-{lang}">')
                    in_code_block = True
                continue
            
            if in_code_block:
                html_lines.append(line)
                continue
            
            # Headings
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('#### '):
                html_lines.append(f'<h4>{line[5:]}</h4>')
            
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                html_lines.append(f'<li>{line[2:]}</li>')
            elif re.match(r'^\d+\. ', line) is not None:
                if not in_list:
                    html_lines.append('<ol>')
                    in_list = True
                html_lines.append(f'<li>{line[line.index(".")+2:]}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                
                # Paragraphs
                if line.strip():
                    # Bold and italic
                    line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
                    line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
                    line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
                    html_lines.append(f'<p>{line}</p>')
        
        if in_list:
            html_lines.append('</ul>')
        
        return '\n'.join(html_lines)
    
    def _insert_image_placeholders(self, html: str, images: List[Dict]) -> str:
        """Insert image placeholders into HTML."""
        for i, image in enumerate(images):
            position = image.get('position', 'section-1')
            prompt = image.get('prompt', '')
            alt_text = image.get('alt_text', 'Blog image')
            
            # Create image placeholder
            image_url = image.get('url') or "/api/placeholder/800/400"
            
            placeholder = f'''
<figure class="blog-image" data-position="{position}">
  <img 
    src="{image_url}" 
    alt="{alt_text}"
    data-image-prompt="{prompt}"
    loading="lazy"
  />
  <figcaption>{alt_text}</figcaption>
</figure>
'''
            
            # Insert after specific heading or at beginning
            if position == 'header':
                # Insert at the beginning of article
                html = html.replace('<article class="blog-post">', 
                                  f'<article class="blog-post">{placeholder}')
            elif position.startswith('section-'):
                # Insert after specific h2
                section_num = position.split('-')[1]
                h2_pattern = r'(<h2[^>]*>.*?</h2>)'
                matches = list(re.finditer(h2_pattern, html))
                
                if matches and int(section_num) <= len(matches):
                    insert_pos = matches[int(section_num) - 1].end()
                    html = html[:insert_pos] + placeholder + html[insert_pos:]
        
        return html
    
    
    def generate_full_html_page(
        self,
        html_content: str,
        meta_title: str,
        meta_description: str,
        meta_keywords: List[str],
        reading_time: int,
        word_count: int
    ) -> str:
        """Generate a complete HTML5 page."""
        return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title}</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{', '.join(meta_keywords)}">
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header class="site-header">
        <h1><a href="../index.html">Blogger Agent</a></h1>
    </header>
    <main class="container">
        <article class="post">
            <header class="post-header">
                <h1 class="post-title">{meta_title}</h1>
                <div class="post-meta">
                    <span>{reading_time} min lectura</span> • <span>{word_count} palabras</span>
                </div>
            </header>
            <div class="post-content">
                {html_content}
            </div>
        </article>
    </main>
    <footer>
        <p>&copy; 2026 Blogger Agent TFG</p>
    </footer>
</body>
</html>'''
    
    def _extract_headings(self, html: str) -> List[Dict[str, str]]:
        """Extract headings from HTML for table of contents."""
        headings = []
        
        # Find all h2 and h3 tags
        heading_pattern = r'<(h[23])(?:\s+id="([^"]*)")?[^>]*>(.*?)</\1>'
        matches = re.finditer(heading_pattern, html, re.IGNORECASE)
        
        for match in matches:
            level = match.group(1)
            heading_id = match.group(2) or self._slugify(match.group(3))
            text = re.sub(r'<[^>]+>', '', match.group(3))  # Strip tags
            
            headings.append({
                'level': level,
                'id': heading_id,
                'text': text
            })
        
        return headings
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug for IDs."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Convert to lowercase and replace spaces with hyphens
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    def _generate_meta_title(self, topic: str, content: str) -> str:
        """Generate SEO-optimized meta title."""
        # LLM not needed for title extraction, use simple parsing
        # Extract first heading as title
        first_h1 = re.search(r'#\s+(.+)', content)
        if first_h1:
            return first_h1.group(1).strip()
        
        # Fallback to topic
        return topic
    
    def _generate_meta_description(self, content: str) -> str:
        """Generate meta description from content."""
        if self.llm and self.llm.is_available():
            try:
                messages = self.llm.create_messages(
                    system_prompt="Generate a concise meta description (150-160 characters) for SEO from the following blog content.",
                    user_prompt=content[:1000]
                )
                
                response = self.llm.chat_completion(
                    messages,
                    max_tokens=100
                )
                
                description = response.content.strip()
                # Ensure it's within character limit
                if len(description) > 160:
                    description = description[:157] + "..."
                
                return description
                
            except Exception as e:
                logger.error(f"Error generating meta description: {e}")
        
        # Fallback: use first paragraph
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if not para.startswith('#') and len(para) > 50:
                # Clean markdown
                clean = re.sub(r'[#*`]', '', para)
                if len(clean) > 160:
                    clean = clean[:157] + "..."
                return clean.strip()
        
        return "Artículo de blog sobre tecnología e innovación."
    
    def _extract_keywords_for_meta(
        self,
        content: str,
        style_profile: Optional[Dict] = None
    ) -> List[str]:
        """Extract keywords for meta tags."""
        # If we have style profile with keywords, use those
        if style_profile and 'keywords' in style_profile:
            return style_profile['keywords'][:10]
        
        # Otherwise, extract from content
        # Remove markdown symbols
        clean_content = re.sub(r'[#*`_]', '', content)
        
        # Simple keyword extraction: find most common meaningful words
        words = clean_content.lower().split()
        
        # Filter out common words (basic stopwords)
        stopwords = {'el', 'la', 'de', 'en', 'y', 'a', 'que', 'es', 'por', 'un', 
                    'una', 'con', 'para', 'como', 'del', 'los', 'las', 'se', 'su'}
        
        filtered_words = [w for w in words if len(w) > 4 and w not in stopwords]
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(filtered_words)
        
        # Get top 10
        keywords = [word for word, _ in word_freq.most_common(10)]
        
        return keywords if keywords else ["blog", "tecnología", "innovación"]
    



if __name__ == '__main__':
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    sample_markdown = """# Mi Primer Post

## Introducción

Este es un **ejemplo** de contenido Markdown que será convertido a HTML.

## Sección Principal

Aquí hay algunos puntos importantes:

- Punto uno
- Punto dos
- Punto tres

### Subsección

Y un poco de código:

```python
def hello_world():
    print("Hello, World!")
```

## Conclusión

Este es el final del post.
"""
    
    builder = HTMLBuilder()
    output = builder.build(
        content=sample_markdown,
        topic="Mi Primer Post",
        images=[
            {"position": "header", "prompt": "Header image", "alt_text": "Header"},
            {"position": "section-1", "prompt": "Section 1 image", "alt_text": "Section 1"}
        ]
    )
    
    print(f"Meta Title: {output.meta_title}")
    print(f"Meta Description: {output.meta_description}")
    print(f"Reading Time: {output.reading_time} min")
    print(f"Headings: {len(output.headings)}")
    print(f"\nHTML Preview:")
    print(output.html[:500] + "...")
