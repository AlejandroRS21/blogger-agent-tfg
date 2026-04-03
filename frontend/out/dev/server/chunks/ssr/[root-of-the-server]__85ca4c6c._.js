module.exports = [
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/favicon.ico.mjs { IMAGE => \"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/favicon.ico (static in ecmascript, tag client)\" } [app-rsc] (structured image object, ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/favicon.ico.mjs { IMAGE => \"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/favicon.ico (static in ecmascript, tag client)\" } [app-rsc] (structured image object, ecmascript)"));
}),
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/layout.tsx [app-rsc] (ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/layout.tsx [app-rsc] (ecmascript)"));
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/not-found.tsx [app-rsc] (ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/not-found.tsx [app-rsc] (ecmascript)"));
}),
"[externals]/fs/promises [external] (fs/promises, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("fs/promises", () => require("fs/promises"));

module.exports = mod;
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/lib/api.ts [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "getAllPosts",
    ()=>getAllPosts,
    "getPostBySlug",
    ()=>getPostBySlug
]);
var __TURBOPACK__imported__module__$5b$externals$5d2f$fs$2f$promises__$5b$external$5d$__$28$fs$2f$promises$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/fs/promises [external] (fs/promises, cjs)");
var __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__ = __turbopack_context__.i("[externals]/path [external] (path, cjs)");
;
;
const DOCS_DIR = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(process.cwd(), '..', 'docs');
const POSTS_JSON_PATH = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(DOCS_DIR, 'posts.json');
const POSTS_DIR = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(DOCS_DIR, 'posts');
async function getAllPosts() {
    try {
        const fileContents = await __TURBOPACK__imported__module__$5b$externals$5d2f$fs$2f$promises__$5b$external$5d$__$28$fs$2f$promises$2c$__cjs$29$__["default"].readFile(POSTS_JSON_PATH, 'utf8');
        const data = JSON.parse(fileContents);
        let rawPosts = [];
        // Some formats might wrap in { posts: [...] }, or just return an array.
        if (Array.isArray(data)) {
            rawPosts = data;
        } else if (data.posts && Array.isArray(data.posts)) {
            rawPosts = data.posts;
        }
        // Normalize data to ensure `slug` and `excerpt` exist
        return rawPosts.map((item)=>{
            let title = item.title || 'Sin Título';
            let excerpt = item.excerpt || item.description || '';
            // Handle AI encoded JSON in titles
            if (title.includes('topic_out') && title.startsWith('{')) {
                try {
                    const cleaned = title.replace(/'/g, '"');
                    const parsed = JSON.parse(cleaned);
                    title = parsed.topic_out || parsed.title || title;
                } catch (e) {
                    console.warn('[api] Failed to parse JSON title', e);
                }
            }
            // Handle AI encoded markdown in excerpts
            excerpt = excerpt.replace(/```markdown\s*/g, '').replace(/```\s*/g, '').replace(/^#+\s+.*/g, '').trim();
            return {
                slug: item.slug || item.id || '',
                title,
                date: item.date || new Date().toISOString(),
                excerpt: excerpt.substring(0, 200) + (excerpt.length > 200 ? '...' : '')
            };
        }).filter((post)=>post.slug !== '');
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.warn(`[api] posts.json not found at ${POSTS_JSON_PATH}. Returning empty list.`);
            return [];
        }
        console.error('[api] Failed to read posts.json:', error);
        return [];
    }
}
async function getPostBySlug(slug) {
    // Prevent directory traversal attacks
    const safeSlug = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].basename(slug);
    const jsonPath = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(POSTS_DIR, `${safeSlug}.json`);
    const htmlPath = __TURBOPACK__imported__module__$5b$externals$5d2f$path__$5b$external$5d$__$28$path$2c$__cjs$29$__["default"].join(POSTS_DIR, `${safeSlug}.html`);
    try {
        // Attempt JSON first
        const jsonContent = await __TURBOPACK__imported__module__$5b$externals$5d2f$fs$2f$promises__$5b$external$5d$__$28$fs$2f$promises$2c$__cjs$29$__["default"].readFile(jsonPath, 'utf8');
        const data = JSON.parse(jsonContent);
        return {
            title: data.title || safeSlug,
            content: data.html_code || data.content || '',
            metadata: data.metadata || {},
            date: data.date || data.metadata?.date,
            excerpt: data.description || data.excerpt
        };
    } catch  {
        console.warn(`[api] Post JSON for slug ${safeSlug} not found. Trying HTML...`);
        try {
            // Fallback to HTML if available
            const htmlContent = await __TURBOPACK__imported__module__$5b$externals$5d2f$fs$2f$promises__$5b$external$5d$__$28$fs$2f$promises$2c$__cjs$29$__["default"].readFile(htmlPath, 'utf8');
            // Fallback matching logic
            return {
                title: safeSlug.replace(/-/g, ' '),
                content: htmlContent
            };
        } catch  {
            console.error(`[api] Post resource not found for ${safeSlug}`);
            return null;
        }
    }
}
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/HTMLRenderer.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>HTMLRenderer
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$isomorphic$2d$dompurify$2f$dist$2f$index$2e$mjs__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/isomorphic-dompurify/dist/index.mjs [app-rsc] (ecmascript)");
;
;
function HTMLRenderer({ htmlContent }) {
    // Synchronous sanitization avoiding useEffect, since isomorphic-dompurify supports SSR
    const clean = __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$isomorphic$2d$dompurify$2f$dist$2f$index$2e$mjs__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"].sanitize(htmlContent, {
        ALLOWED_TAGS: [
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'blockquote',
            'p',
            'a',
            'ul',
            'ol',
            'nl',
            'li',
            'b',
            'i',
            'strong',
            'em',
            'strike',
            'code',
            'hr',
            'br',
            'div',
            'table',
            'thead',
            'caption',
            'tbody',
            'tr',
            'th',
            'td',
            'pre',
            'iframe',
            'img',
            'span'
        ],
        ALLOWED_ATTR: [
            'href',
            'name',
            'target',
            'src',
            'alt',
            'title',
            'class',
            'id',
            'width',
            'height',
            'allow',
            'allowfullscreen'
        ]
    });
    // Cleanup for AI-generated JSON string titles in internal links
    const polishedContent = clean.replace(/>\{'keywords':.*'topic_out':\s*'([^']*)'\}<\/a>/g, '>$1</a>');
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "prose prose-neutral dark:prose-invert max-w-none",
        dangerouslySetInnerHTML: {
            __html: polishedContent
        }
    }, void 0, false, {
        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/HTMLRenderer.tsx",
        lineNumber: 23,
        columnNumber: 5
    }, this);
}
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>PostMeta
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
;
function PostMeta({ metadata }) {
    if (!metadata) return null;
    const entries = Object.entries(metadata).filter(([_, value])=>value !== undefined && value !== null);
    if (entries.length === 0) return null;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        className: "my-12 overflow-hidden border border-zinc-100 dark:border-zinc-800 rounded-xl bg-zinc-50/50 dark:bg-zinc-900/30",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "px-5 py-3 border-b border-zinc-100 dark:border-zinc-800 bg-zinc-100/50 dark:bg-zinc-800/50",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h4", {
                    className: "text-[11px] font-black uppercase tracking-[0.2em] text-secondary",
                    children: "Métricas de Generación IA"
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
                    lineNumber: 16,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
                lineNumber: 15,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-px bg-zinc-100 dark:bg-zinc-800",
                children: entries.map(([key, value])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "bg-white dark:bg-zinc-900 p-4 flex flex-col gap-1",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-[10px] font-bold uppercase tracking-wider text-secondary opacity-70",
                                children: key.replace(/_/g, ' ')
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
                                lineNumber: 23,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "font-mono text-sm font-semibold text-primary truncate",
                                children: typeof value === 'number' ? value.toFixed(2) : String(value)
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
                                lineNumber: 26,
                                columnNumber: 13
                            }, this)
                        ]
                    }, key, true, {
                        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
                        lineNumber: 22,
                        columnNumber: 11
                    }, this))
            }, void 0, false, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
                lineNumber: 20,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx",
        lineNumber: 14,
        columnNumber: 5
    }, this);
}
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>PostPage,
    "dynamic",
    ()=>dynamic,
    "dynamicParams",
    ()=>dynamicParams,
    "generateMetadata",
    ()=>generateMetadata,
    "generateStaticParams",
    ()=>generateStaticParams
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$api$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__$3c$locals$3e$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/api/navigation.react-server.js [app-rsc] (ecmascript) <locals>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$components$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/client/components/navigation.react-server.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$lib$2f$api$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/lib/api.ts [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$components$2f$HTMLRenderer$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/HTMLRenderer.tsx [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$components$2f$PostMeta$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostMeta.tsx [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/client/app-dir/link.react-server.js [app-rsc] (ecmascript)");
;
;
;
;
;
;
const dynamic = 'force-static';
const dynamicParams = false;
async function generateMetadata(props) {
    const params = await props.params;
    const post = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$lib$2f$api$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getPostBySlug"])(params.slug);
    if (!post) return {
        title: 'Post no encontrado'
    };
    return {
        title: `${post.title} | AI Blogger`,
        description: post.excerpt || `Lee sobre ${post.title} en nuestro blog generado por IA.`,
        openGraph: {
            title: post.title,
            description: post.excerpt,
            type: 'article',
            publishedTime: post.date
        }
    };
}
async function generateStaticParams() {
    const posts = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$lib$2f$api$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getAllPosts"])();
    return posts.map((post)=>({
            slug: post.slug
        }));
}
async function PostPage(props) {
    const params = await props.params;
    const post = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$lib$2f$api$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getPostBySlug"])(params.slug);
    if (!post) {
        (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$components$2f$navigation$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["notFound"])();
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
        className: "py-10 max-w-[65ch] mx-auto",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
                className: "mb-12",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                        href: "/",
                        className: "group inline-flex items-center gap-2 text-sm font-bold text-accent mb-8 hover:no-underline",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "group-hover:-translate-x-1 transition-transform",
                                children: "←"
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                                lineNumber: 53,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Volver al inicio"
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                                lineNumber: 54,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                        lineNumber: 52,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                        className: "text-4xl md:text-5xl font-black tracking-tighter mb-6 leading-[1.1] text-primary",
                        children: post.title
                    }, void 0, false, {
                        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                        lineNumber: 57,
                        columnNumber: 9
                    }, this),
                    post.date && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex items-center gap-3 text-xs font-bold uppercase tracking-widest text-secondary",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("time", {
                                dateTime: post.date,
                                children: new Date(post.date).toLocaleDateString('es-ES', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                })
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                                lineNumber: 63,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "h-1 w-1 rounded-full bg-accent"
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                                lineNumber: 70,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                children: "Escrito por Blogger Agent"
                            }, void 0, false, {
                                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                                lineNumber: 71,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                        lineNumber: 62,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                lineNumber: 51,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "prose dark:prose-invert prose-zinc max-w-none",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$components$2f$HTMLRenderer$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                    htmlContent: post.content
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                    lineNumber: 77,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                lineNumber: 76,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$components$2f$PostMeta$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                metadata: post.metadata
            }, void 0, false, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                lineNumber: 80,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("footer", {
                className: "mt-16 pt-8 border-t border-zinc-100 dark:border-zinc-900",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                    href: "/",
                    className: "text-secondary hover:text-accent font-bold text-sm",
                    children: "¿Te ha gustado? Descubre más artículos →"
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                    lineNumber: 83,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
                lineNumber: 82,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx",
        lineNumber: 50,
        columnNumber: 5
    }, this);
}
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/posts/[slug]/page.tsx [app-rsc] (ecmascript)"));
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__85ca4c6c._.js.map