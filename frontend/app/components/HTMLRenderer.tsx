'use client';

import React, { useEffect, useState } from 'react';
import DOMPurify from 'isomorphic-dompurify';

interface Props {
  htmlContent: string;
}

export default function HTMLRenderer({ htmlContent }: Props) {
  const [sanitizedHtml, setSanitizedHtml] = useState('');

  useEffect(() => {
    // Sanitize HTML on the client to avoid hydration mismatches,
    // though isomorphic-dompurify can run on the server too.
    // It's safer to ensure the exact same output on the server and client.
    const clean = DOMPurify.sanitize(htmlContent, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'p', 'a', 'ul', 'ol',
        'nl', 'li', 'b', 'i', 'strong', 'em', 'strike', 'code', 'hr', 'br', 'div',
        'table', 'thead', 'caption', 'tbody', 'tr', 'th', 'td', 'pre', 'iframe', 'img', 'span'
      ],
      ALLOWED_ATTR: ['href', 'name', 'target', 'src', 'alt', 'title', 'class', 'id', 'width', 'height', 'allow', 'allowfullscreen']
    });
    setSanitizedHtml(clean);
  }, [htmlContent]);

  // Initial SSR generic render to avoid hydration mismatch
  if (!sanitizedHtml) {
    return <div className="prose prose-neutral dark:prose-invert max-w-none" dangerouslySetInnerHTML={{ __html: htmlContent }} />;
  }

  return (
    <div 
      className="prose prose-neutral dark:prose-invert max-w-none" 
      dangerouslySetInnerHTML={{ __html: sanitizedHtml }} 
    />
  );
}
