/**
 * API Route: Generate Post
 * 
 * POST /api/generate-post
 * 
 * Conecta con el backend Python para generar posts usando el Blogger Agent.
 */

import { NextRequest, NextResponse } from 'next/server';
import type { GenerateRequest, GenerateResponse, BlogPost } from '../../types/post';

// Configuración del backend
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const USE_MOCK = process.env.USE_MOCK === 'true' || true; // Default to mock for development

/**
 * Mock backend response para desarrollo sin backend corriendo
 */
function mockGeneratePost(request: GenerateRequest): BlogPost {
  const slug = request.topic.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
  
  return {
    id: slug,
    title: `${request.topic}: Una Perspectiva Única`,
    description: `Explorando ${request.topic} desde el estilo de ${request.blogger_name}`,
    html_code: `
      <article>
        <p>Hola, soy <strong>${request.blogger_name}</strong>, y hoy quiero hablar sobre <em>${request.topic}</em>.</p>
        
        <h2>Introducción</h2>
        <p>${request.blogger_bio}</p>
        
        <h2>Desarrollo del Tema</h2>
        <p>Este es un post generado de forma mock para desarrollo. En producción, aquí verías contenido generado por los agentes de IA basándose en mi estilo de escritura.</p>
        
        <h3>Puntos Clave</h3>
        <ul>
          ${(request.keywords || []).map(kw => `<li>${kw}</li>`).join('\n          ')}
        </ul>
        
        <blockquote>
          "El contenido generado por IA debe mantener la autenticidad del blogger"
        </blockquote>
        
        <h2>Conclusión</h2>
        <p>Gracias por leer. Este contenido fue generado usando el Blogger Agent TFG.</p>
      </article>
    `,
    metadata: {
      word_count: 150,
      reading_time: 1,
      date: new Date().toISOString().split('T')[0],
      author: request.blogger_name,
      tags: request.keywords || []
    }
  };
}

/**
 * Llama al backend Python real
 */
async function callBackendAPI(request: GenerateRequest): Promise<BlogPost> {
  const response = await fetch(`${BACKEND_URL}/api/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return data.post;
}

export async function POST(request: NextRequest) {
  try {
    const body: GenerateRequest = await request.json();

    // Validación
    if (!body.blogger_name || !body.blogger_bio || !body.topic) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'Missing required fields: blogger_name, blogger_bio, topic' 
        } as GenerateResponse,
        { status: 400 }
      );
    }

    if (!body.blogger_sample_posts || body.blogger_sample_posts.length === 0) {
      return NextResponse.json(
        { 
          success: false, 
          error: 'At least one sample post is required' 
        } as GenerateResponse,
        { status: 400 }
      );
    }

    const startTime = Date.now();

    // Generar post (mock o backend real)
    let post: BlogPost;
    if (USE_MOCK) {
      console.log('[API] Using mock backend');
      post = mockGeneratePost(body);
      // Simular delay de procesamiento
      await new Promise(resolve => setTimeout(resolve, 2000));
    } else {
      console.log('[API] Calling real backend:', BACKEND_URL);
      post = await callBackendAPI(body);
    }

    const executionTime = Date.now() - startTime;

    return NextResponse.json({
      success: true,
      post,
      execution_time: executionTime
    } as GenerateResponse);

  } catch (error) {
    console.error('[API] Error generating post:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      } as GenerateResponse,
      { status: 500 }
    );
  }
}

// Exportar configuración de ruta
export const runtime = 'nodejs'; // or 'edge'
export const dynamic = 'force-dynamic'; // No caching
