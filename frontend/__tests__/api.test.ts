import { getAllPosts, getPostBySlug } from '../app/lib/api';

describe('API functions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    global.fetch = jest.fn();
  });

  describe('getAllPosts', () => {
    it('returns an empty array when posts.json does not exist', async () => {
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        status: 404,
        statusText: 'Not Found'
      });

      const posts = await getAllPosts();
      expect(posts).toEqual([]);
    });

    it('returns posts from posts array', async () => {
      const mockData = [{ slug: 'post-1', title: 'Post 1' }];
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: async () => mockData
      });

      const posts = await getAllPosts();
      expect(posts).toHaveLength(1);
      expect(posts[0].slug).toBe('post-1');
    });
  });

  describe('getPostBySlug', () => {
    it('loads json fallback successfully', async () => {
      const mockPost = { slug: 'post-test', title: 'Test', content: 'test content' };
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: true,
        json: async () => mockPost
      });

      const post = await getPostBySlug('post-test');
      expect(post?.title).toBe('Test');
    });

    it('loads HTML fallback successfully when JSON fails', async () => {
      // JSON fetch fails (404)
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404
      });
      // HTML fetch succeeds
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        text: async () => '<h1>Title</h1>'
      });

      const post = await getPostBySlug('post-from-html');
      expect(post?.title).toBe('post from html');
      expect(post?.content).toBe('<h1>Title</h1>');
    });

    it('returns null if neither JSON nor HTML are found', async () => {
      (global.fetch as jest.Mock).mockResolvedValue({
        ok: false,
        status: 404
      });
      
      const post = await getPostBySlug('missing');
      expect(post).toBeNull();
    });
  });
});
