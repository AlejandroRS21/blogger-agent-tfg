import type { GenerateRequest, GenerateResponse, BlogPost } from "@/types/post";

function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9áéíóúüñ]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function generateMockPost(topic: string): BlogPost {
  const now = new Date();
  const dateStr = now.toISOString().split("T")[0];
  const slug = generateSlug(topic);

  const content = `
<h2>Introducción</h2>
<p>En el mundo actual, la tecnología avanza a pasos agigantados y cada vez son más las personas que se interesan por <strong>${topic}</strong>. Este artículo explora los aspectos fundamentales y las últimas tendencias que están marcando el panorama actual.</p>

<h2>Contexto y antecedentes</h2>
<p>El ecosistema digital ha evolucionado de manera significativa en los últimos años. Según diversos estudios, la adopción de nuevas tecnologías relacionadas con <strong>${topic}</strong> ha crecido exponencialmente, transformando la forma en que interactuamos con la información y abriendo nuevas oportunidades para profesionales y empresas.</p>

<h2>Puntos clave</h2>
<ul>
  <li><strong>Innovación constante:</strong> El sector se caracteriza por una innovación continua, donde cada trimestre surgen nuevas herramientas y enfoques.</li>
  <li><strong>Impacto en la industria:</strong> Las empresas que adoptan estas tecnologías reportan mejoras significativas en eficiencia y productividad.</li>
  <li><strong>Formación especializada:</strong> La demanda de profesionales con conocimientos en ${topic} ha aumentado considerablemente.</li>
  <li><strong>Comunidad activa:</strong> Existe una comunidad global muy activa que comparte conocimiento y mejores prácticas.</li>
</ul>

<h2>Análisis en profundidad</h2>
<p>Para comprender realmente el impacto de <strong>${topic}</strong>, es necesario analizar varios factores. La infraestructura tecnológica actual permite procesar volúmenes de datos que hace una década eran impensables, democratizando el acceso a herramientas que antes solo estaban al alcance de grandes corporaciones.</p>

<blockquote>
  "La tecnología no es nada. Lo importante es que tengas fe en la gente, que sean básicamente buenas e inteligentes, y si les das herramientas, harán cosas maravillosas con ellas." — Steve Jobs
</blockquote>

<h2>Conclusiones</h2>
<p>En resumen, <strong>${topic}</strong> representa una oportunidad única para aquellos que deseen mantenerse a la vanguardia en el mundo digital. La clave está en la formación continua y en la capacidad de adaptación a un entorno que cambia rápidamente.</p>
`;

  const words = content.replace(/<[^>]*>/g, "").split(/\s+/).length;
  const readingTime = Math.max(1, Math.ceil(words / 200));

  return {
    id: crypto.randomUUID(),
    slug,
    title: topic.charAt(0).toUpperCase() + topic.slice(1),
    description: `Análisis completo sobre ${topic}, explorando fundamentos, tendencias actuales y perspectivas futuras.`,
    content,
    author: "Blogger Agent AI",
    date: dateStr,
    word_count: words,
    reading_time: readingTime,
    keywords: [topic, "tecnología", "innovación", "análisis"],
    tags: [topic, "Tecnología", "Innovación"],
    html_structure: {
      html: content,
      jsx: "<div>" + content + "</div>",
      headings: ["Introducción", "Contexto y antecedentes", "Puntos clave", "Análisis en profundidad", "Conclusiones"],
      meta: {
        title: topic.charAt(0).toUpperCase() + topic.slice(1),
        description: `Análisis completo sobre ${topic}`,
        keywords: `${topic}, tecnología, innovación, análisis`,
      },
      reading_time: readingTime,
      word_count: words,
    },
  };
}

// Generate static sample posts for homepage display
export function getSamplePosts(): BlogPost[] {
  const topics = [
    "Inteligencia Artificial en 2026",
    "El futuro de las APIs REST",
    "Blockchain más allá de las criptomonedas",
    "Machine Learning en producción",
    "TypeScript vs JavaScript en 2026",
    "Cloud Computing y serverless",
  ];

  return topics.map((topic) => generateMockPost(topic));
}

export async function generatePostMock(data: GenerateRequest): Promise<GenerateResponse> {
  await new Promise((resolve) => setTimeout(resolve, 2000));

  const post = generateMockPost(data.topic);

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
    const backendUrl = process.env.BACKEND_URL;
    if (!backendUrl) {
      return { success: false, error: "BACKEND_URL no configurado" };
    }

    // Modal webhook format: POST directly to the webhook URL
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        blogger_urls: [data.blog_url],
        topic: data.topic,
        provider: data.provider || "huggingface",
        enable_critique: true,
        min_word_count: 800,
        max_word_count: 2500,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      return {
        success: false,
        error: `Error del servidor (${response.status}): ${errorText}`,
      };
    }

    // Modal webhook response format: { success, data, error }
    const result = await response.json();

    if (result.success && result.data) {
      // Transform Modal response to our BlogPost format
      const modalData = result.data;
      const slug = generateSlug(data.topic);
      return {
        success: true,
        post: {
          id: modalData.workflow_id || crypto.randomUUID(),
          slug,
          title: data.topic.charAt(0).toUpperCase() + data.topic.slice(1),
          description: modalData.description || `Artículo generado sobre ${data.topic}`,
          content: modalData.content || modalData.final_content || "",
          author: "Blogger Agent AI",
          date: new Date().toISOString().split("T")[0],
          word_count: modalData.word_count || 0,
          reading_time: modalData.reading_time || 1,
          keywords: modalData.keywords || [],
          tags: modalData.tags || [],
          html_structure: modalData.html_structure,
        },
        execution_time: modalData.execution_time,
      };
    }

    return {
      success: false,
      error: result.error || "Error desconocido del backend",
    };
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : "Error de conexión con el servidor",
    };
  }
}

export async function getAllPosts(): Promise<BlogPost[]> {
  try {
    const GITHUB_RAW_BASE = "https://raw.githubusercontent.com/AlejandroRS21/blogger-agent-tfg/main/docs";
    const response = await fetch(`${GITHUB_RAW_BASE}/posts.json`, { next: { revalidate: 60 } });
    
    if (!response.ok) {
      return getSamplePosts();
    }
    
    const data = await response.json();
    return data.map((post: any) => ({
      ...post,
      slug: post.slug || post.id || "unnamed-post",
      title: post.title || "Post sin título",
      date: post.date || new Date().toISOString(),
      author: post.author || "Blogger Agent",
    }));
  } catch (error) {
    console.warn('[API] Fallback to samples:', error);
    return getSamplePosts();
  }
}

export async function fetchPost(slug: string): Promise<BlogPost | null> {
  const useMock = process.env.USE_MOCK !== "false";

  if (useMock) {
    const sampleTopic = slug.replace(/-/g, " ");
    const post = generateMockPost(sampleTopic);
    post.slug = slug;
    return post;
  }

  try {
    const GITHUB_RAW_BASE = "https://raw.githubusercontent.com/AlejandroRS21/blogger-agent-tfg/main/docs";
    const response = await fetch(`${GITHUB_RAW_BASE}/posts/${slug}.json`, { next: { revalidate: 60 } });
    
    if (response.ok) {
      return await response.json();
    }
    
    return null;
  } catch (error) {
    return null;
  }
}
