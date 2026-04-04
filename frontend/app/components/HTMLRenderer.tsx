import DOMPurify from 'isomorphic-dompurify';

interface HTMLRendererProps {
  html: string;
}

export default function HTMLRenderer({ html }: HTMLRendererProps) {
  // Configure DOMPurify to allow standard HTML and focus on safety
  const cleanHTML = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'strong', 'em', 'i', 'b',
      'ul', 'ol', 'li', 'br', 'hr', 'blockquote', 'code', 'pre', 'a', 'img',
      'table', 'thead', 'tbody', 'tr', 'th', 'td'
    ],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'target', 'rel', 'class'],
  });

  return (
    <div 
      className="prose prose-stone dark:prose-invert lg:prose-lg max-w-none 
                 prose-headings:text-balance prose-img:rounded-xl prose-img:mx-auto
                 prose-pre:shadow-inner prose-blockquote:border-red-500 prose-blockquote:bg-red-50/20"
      dangerouslySetInnerHTML={{ __html: cleanHTML }} 
    />
  );
}
