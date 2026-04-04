import { auditPostHTML } from '../app/lib/postAudit';

describe('Post Integrity Audit (T022)', () => {
    it('should pass for clean, balanced, and safe HTML', async () => {
        const cleanHTML = `
            <article>
                <h1>Test Post</h1>
                <p>Simple content with <strong>bold</strong> text.</p>
                <ul>
                    <li>Item 1</li>
                </ul>
                <iframe src="https://youtube.com" sandbox="allow-scripts" loading="lazy"></iframe>
            </article>
        `;
        const result = await auditPostHTML('clean-post', cleanHTML);
        expect(result.score).toBe(100);
        expect(result.findings).toHaveLength(0);
    });

    it('should detect unbalanced div tags', async () => {
        const brokenHTML = `
            <div>
                <p>Broken content
            </div>
            <div>Missing closing div
        `;
        const result = await auditPostHTML('broken-div', brokenHTML);
        expect(result.findings).toContain('UNBALANCED_TAG: <div> (Opened: 2, Closed: 1)');
        expect(result.score).toBeLessThan(100);
    });

    it('should detect unsafe iframes without sandbox', async () => {
        const unsafeHTML = `
            <iframe src="https://malicious.site"></iframe>
        `;
        const result = await auditPostHTML('unsafe-iframe', unsafeHTML);
        expect(result.findings).toContain('UNSAFE_IFRAME: Missing sandbox attribute in iframe');
        expect(result.score).toBeLessThan(100);
    });

    it('should detect potential mobile overflow from unstyled tables', async () => {
        const tableHTML = `
            <table>
                <tr><td>Data</td></tr>
            </table>
        `;
        // Score should be slightly lower due to responsiveness risk
        const result = await auditPostHTML('responsive-risk', tableHTML);
        expect(result.findings).toContain('RESPONSIVE_RISK: Table detected without explicit responsive container');
        expect(result.score).toBe(90);
    });
});
