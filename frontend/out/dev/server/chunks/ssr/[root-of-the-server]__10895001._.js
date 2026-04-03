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
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>PostCard
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/client/app-dir/link.react-server.js [app-rsc] (ecmascript)");
;
;
function PostCard({ post }) {
    const formattedDate = new Date(post.date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
        className: "group py-10 border-b border-zinc-100 dark:border-zinc-900 last:border-0",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
            href: `/posts/${post.slug}`,
            className: "flex flex-col gap-3",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-2xl md:text-3xl font-extrabold tracking-tight text-primary group-hover:text-accent transition-colors leading-tight",
                    children: post.title
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                    lineNumber: 18,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex items-center gap-3 text-[10px] font-black uppercase tracking-widest text-secondary/60",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("time", {
                            dateTime: post.date,
                            children: formattedDate
                        }, void 0, false, {
                            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                            lineNumber: 23,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: "h-1 w-1 rounded-full bg-accent"
                        }, void 0, false, {
                            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                            lineNumber: 24,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            children: "Post IA"
                        }, void 0, false, {
                            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                            lineNumber: 25,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                    lineNumber: 22,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: "text-secondary dark:text-secondary leading-relaxed font-medium line-clamp-2 italic",
                    children: post.excerpt
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                    lineNumber: 28,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "mt-2 flex items-center gap-1 text-accent font-bold text-sm",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            children: "Leer artículo"
                        }, void 0, false, {
                            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                            lineNumber: 33,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: "group-hover:translate-x-1 transition-transform",
                            children: "→"
                        }, void 0, false, {
                            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                            lineNumber: 34,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
                    lineNumber: 32,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
            lineNumber: 17,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx",
        lineNumber: 16,
        columnNumber: 5
    }, this);
}
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Home,
    "dynamic",
    ()=>dynamic,
    "revalidate",
    ()=>revalidate
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$lib$2f$api$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/lib/api.ts [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$components$2f$PostCard$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/components/PostCard.tsx [app-rsc] (ecmascript)");
;
;
;
const dynamic = 'force-static';
const revalidate = false;
async function Home() {
    const posts = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$lib$2f$api$2e$ts__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["getAllPosts"])();
    if (!posts || posts.length === 0) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "py-20 text-center",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-2xl font-semibold mb-4",
                    children: "Aún no hay publicaciones"
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx",
                    lineNumber: 13,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: "text-gray-500",
                    children: "El agente no ha generado ningún artículo todavía."
                }, void 0, false, {
                    fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx",
                    lineNumber: 14,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx",
            lineNumber: 12,
            columnNumber: 7
        }, this);
    }
    // Sort by date (newest first)
    const sortedPosts = posts.sort((a, b)=>new Date(b.date).getTime() - new Date(a.date).getTime());
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-4",
        children: sortedPosts.map((post)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Escritorio$2f$PROYECTOS$2f$Big__Data__IA$2f$Modelos__de__IA$2f$blogger$2d$agent$2d$tfg$2f$frontend$2f$app$2f$components$2f$PostCard$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                post: post
            }, post.slug, false, {
                fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx",
                lineNumber: 25,
                columnNumber: 9
            }, this))
    }, void 0, false, {
        fileName: "[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx",
        lineNumber: 23,
        columnNumber: 5
    }, this);
}
}),
"[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/Escritorio/PROYECTOS/Big Data IA/Modelos de IA/blogger-agent-tfg/frontend/app/page.tsx [app-rsc] (ecmascript)"));
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__10895001._.js.map