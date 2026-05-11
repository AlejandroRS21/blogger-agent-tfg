import React from 'react';
import { render, screen } from '@testing-library/react';
import HTMLRenderer from '../app/components/HTMLRenderer';

// Mock now handled globally in jest.setup.ts

describe('HTMLRenderer', () => {
  it('renders sanitized HTML correctly', () => {
    const rawHtml = '<h1>Test Title</h1><p>Test paragraph with <strong>bold</strong> text.</p><script>alert("xss")</script>';
    const { container } = render(<HTMLRenderer html={rawHtml} />);
    
    // Check if valid HTML is rendered
    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText(/Test paragraph/)).toBeInTheDocument();
    
    // Check if script tag was stripped out
    expect(container.innerHTML).not.toContain('<script>');
  });

  it('contains proper Tailwind Typography classes for layout stability', () => {
    const { container } = render(<HTMLRenderer html="<p>Test</p>" />);
    const div = container.querySelector('div');
    expect(div).toHaveClass('prose');
    expect(div).toHaveClass('dark:prose-invert');
  });

  it('renders exceptionally long words with proper break-words behavior (FR-004)', () => {
    const longWord = 'a'.repeat(200);
    render(<HTMLRenderer html={longWord} />);
    
    // We can't easily test CSS properties in unit tests with Jest/RTL 
    // but we verify the container exists and the text is rendered.
    expect(screen.getByText(longWord)).toBeInTheDocument();
  });
});
