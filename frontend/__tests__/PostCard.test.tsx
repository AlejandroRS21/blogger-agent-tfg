import React from 'react';
import { render, screen } from '@testing-library/react';
import PostCard from '../app/components/PostCard';
import { PostListItem } from '../app/types/post';

const mockPost: PostListItem = {
  id: '1',
  slug: 'test-slug',
  title: 'Test Post Title',
  excerpt: 'This is a test excerpt.',
  date: '2026-04-03T10:00:00Z',
  content: 'Content here'
};

describe('PostCard', () => {
  it('renders post details correctly', () => {
    render(<PostCard post={mockPost} />);

    // Title and excerpt
    expect(screen.getByText('Test Post Title')).toBeInTheDocument();
    expect(screen.getByText('This is a test excerpt.')).toBeInTheDocument();

    // Link should point to the correct slug
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/posts/test-slug');
  });
});