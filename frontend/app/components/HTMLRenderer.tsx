import React from 'react';
import DOMPurify from 'isomorphic-dompurify';

interface Props {
  htmlContent: string;
}

export default function HTMLRenderer({ htmlContent }: Props) {
  // Synchronous sanitization avoiding useEffect, since isomorphic-dompurify supports SSR
  const clean = DOMPurify.sanitize(htmlContent, {
    ALLOWED_TAGS: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
      'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
      'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe', 'img', 'span'
    ],
    ALLOWED_ATTR: ['href', 'name', 'target', 'src', 'alt', 'title', 'class', 'id', 'width', 'height', 'allow', 'allowfullscreen']
  });

  return (
    <div 
      className="prose prose-neutral dark:prose-invert max-w-none" 
      dangerouslySetInnerHTML={{ __html: clean }} 
    />
  );
}
