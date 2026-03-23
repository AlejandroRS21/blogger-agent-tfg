# Blogger Agent TFG - Limpieza de Archivos Gradio

✅ **Archivos eliminados:**
- `gradio_app.py` - Interfaz básica (eliminada)
- `gradio_app_advanced.py` - Interfaz avanzada (eliminada)
- `gradio_diagrams.py` - Solo diagramas (eliminada)
- `gradio_dag.py` - Intento de daggr component (eliminada)
- `gradio_dag_interactive.py` - DAG con vis.js (eliminada)
- `test_gradio.py` - Tests de Gradio (eliminada)

✅ **Archivos mantenidos:**
- `daggr_blogger_workflow.py` - **Workflow visual oficial con Daggr**

## Nuevo Flujo de Trabajo

### Backend (Generación)
```bash
cd backend
python daggr_blogger_workflow.py
# http://localhost:7860
```

**Daggr proporciona:**
- 📊 Canvas visual con 6 agentes conectados
- 🔍 Inspección de cada nodo
- 🔄 Re-ejecución selectiva
- 💾 Persistencia de estado
- 🧪 Testing manual completo

### Frontend (Visualización)
```bash
cd frontend
npm run dev
# http://localhost:3000
```

**Next.js proporciona:**
- 📱 Interfaz responsive
- 📖 Listado de posts
- ✍️ Formulario de generación
- 🎨 Visualización de blogs

## Arquitectura

```
┌─────────────────────────────────────────────────┐
│            BLOGGER AGENT TFG                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐         ┌──────────────┐     │
│  │   Frontend   │         │   Backend    │     │
│  │  (Next.js)   │         │   (Daggr)    │     │
│  │  Port: 3000  │         │  Port: 7860  │     │
│  ├──────────────┤         ├──────────────┤     │
│  │ Visualizar   │◄───────►│ Generar      │     │
│  │ Gestionar    │  JSON   │ Debuggear    │     │
│  │ Listar       │  Files  │ Testing      │     │
│  └──────────────┘         └──────────────┘     │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Dependencias

**requirements.txt actualizado:**
```txt
# Antes:
gradio>=5.0.0

# Ahora:
daggr>=0.7.0  # Incluye gradio como dependencia
```

## Documentación

Ver [DAGGR_WORKFLOW.md](DAGGR_WORKFLOW.md) para:
- Guía completa de uso
- Flujo de 6 agentes explicado
- Características avanzadas
- Integración Frontend ↔ Backend
- Testing y debugging
