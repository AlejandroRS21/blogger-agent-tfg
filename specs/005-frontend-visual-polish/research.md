# Investigación: Diversidad Estructural y Espontaneidad (Javipas-Style)

## 01. Análisis de Patrones Estructurales en Javipas.com

### Observaciones del Estilo Original
Tras revisar el feedback del usuario y los archivos del corpus (`javipas_corpus.json`, `javipas_style_profile.json`):

1.  **Rechazo a la Plantilla**: No existe un "Intro -> Subtítulo 1 -> Subtítulo 2 -> Conclusión".
2.  **Narrativa vs. Listado**: Algunos posts son puramente narrativos (ensayo), otros son listas de herramientas, y otros son reacciones rápidas a una noticia.
3.  **Uso Inesperado de Formatos**:
    *   Citas directas largas integradas en el flujo.
    *   Listas de puntos que actúan como "balas de pensamiento".
    *   Párrafos de una sola frase para énfasis dramático.
4.  **Flujo "Stream of Consciousness"**: La estructura sigue el razonamiento del autor, no un estándar SEO.

### Clasificación de Estructuras Identificadas
*   **Tipo A (Ensayo Reflexivo)**: Párrafos medios-largos, pocos subtítulos, enfoque en la opinión personal.
*   **Tipo B (Análisis Técnico/Cacharreo)**: Uso extensivo de negritas, imágenes intercaladas, listas de especificaciones seguidas de "Pero...".
*   **Tipo C (Flash News)**: Muy corto, directo al grano, termina con una pregunta al lector.
*   **Tipo D (Curación de Enlaces)**: Estructura de "Link + Comentario mordaz".

---

## 02. Estrategia de Implementación Tecnológica

### Decisión 1: Inyección de "Semilla de Spontaneidad" en `content_generator.py`
*   **Propuesta**: En lugar de pedirle al LLM que siga un esquema, le daremos una **intención estructural** aleatoria o basada en el tema.
*   **Acción**: Modificar el prompt en `backend/aphra_blogger/agents/content_generator.py` para prohibir explícitamente el uso de estructuras predecibles.

### Decisión 2: Actualización del Perfil de Estilo
*   **Propuesta**: Añadir una sección de "Layout Patterns" al archivo `javipas_style_profile.json` que incluya ejemplos de posts con estructuras radicalmente distintas.

### Decisión 3: Validación Frontend de Riqueza de Tags
*   **Propuesta**: Ajustar `frontend/app/posts/[slug]/page.tsx` para que el `prose` de Tailwind maneje correctamente elementos menos comunes (blockquotes anidados, listas dentro de listas) que Javipas usa ocasionalmente.

---

## 03. Conclusiones y Próximos Pasos (Fase 1)
- [ ] Refactorizar el agente generador para usar el modo "Antiplanteilla".
- [ ] Actualizar el sistema de prompting para incluir la variable `structural_template_type`.
- [ ] Verificar que el `Markdown` generado por el agente no sea monótono.

