import type { GenerateRequest, GenerateResponse, BlogPost } from "@/types/post";

function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9áéíóúüñ]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function generateMockPost(topic: string, blogUrl: string): BlogPost {
  const now = new Date();
  const dateStr = now.toISOString().split("T")[0];
  const slug = generateSlug(topic);

  const content = `
<h2>Introduccion</h2>
<p>En el mundo actual, la tecnologia avanza a pasos agigantados y cada vez son mas las personas que se interesan por <strong>${topic}</strong>. Este articulo explora los aspectos fundamentales y las ultimas tendencias que estan marcando el panorama actual.</p>

<h2>Contexto y antecedentes</h2>
<p>El ecosistema digital ha evolucionado de manera significativa en los ultimos anos. Segun diversos estudios, la adopcion de nuevas tecnologias relacionadas con <strong>${topic}</strong> ha crecido exponencialmente. Este crecimiento no solo ha transformado la forma en que interactuamos con la informacion, sino que tambien ha abierto nuevas oportunidades para profesionales y empresas por igual.</p>

<h2>Puntos clave a considerar</h2>
<ul>
  <li><strong>Innovacion constante:</strong> El sector se caracteriza por una innovacion continua, donde cada trimestre surgen nuevas herramientas y enfoques.</li>
  <li><strong>Impacto en la industria:</strong> Las empresas que adoptan estas tecnologias reportan mejoras significativas en eficiencia y productividad.</li>
  <li><strong>Formacion especializada:</strong> La demanda de profesionales con conocimientos en ${topic} ha aumentado considerablemente.</li>
  <li><strong>Comunidad activa:</strong> Existe una comunidad global muy activa que comparte conocimiento y mejores practicas.</li>
</ul>

<h2>Analisis en profundidad</h2>
<p>Para comprender realmente el impacto de <strong>${topic}</strong>, es necesario analizar varios factores. En primer lugar, la infraestructura tecnologica actual permite procesar volumenes de datos que hace una decada eran impensables. Esto ha democratizado el acceso a herramientas que antes solo estaban al alcance de grandes corporaciones.</p>

<blockquote>
  "La tecnologia no es nada. Lo importante es que tengas fe en la gente, que sean basicamente buenas e inteligentes, y si les das herramientas, haran cosas maravillosas con ellas." — Steve Jobs
</blockquote>

<p>En segundo lugar, la colaboracion entre instituciones academicas y empresas privadas ha acelerado el ritmo de la investigacion. Los laboratorios de investigacion en <strong>${topic}</strong> estan produciendo avances a un ritmo sin precedentes.</p>

<h2>Conclusiones</h2>
<p>En resumen, <strong>${topic}</strong> representa una oportunidad unica para aquellos que deseen mantenerse a la vanguardia en el mundo digital. La clave esta en la formacion continua y en la capacidad de adaptacion a un entorno que cambia rapidamente.</p>

<p>Te invito a seguir explorando este fascinante tema y a compartir tus experiencias en los comentarios. El conocimiento crece cuando se comparte.</p>
`;

  const words = content.replace(/<[^>]*>/g, "").split(/\s+/).length;
  const readingTime = Math.max(1, Math.ceil(words / 200));

  return {
    id: crypto.randomUUID(),
    slug,
    title: topic.charAt(0).toUpperCase() + topic.slice(1),
    description: `Un analisis completo y detallado sobre ${topic}, explorando sus fundamentos, tendencias actuales y perspectivas futuras en el ecosistema digital.`,
    content,
    author: "Blogger Agent AI",
    date: dateStr,
    word_count: words,
    reading_time: readingTime,
    keywords: [topic, "tecnologia", "innovacion", "analisis"],
    tags: [topic, "Tecnologia", "Innovacion"],
    html_structure: {
      html: content,
      jsx: "<div>" + content + "</div>",
      headings: ["Introduccion", "Contexto y antecedentes", "Puntos clave a considerar", "Analisis en profundidad", "Conclusiones"],
      meta: {
        title: topic.charAt(0).toUpperCase() + topic.slice(1),
        description: `Analisis completo sobre ${topic}`,
        keywords: `${topic}, tecnologia, innovacion, analisis`,
      },
      reading_time: readingTime,
      word_count: words,
    },
  };
}

export async function generatePostMock(data: GenerateRequest): Promise<GenerateResponse> {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const post = generateMockPost(data.topic, data.blog_url);

  return {
    success: true,
    post,
    execution_time: 2.0,
  };
}

export async function generatePost(data: GenerateRequest): Promise<GenerateResponse> {
  const useMock = process.env.USE_MOCK !== "false";

  if (useMock) {
    return generatePostMock(data);
  }

  try {
    const backendUrl = process.env.BACKEND_URL || "https://your-modal-app.modal.run";
    const response = await fetch(`${backendUrl}/generate-post`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return {
        success: false,
        error: `Error del servidor (${response.status}): ${errorText}`,
      };
    }

    const result: GenerateResponse = await response.json();
    return result;
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : "Error de conexion con el servidor",
    };
  }
}

export async function fetchPost(slug: string): Promise<BlogPost | null> {
  const useMock = process.env.USE_MOCK !== "false";

  if (useMock) {
    // Return a sample post for preview — in production this would come from a DB
    const sampleTopic = slug.replace(/-/g, " ");
    const post = generateMockPost(sampleTopic, "https://javipas.com");
    // Override slug to match request
    post.slug = slug;
    return post;
  }

  // Real implementation would fetch from backend
  return null;
}
