import { NextRequest, NextResponse } from "next/server";
import type { GenerateRequest, GenerateResponse } from "@/types/post";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9áéíóúüñ]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function generateMockResponse(topic: string): GenerateResponse {
  const content = `
<h2>Introducción</h2>
<p>En el mundo actual, la tecnología avanza a pasos agigantados y cada vez son más las personas que se interesan por <strong>${topic}</strong>. Este artículo explora los aspectos fundamentales y las últimas tendencias que están marcando el panorama actual.</p>

<h2>Contexto y antecedentes</h2>
<p>El ecosistema digital ha evolucionado de manera significativa en los últimos años. La adopción de nuevas tecnologías relacionadas con <strong>${topic}</strong> ha crecido exponencialmente, transformando la forma en que interactuamos con la información.</p>

<h2>Puntos clave</h2>
<ul>
  <li><strong>Innovación constante:</strong> El sector se caracteriza por una innovación continua.</li>
  <li><strong>Impacto en la industria:</strong> Las empresas que adoptan estas tecnologías reportan mejoras significativas.</li>
  <li><strong>Formación especializada:</strong> La demanda de profesionales ha aumentado considerablemente.</li>
</ul>

<h2>Análisis en profundidad</h2>
<p>Para comprender realmente el impacto de <strong>${topic}</strong>, es necesario analizar varios factores. La infraestructura tecnológica actual permite procesar volúmenes de datos que hace una década eran impensables.</p>

<blockquote>
  "La tecnología no es nada. Lo importante es que tengas fe en la gente, que sean básicamente buenas e inteligentes, y si les das herramientas, harán cosas maravillosas con ellas." — Steve Jobs
</blockquote>

<h2>Conclusiones</h2>
<p>En resumen, <strong>${topic}</strong> representa una oportunidad única para aquellos que deseen mantenerse a la vanguardia en el mundo digital. La clave está en la formación continua.</p>
`;

  const words = content.replace(/<[^>]*>/g, "").split(/\s+/).length;
  const readingTime = Math.max(1, Math.ceil(words / 200));
  const title = topic.charAt(0).toUpperCase() + topic.slice(1);
  const slug = generateSlug(topic);

  return {
    success: true,
    execution_time: 2.3,
    post: {
      id: crypto.randomUUID(),
      slug,
      title,
      description: `Análisis completo y detallado sobre ${topic}, explorando sus fundamentos, tendencias actuales y perspectivas futuras.`,
      content,
      author: "Blogger Agent AI",
      date: new Date().toISOString().split("T")[0],
      word_count: words,
      reading_time: readingTime,
      keywords: [topic, "tecnología", "innovación", "análisis"],
      tags: [topic, "Tecnología", "Innovación"],
      html_structure: {
        html: content,
        jsx: "<div>" + content + "</div>",
        headings: ["Introducción", "Contexto y antecedentes", "Puntos clave", "Análisis en profundidad", "Conclusiones"],
        meta: {
          title,
          description: `Análisis completo sobre ${topic}`,
          keywords: `${topic}, tecnología, innovación, análisis`,
        },
        reading_time: readingTime,
        word_count: words,
      },
    },
  };
}

export async function POST(request: NextRequest) {
  try {
    const body: GenerateRequest = await request.json();

    if (!body.topic || !body.topic.trim()) {
      return NextResponse.json(
        { success: false, error: "El tema es obligatorio" },
        { status: 400 }
      );
    }

    if (!body.blog_url || !body.blog_url.trim()) {
      return NextResponse.json(
        { success: false, error: "La URL del blog es obligatoria" },
        { status: 400 }
      );
    }

    const useMock = process.env.USE_MOCK !== "false";

    if (useMock) {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      const response = generateMockResponse(body.topic);
      return NextResponse.json(response);
    }

    // === REAL MODE: Connect to Modal webhook ===
    const backendUrl = process.env.BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json(
        { success: false, error: "BACKEND_URL no configurado. Configuralo en Vercel Environment Variables." },
        { status: 500 }
      );
    }

    // Modal webhook expects: { blogger_urls, topic, provider, enable_critique, ... }
    const modalResponse = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        blogger_urls: [body.blog_url],
        topic: body.topic,
        provider: body.provider || "huggingface",
        enable_critique: true,
        min_word_count: 800,
        max_word_count: 2500,
      }),
    });

    if (!modalResponse.ok) {
      const errorText = await modalResponse.text();
      return NextResponse.json(
        { success: false, error: `Error del backend Modal (${modalResponse.status}): ${errorText}` },
        { status: 502 }
      );
    }

    // Modal response: { success: bool, data: {...}, error: string|null }
    const modalResult = await modalResponse.json();

    if (!modalResult.success) {
      return NextResponse.json(
        { success: false, error: modalResult.error || "Error del backend Modal" },
        { status: 500 }
      );
    }

    // Transform Modal data to our GenerateResponse format
    const slug = generateSlug(body.topic);
    const modalData = modalResult.data;
    return NextResponse.json({
      success: true,
      execution_time: modalData.execution_time,
      post: {
        id: modalData.workflow_id || crypto.randomUUID(),
        slug,
        title: body.topic.charAt(0).toUpperCase() + body.topic.slice(1),
        description: modalData.description || `Artículo generado sobre ${body.topic}`,
        content: modalData.content || modalData.final_content || "",
        author: "Blogger Agent AI",
        date: new Date().toISOString().split("T")[0],
        word_count: modalData.word_count || 0,
        reading_time: modalData.reading_time || 1,
        keywords: modalData.keywords || [],
        tags: modalData.tags || [],
        html_structure: modalData.html_structure,
      } satisfies import("@/types/post").BlogPost,
    } satisfies GenerateResponse);

  } catch (err) {
    return NextResponse.json(
      {
        success: false,
        error: err instanceof Error ? err.message : "Error interno del servidor",
      },
      { status: 500 }
    );
  }
}
