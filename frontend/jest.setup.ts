import '@testing-library/jest-dom';

// Global mock for isomorphic-dompurify due to transformation issues with its deep dependencies in Jest
jest.mock('isomorphic-dompurify', () => ({
  sanitize: (html: string) => (html || '').replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
}));