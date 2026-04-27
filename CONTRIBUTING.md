# Contributing - Blogger Agent TFG

¡Gracias por contribuir al proyecto! Este documento explica el flujo de trabajo para colaborar.

## 🚀 Flujo Git

1. **Crear issue** desde GitHub Projects
2. **Asignarte** la issue
3. **Crear rama**: `git checkout -b feature/nombre`
4. **Commits con Conventional Commits**: `feat(scope): description`
5. **Push y PR** contra `develop` (o `main` si no hay develop)
6. **Esperar 1 approval**
7. **Merge**

## 📝 Convenciones de Código

### Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
```
feat(agents): add research agent for topic exploration
fix(scraper): handle WordPress pagination edge case
docs(readme): update architecture diagram
test(html_builder): add JSX generation tests
refactor(llm): extract provider factory logic
```

### Ramas
- `feature/nombre` — Nuevas funcionalidades
- `fix/nombre` — Correcciones de bugs
- `docs/nombre` — Cambios de documentación
- `refactor/nombre` — Refactorización sin cambios funcionales
- `test/nombre` — Solo tests

### Pull Requests
Usá el template de PR con checklist:
- [ ] Tests pasan
- [ ] Documentación actualizada
- [ ] Revisado por al menos 1 persona

## 🧪 Testing

### Backend (Python)
```bash
cd backend
pytest tests/ -v
```

### Frontend (Next.js)
```bash
cd frontend
npm test
```

## 📦 Estructura del Proyecto

```
blogger-agent-tfg/
├── backend/          # Python + Aphra + HuggingFace
├── frontend/         # Next.js 16 + React 19 + Tailwind 4
├── docs/             # Documentación técnica
├── specs/            # SDD change specs
└── project_docs/     # Documentación legacy (deprecated)
```

## 🎯 Antes de Empezar

1. Leé el [README](README.md) para visión general
2. Revisá [PROJECT_STATUS.md](PROJECT_STATUS.md) para estado actual
3. Consultá `docs/ORCHESTRATION_PLAN.md` para el plan maestro
4. Configurá el entorno con [SETUP_GUIDE.md](SETUP_GUIDE.md)

## ❓ Dudas

Abrí una issue con label `question` o preguntá en el equipo del TFG.
