# Modelo de Datos: Diversidad Estructural y Contenido Orgánico

Este documento define la estructura de datos para asegurar la variabilidad narrativa y el estilo "Javipas-like", evitando estructuras fijas.

## 01. Entidad: ArticleDiversity (Generación de Contenido)

| Campo | Tipo | Descripción | Validación |
| :--- | :--- | :--- | :--- |
| `structural_mode` | `Enum` | Modo estructural del artículo: `REFLECTIVE`, `TECHNICAL`, `QUICK_FLASH`, `CURATED_LINKS`, `RANT`. | Debe ser uno de los cinco modos. |
| `style_signature` | `String` | RASGO predominante en este post: "Conversacional", "Crítico", "Entusiasta". | Dinámico, extraído del corpus. |
| `organic_layout` | `Boolean` | Si es true, prohíbe explícitamente subtítulos H2 en posiciones fijas. | Siempre `true`. |

---

## 02. Esquema de Metadatos de SEO (Actualización)

El modelo de datos del Front-End en `frontend/app/types/post.ts` debe soportar:

*   **Descripción Meta**: Longitud dinámica basada en el primer párrafo (no estática).
*   **Keywords**: Extraídas de forma no repetitiva (evitar saturación).

---

## 03. Reglas de Validación de Contenido (Zod)

Para prevenir la "monotonía estructural", el sistema de validación (en tests o frontend) verificará:

1.  **Variedad de Longitud de Párrafos**: No más de 3 párrafos consecutivos con longitud similar (+/- 20%).
2.  **Densidad de Heading**: Proporción de H2/H3 menor al 20% del contenido total (evitar "libros de texto SEO").
3.  **Presencia de "Markers" de Estilo**: Uso de frases habituales ("A ver...", "La cosa es que...", "Y sin embargo...").

---

## 04. Estado del Post

| Estado | Significado | Transiciones |
| :--- | :--- | :--- |
| `STYLING` | El agente está aplicando la diversidad estructural. | -> `GENERATED` |
| `DIVERSIFIED` | Validado por el agente `critic` como una estructura orgánica. | -> `READY_FOR_DEPLOY` |

