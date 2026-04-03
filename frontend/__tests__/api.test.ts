import { getAllPosts, getPostBySlug } from '../app/lib/api';
import fs from 'fs/promises';

jest.mock('fs/promises');

describe('API functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getAllPosts', () => {
    it('returns an empty array when posts.json does not exist', async () => {
      const error = new Error('ENOENT') as any;
      error.code = 'ENOENT';
      (fs.readFile as jest.Mock).mockRejectedValue(error);

      const posts = await getAllPosts();
      expect(posts).toEqual([]);
    });

    it('returns posts from posts array', async () => {
      const mockData = { posts: [{ slug: 'post-1', title: 'Post 1' }] };
      (fs.readFile as jest.Mock).mockResolvedValue(JSON.stringify(mockData));

      const posts = await getAllPosts();
      expect(posts).toHaveLength(1);
      expect(posts[0].slug).toBe('post-1');
    });
  });

  describe('getPostBySlug', () => {
    it('loads json fallback successfully', async () => {
      const mockPost = { slug: 'post-test', title: 'Test', content: 'test content' };
      (fs.readFile as jest.Mock).mockResolvedValueOnce(JSON.stringify(mockPost));

      const post = await getPostBySlug('post-test');
      expect(post?.title).toBe('Test');
    });

    it('loads HTML fallback successfully when JSON fails', async () => {
      // JSON fetch fails
      (fs.readFile as jest.Mock).mockRejectedValueOnce(new Error('ENOENT'));
      // HTML fetch succeeds
      (fs.readFile as jest.Mock).mockResolvedValueOnce('<h1>Title</h1>');

      const post = await getPostBySlug('post-from-html');
      expect(post?.title).toBe('post from html');
      expect(post?.content).toBe('<h1>Title</h1>');
    });

    it('returns null if neither JSON nor HTML are found', async () => {
      (fs.readFile as jest.Mock).mockRejectedValue(new Error('ENOENT'));
      
      const post = await getPostBySlug('missing');
      expect(post).toBeNull();
    });
  });
});
