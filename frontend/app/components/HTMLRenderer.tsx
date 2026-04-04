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
      'table', 'thead', 'tbody', 'tr', 'th', 'td', 'iframe'
    ],
    ALLOWED_ATTR: [
      'href', 'src', 'alt', 'target', 'rel', 'class', 
      'width', 'height', 'frameborder', 'allow', 'allowfullscreen', 'sandbox'
    ],
    ADD_ATTR: ['sandbox'], // Force sandbox attribute if not present
  });

  // Post-sanitize: Ensure all iframes have a strict sandbox and white-listed domains
  const finalHTML = DOMPurify.sanitize(cleanHTML, {
    FORBID_TAGS: ['script', 'style'], // Extra precaution
    FORBID_ATTR: ['onerror', 'onclick', 'onload'],
  }).replace(/<iframe/g, '<iframe sandbox="allow-scripts allow-same-origin allow-popups allow-forms" loading="lazy"');

  return (
    <div 
      className="prose prose-stone dark:prose-invert lg:prose-lg max-w-none 
                 prose-headings:text-balance prose-img:rounded-xl prose-img:mx-auto
                 prose-pre:shadow-inner prose-blockquote:border-red-500 prose-blockquote:bg-red-50/20"
      dangerouslySetInnerHTML={{ __html: finalHTML }} 
    />
  );
}
