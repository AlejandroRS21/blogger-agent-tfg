# Feature Specification: Solucionar error de validación de API key al usar el proveedor Gemini

**Feature Branch**: `006-fix-gemini-api-key`  
**Created**: 4 de abril de 2026  
**Status**: Draft  
**Input**: User description: "solucionar error : Error initializing orchestrator: At least one API key must be set: OPENAI_API_KEY, HF_TOKEN, or MODAL_TOKEN_ID/SECRET"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ejecución exitosa con Gemini AI (Priority: P1)

Como usuario del Blogger Agent, quiero poder ejecutar el orquestador usando únicamente mi clave de API de Gemini, sin que el sistema me obligue a tener configuradas otras claves que no voy a utilizar.

**Why this priority**: Es crítico para la usabilidad del sistema. Actualmente, un usuario con solo Gemini no puede usar el software a pesar de haber configurado su clave.

**Independent Test**: Ejecutar el comando `python -m src.orchestrator.runner --provider gemini --topic "Texto" --blog-url "URL"` teniendo únicamente configurada la variable `GEMINI_API_KEY` en el entorno.

**Acceptance Scenarios**:

1. **Given** un entorno con `GEMINI_API_KEY` configurada y sin claves de OpenAI/HF/Modal, **When** ejecuto el runner con el proveedor `gemini`, **Then** el orquestador se inicializa correctamente sin lanzar errores de validación de claves.
2. **Given** un archivo `.env` con la clave de Gemini, **When** el sistema carga la configuración, **Then** reconoce que hay al menos una clave válida presente.

---

### User Story 2 - Mensajes de error informativos (Priority: P2)

Como desarrollador, quiero que los mensajes de error de validación incluyan todas las opciones de proveedores soportadas, incluyendo Gemini, para saber qué claves puedo configurar.

**Why this priority**: Mejora la experiencia de depuración y guía al usuario hacia la solución correcta.

**Independent Test**: Eliminar todas las claves de API y ejecutar el sistema para verificar que el mensaje de error mencione explícitamente `GEMINI_API_KEY`.

**Acceptance Scenarios**:

1. **Given** ninguna clave de API configurada, **When** intento ejecutar el sistema, **Then** el error mostrado es: "Error initializing orchestrator: At least one API key must be set: OPENAI_API_KEY, HF_TOKEN, GEMINI_API_KEY, or MODAL_TOKEN_ID/SECRET".

---

### Edge Cases

- **Uso de múltiples claves**: Si el usuario tiene configurada la clave de Gemini y la de OpenAI, el sistema debe permitir elegir cualquiera de los dos proveedores sin conflictos.
- **Clave vacía**: Si la variable `GEMINI_API_KEY` está presente pero vacía, el sistema debe tratarla como no configurada y lanzar el error correspondiente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE reconocer la variable de entorno `GEMINI_API_KEY` (y opcionalmente `GOOGLE_API_KEY`) como un método de autenticación válido.
- **FR-002**: El `OrchestratorConfig` DEBE considerar que la configuración es válida si `GEMINI_API_KEY` está presente, incluso si faltan `OPENAI_API_KEY`, `HF_TOKEN` o las claves de Modal.
- **FR-003**: El mensaje de error de validación en `OrchestratorConfig.validate()` DEBE actualizarse para listar `GEMINI_API_KEY` entre las opciones requeridas.
- **FR-004**: El sistema DEBE asegurar que el `provider` seleccionado coincide con una clave de API configurada antes de iniciar el workflow.

### Success Criteria

- **SC-001**: El comando de ejecución del usuario mencionado en el prompt (`python -m src.orchestrator.runner ... --provider gemini`) se completa sin el error de "Error initializing orchestrator".
- **SC-002**: Al menos el 100% de las fases del orquestador se inicializan correctamente usando el proveedor Gemini si la clave está presente.
- **SC-003**: No se rompe la compatibilidad con los proveedores existentes (OpenAI, HuggingFace, Modal).

## Assumptions

- Se asume que el usuario ya tiene instalada la librería `google-generativeai`.
- Se asume que el nombre del modelo por defecto para Gemini es compatible con la región del usuario.

