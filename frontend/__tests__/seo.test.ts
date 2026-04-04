import { generateMetadata } from '../app/posts/[slug]/page';
import { getPostBySlug } from '../app/lib/api';

jest.mock('../app/lib/api');

describe('SEO Metadata Generation', () => {
    it('generates correct metadata for a valid post', async () => {
        const mockPost = {
            slug: 'test-post',
            title: 'Test Post Title',
            excerpt: 'This is a test excerpt',
            content: '<p>Content</p>'
        };
        (getPostBySlug as jest.Mock).mockResolvedValue(mockPost);

        const metadata = await generateMetadata({ params: { slug: 'test-post' } });

        expect(metadata.title).toBe('Test Post Title | Blogger Agent');
        expect(metadata.description).toBe('This is a test excerpt');
        expect(metadata.openGraph?.title).toBe('Test Post Title');
        expect(metadata.openGraph?.description).toBe('This is a test excerpt');
    });

    it('uses fallback metadata when post is missing', async () => {
        (getPostBySlug as jest.Mock).mockResolvedValue(null);

        const metadata = await generateMetadata({ params: { slug: 'missing-post' } });

        expect(metadata.title).toBe('Post Not Found | Blogger Agent');
    });
});
