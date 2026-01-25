# 💡 Propuestas de Mejora para Alex's Notes

## 🎨 Apariencia y Diseño

### 1. Cambiar a un tema más orientado a blog
**Problema**: Actualmente usas `book-theme` que está pensado para libros lineales.

**Solución**: Considera cambiar a templates más modernos:
- **MyST Article Theme**: Más limpio para artículos independientes
- **Sphinx Book Theme personalizado**: Permite más customización
- **Alternativa**: Usar un generador de sitios estáticos como:
  - **Quarto** (similar a MyST pero más orientado a publicaciones)
  - **MkDocs Material** (muy popular para documentación técnica estilo blog)

**Implementación sugerida**:
```yaml
# myst.yml
site:
  template: article-theme  # Prueba este primero
  options:
    logo: assets/logo.png
    favicon: assets/favicon.ico
```

### 2. Añadir un logo y favicon personalizados
Crea una carpeta `assets/` y añade:
- `logo.png` (recomendado: 200x50px)
- `favicon.ico` (16x16px y 32x32px)

### 3. Implementar tags/etiquetas por tema
Para un blog de notas variadas es crucial la categorización:

```markdown
---
title: Mi nota sobre Machine Learning
tags: [machine-learning, python, sklearn]
date: 2026-01-25
---
```

Luego podrías crear páginas índice por tag.

### 4. Añadir un sistema de fechas y "últimas notas"
Modifica `index.md` para que muestre las últimas entradas:

```markdown
# Alex's Notes

## Últimas notas
- [2026-01-25] Introducción a Transformers
- [2026-01-20] Setup de Docker en MacOS
- [2026-01-15] Apuntes de AWS Lambda
```

Esto se puede automatizar con un script Python.

---

## 📂 Estructura y Organización

### 5. Reorganizar contenido por categorías
Propuesta de estructura:

```
.
├── machine-learning/
│   ├── _category.md
│   ├── transformers.md
│   └── sklearn-tips.ipynb
├── devops/
│   ├── _category.md
│   ├── docker.md
│   └── kubernetes.md
├── programming/
│   ├── python/
│   ├── rust/
│   └── web/
├── random/              # Para experimentos y notas variadas
└── index.md
```

Cada `_category.md` describe la categoría.

### 6. Crear un `_toc.yml` automático
Script para generar tabla de contenidos basado en la estructura de carpetas:

```python
# scripts/generate_toc.py
import os
from pathlib import Path
import yaml

def generate_toc():
    # Escanea directorios y genera _toc.yml automáticamente
    pass
```

---

## 🚀 Funcionalidades Técnicas

### 7. Mejorar el workflow de GitHub Actions

**Optimizaciones sugeridas**:

```yaml
# .github/workflows/deploy.yml
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/pyproject.toml') }}

- name: Install AWS CLI
  run: pip install awscli  # El workflow actual asume que ya está

- name: Invalidate CloudFront (si usas CDN)
  run: aws cloudfront create-invalidation --distribution-id XXX --paths "/*"
```

### 8. Añadir CloudFront para HTTPS y mejor rendimiento

**Beneficios**:
- HTTPS gratis con certificado de AWS
- Mejor velocidad global (CDN)
- Dominio personalizado (ej: `notes.alexdelapuente.com`)

**Infraestructura adicional** (archivo `infra/cloudfront.tf`):

```hcl
resource "aws_cloudfront_distribution" "website" {
  origin {
    domain_name = aws_s3_bucket_website_configuration.website.website_endpoint
    origin_id   = "S3-Website"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-Website"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
    # O usa ACM certificate para dominio custom
  }
}
```

### 9. Pre-commit hooks para validación

Crea `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: local
    hooks:
      - id: jupyter-book-build
        name: Test build
        entry: jupyter-book build --html
        language: system
        pass_filenames: false
```

Instala: `pip install pre-commit && pre-commit install`

### 10. Búsqueda de contenido

MyST y Jupyter Book soportan búsqueda. Actívala en `myst.yml`:

```yaml
site:
  template: book-theme
  options:
    search: true  # Añade barra de búsqueda
```

---

## 📝 Calidad de Vida

### 11. Script de creación rápida de notas

Crea `scripts/new_note.py`:

```python
#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path

def create_note(category, title):
    slug = title.lower().replace(" ", "-")
    date = datetime.now().strftime("%Y-%m-%d")

    category_dir = Path(category)
    category_dir.mkdir(exist_ok=True)

    note_path = category_dir / f"{slug}.md"

    content = f"""---
title: {title}
date: {date}
tags: []
---

# {title}

Escribe tu contenido aquí...
"""

    note_path.write_text(content)
    print(f"✅ Nota creada: {note_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: ./scripts/new_note.py <categoría> <título>")
        sys.exit(1)

    create_note(sys.argv[1], sys.argv[2])
```

Uso:
```bash
python scripts/new_note.py machine-learning "Introducción a Transformers"
```

### 12. Makefile para comandos comunes

Crea `Makefile`:

```makefile
.PHONY: build serve clean deploy new

build:
	jupyter-book build --html

serve: build
	open _build/html/index.html

clean:
	jupyter-book clean .

deploy: build
	aws s3 sync _build/html s3://alexnotes-blog-2026 --region eu-west-1

new:
	@echo "Uso: python scripts/new_note.py <categoría> <título>"
```

Uso: `make serve`, `make deploy`, etc.

### 13. GitHub Issue Templates

Para que tú mismo puedas trackear ideas de contenido:

`.github/ISSUE_TEMPLATE/idea-nota.md`:
```markdown
---
name: Idea de nota
about: Template para ideas de nuevas notas
---

## Tema
¿Sobre qué trata?

## Categoría
- [ ] Machine Learning
- [ ] DevOps
- [ ] Programming
- [ ] Random

## Notas adicionales
Contexto, links, recursos...
```

---

## 🔒 Seguridad y Mantenimiento

### 14. Dependabot para actualizaciones automáticas

Crea `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "terraform"
    directory: "/infra"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### 15. Backup automático

Añade un workflow para backup del bucket S3:

```yaml
# .github/workflows/backup.yml
name: Weekly Backup
on:
  schedule:
    - cron: '0 0 * * 0'  # Domingos a medianoche
jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Backup S3 to GitHub
        run: |
          aws s3 sync s3://alexnotes-blog-2026 ./backup
          tar -czf backup-$(date +%Y%m%d).tar.gz backup/
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: backup
          path: backup-*.tar.gz
```

---

## 📊 Analytics y Monitorización

### 16. Google Analytics o Plausible

Añade tracking (si te interesa ver qué contenido es más popular):

- **Google Analytics**: Clásico pero completo
- **Plausible**: Privacy-friendly, más simple
- **Umami**: Self-hosted, open source

Integración en `myst.yml`:
```yaml
site:
  analytics:
    google: "G-XXXXXXXXXX"
```

### 17. RSS Feed para suscriptores

Genera un `feed.xml` automáticamente para que otros puedan seguir tus notas:

```python
# scripts/generate_rss.py
# Genera RSS basado en los archivos .md con fecha
```

---

## 🎯 Prioridades Recomendadas

### Corto plazo (1-2 sesiones)
1. ✅ **Reorganizar estructura** de carpetas por temas
2. ✅ **Crear script** `new_note.py` para facilitar creación
3. ✅ **Añadir Makefile** para comandos rápidos
4. ✅ **Mejorar index.md** con últimas notas

### Medio plazo
5. **CloudFront + HTTPS** para mejor rendimiento
6. **Sistema de tags** y páginas índice
7. **Cambiar tema** a algo más blog-like
8. **Pre-commit hooks** para validación

### Largo plazo
9. Analytics si te interesa
10. Dominio personalizado
11. Comentarios (Giscus, utterances)

---

## 🤔 Alternativas a Considerar

Si encuentras limitaciones con Jupyter Book, considera:

1. **Quarto**: Similar pero más flexible, mejor para blogs
   - Soporta Python, R, Julia, Observable
   - Themes más modernos out-of-the-box
   - Mejor integración con blogs multi-categoría

2. **MkDocs Material**: Extremadamente popular
   - UI/UX excepcional
   - Plugins para tags, búsqueda, RSS
   - Muy customizable

3. **Docusaurus**: Si quieres algo muy moderno
   - React-based
   - Usado por Meta, Microsoft
   - Mejor para docs técnicas

---

¿Qué mejoras te interesan más? Puedo ayudarte a implementar cualquiera de estas.
