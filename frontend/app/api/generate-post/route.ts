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

function generateMockResponse(topic: string, blogUrl: string): GenerateResponse {
  const content = `
<h2>Introduccion</h2>
<p>En el mundo actual, la tecnologia avanza a pasos agigantados y cada vez son mas las personas que se interesan por <strong>${topic}</strong>. Este articulo explora los aspectos fundamentales y las ultimas tendencias que estan marcando el panorama actual.</p>

<h2>Contexto y antecedentes</h2>
<p>El ecosistema digital ha evolucionado de manera significativa en los ultimos anos. La adopcion de nuevas tecnologias relacionadas con <strong>${topic}</strong> ha crecido exponencialmente, transformando la forma en que interactuamos con la informacion y abriendo nuevas oportunidades para profesionales y empresas.</p>

<h2>Puntos clave</h2>
<ul>
  <li><strong>Innovacion constante:</strong> El sector se caracteriza por una innovacion continua, donde cada trimestre surgen nuevas herramientas y enfoques.</li>
  <li><strong>Impacto en la industria:</strong> Las empresas que adoptan estas tecnologias reportan mejoras significativas en eficiencia y productividad.</li>
  <li><strong>Formacion especializada:</strong> La demanda de profesionales con conocimientos en ${topic} ha aumentado considerablemente.</li>
</ul>

<h2>Analisis en profundidad</h2>
<p>Para comprender realmente el impacto de <strong>${topic}</strong>, es necesario analizar varios factores. La infraestructura tecnologica actual permite procesar volumenes de datos que hace una decada eran impensables, democratizando el acceso a herramientas que antes solo estaban al alcance de grandes corporaciones.</p>

<blockquote>
  "La tecnologia no es nada. Lo importante es que tengas fe en la gente, que sean basicamente buenas e inteligentes, y si les das herramientas, haran cosas maravillosas con ellas." — Steve Jobs
</blockquote>

<h2>Conclusiones</h2>
<p>En resumen, <strong>${topic}</strong> representa una oportunidad unica para aquellos que deseen mantenerse a la vanguardia en el mundo digital. La clave esta en la formacion continua y en la capacidad de adaptacion a un entorno que cambia rapidamente.</p>
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
      description: `Analisis completo y detallado sobre ${topic}, explorando sus fundamentos, tendencias actuales y perspectivas futuras.`,
      content,
      author: "Blogger Agent AI",
      date: new Date().toISOString().split("T")[0],
      word_count: words,
      reading_time: readingTime,
      keywords: [topic, "tecnologia", "innovacion", "analisis"],
      tags: [topic, "Tecnologia", "Innovacion"],
      html_structure: {
        html: content,
        jsx: "<div>" + content + "</div>",
        headings: ["Introduccion", "Contexto y antecedentes", "Puntos clave", "Analisis en profundidad", "Conclusiones"],
        meta: {
          title,
          description: `Analisis completo sobre ${topic}`,
          keywords: `${topic}, tecnologia, innovacion, analisis`,
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

    // Validate required fields
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
      // Simulate processing delay
      await new Promise((resolve) => setTimeout(resolve, 2000));
      const response = generateMockResponse(body.topic, body.blog_url);
      return NextResponse.json(response);
    }

    // Real backend call
    const backendUrl = process.env.BACKEND_URL;
    if (!backendUrl) {
      return NextResponse.json(
        { success: false, error: "BACKEND_URL no configurado" },
        { status: 500 }
      );
    }

    const backendResponse = await fetch(`${backendUrl}/generate-post`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      return NextResponse.json(
        { success: false, error: `Error del backend: ${errorText}` },
        { status: backendResponse.status }
      );
    }

    const data: GenerateResponse = await backendResponse.json();
    return NextResponse.json(data);
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
