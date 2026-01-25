# 💡 Propuestas de Mejora para Alex's Notes

## ✅ Migración a Quarto completada

El proyecto ha sido migrado exitosamente de Jupyter Book a Quarto. Esto ya soluciona muchos de los problemas de diseño y organización que tenía el proyecto original:

- ✅ Tema más orientado a blog
- ✅ Sistema de categorías automático
- ✅ Listados de posts por fecha
- ✅ Búsqueda integrada
- ✅ Modo oscuro/claro automático

## 🎨 Apariencia y Diseño

### 1. Añadir un logo y favicon personalizados
Crea una carpeta `assets/` y añade:
- `logo.png` (recomendado: 200x50px)
- `favicon.ico` (16x16px y 32x32px)

Luego actualiza `_quarto.yml`:
```yaml
website:
  favicon: assets/favicon.ico
  navbar:
    logo: assets/logo.png
```

### 2. Añadir listado de "Últimas notas" en la home

Actualmente `index.qmd` es estático. Puedes añadir un listado automático:

```yaml
---
title: "Alex's Notes"
listing:
  contents: posts
  sort: "date desc"
  max-items: 5
  type: grid
  fields: [title, date, description, categories]
---
```

### 3. Probar diferentes temas

Quarto tiene muchos temas built-in. Edita `_quarto.yml`:

```yaml
format:
  html:
    theme:
      light: [cosmo, custom.scss]  # Prueba: flatly, minty, pulse
      dark: [darkly, custom.scss]   # Prueba: cyborg, slate, superhero
```

Lista completa: https://quarto.org/docs/output-formats/html-themes.html

---

## 📂 Estructura y Organización

### 4. Añadir imágenes destacadas a los posts

Las imágenes hacen los listados más atractivos:

```markdown
---
title: "Mi Post"
image: "thumbnail.jpg"  # Imagen en el mismo directorio que el post
---
```

O usa imágenes remotas:
```markdown
image: "https://unsplash.com/photos/..."
```

---

## 🚀 Funcionalidades Técnicas

### 5. Mejorar el workflow de GitHub Actions

**Optimizaciones sugeridas**:

```yaml
# .github/workflows/deploy.yml
- name: Cache Quarto
  uses: actions/cache@v4
  with:
    path: ~/.quarto
    key: ${{ runner.os }}-quarto-${{ hashFiles('_quarto.yml') }}

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

### 6. RSS Feed automático

Quarto puede generar RSS feeds automáticamente. Añade a `_quarto.yml`:

```yaml
website:
  site-url: "http://alexnotes-blog-2026.s3-website-eu-west-1.amazonaws.com"
  rss:
    items: 20
    image: "assets/logo.png"
```

Esto genera automáticamente `index.xml` que los lectores RSS pueden suscribirse.

---

## 📝 Calidad de Vida

### 7. Script de creación rápida de notas

Crea `scripts/new_post.py`:

```python
#!/usr/bin/env python3
import sys
from datetime import datetime
from pathlib import Path

def create_post(title, categories=""):
    slug = title.lower().replace(" ", "-")
    date = datetime.now().strftime("%Y-%m-%d")

    posts_dir = Path("posts")
    posts_dir.mkdir(exist_ok=True)

    post_path = posts_dir / f"{slug}.qmd"

    cats = [f'"{c.strip()}"' for c in categories.split(",")] if categories else []
    cats_str = f"[{', '.join(cats)}]" if cats else "[]"

    content = f"""---
title: "{title}"
description: ""
author: "Alex de la Puente"
date: "{date}"
categories: {cats_str}
---

## Introducción

Escribe tu contenido aquí...
"""

    post_path.write_text(content)
    print(f"✅ Post creado: {post_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/new_post.py '<título>' '[categorías]'")
        print("Ejemplo: python scripts/new_post.py 'Mi nota' 'machine-learning,python'")
        sys.exit(1)

    title = sys.argv[1]
    categories = sys.argv[2] if len(sys.argv) > 2 else ""
    create_post(title, categories)
```

Uso:
```bash
python scripts/new_post.py "Introducción a Transformers" "machine-learning,python"
```

### 8. Makefile para comandos comunes

Crea `Makefile`:

```makefile
.PHONY: preview build clean deploy new

preview:
	quarto preview

build:
	quarto render

clean:
	rm -rf _site .quarto

deploy: build
	aws s3 sync _site s3://alexnotes-blog-2026 --region eu-west-1 --delete

new:
	@read -p "Título: " title; \
	read -p "Categorías (separadas por coma): " cats; \
	python scripts/new_post.py "$$title" "$$cats"
```

Uso: `make preview`, `make deploy`, `make new`, etc.

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

### 9. Google Analytics

Quarto integra fácilmente con Google Analytics. Añade a `_quarto.yml`:

```yaml
website:
  google-analytics: "G-XXXXXXXXXX"
```

Alternativas privacy-friendly:
- **Plausible**: Añade script en `include-in-header`
- **Umami**: Self-hosted, open source

### 10. Comentarios con Giscus

Añade sistema de comentarios usando GitHub Discussions. En `_quarto.yml`:

```yaml
format:
  html:
    comments:
      giscus:
        repo: tu-usuario/tu-repo
```

Esto añade automáticamente comentarios en cada post usando GitHub Discussions.

---

## 🎯 Prioridades Recomendadas

### Corto plazo (1-2 sesiones)
1. ✅ **Migración a Quarto** - COMPLETADO
2. **Crear script** `new_post.py` para facilitar creación de posts
3. **Añadir Makefile** para comandos rápidos
4. **Logo y favicon** personalizados
5. **Mejorar index.qmd** con listado de últimas notas

### Medio plazo
6. **CloudFront + HTTPS** para mejor rendimiento y dominio personalizado
7. **RSS Feed** automático
8. **Pre-commit hooks** para validación
9. **Probar diferentes temas** de Quarto

### Largo plazo
10. **Analytics** si te interesa
11. **Dominio personalizado** (notes.alexdelapuente.com)
12. **Comentarios** (Giscus con GitHub Discussions)
13. **Búsqueda avanzada** con Algolia o similar

---

## 🎉 Ventajas de usar Quarto

Ya que migramos a Quarto, ahora tienes:

1. ✅ **Sistema de categorías automático** - No necesitas gestionar índices manualmente
2. ✅ **Listados por fecha** - Los posts se ordenan automáticamente
3. ✅ **Búsqueda integrada** - Búsqueda funciona out-of-the-box
4. ✅ **Temas modernos** - Muchas opciones de diseño
5. ✅ **Código ejecutable** - Soporta Python, R, Julia, Observable
6. ✅ **Modo oscuro/claro** - Automático según preferencias del sistema
7. ✅ **Responsive** - Se ve bien en móvil, tablet y desktop
8. ✅ **Markdown enriquecido** - LaTeX, callouts, tabsets, etc.
9. ✅ **Fast refresh** - Cambios se ven instantáneamente con `quarto preview`

## 🔄 Comparación con alternativas

Si en el futuro quieres explorar otras opciones:

- **MkDocs Material**: Mejor para documentación de software/APIs
- **Docusaurus**: Si necesitas algo muy React-heavy
- **Hugo**: Si quieres velocidad extrema (pero menos features para código)

Pero Quarto es ideal para tu caso: blog técnico con código ejecutable.

---

¿Qué mejoras te interesan más? Puedo ayudarte a implementar cualquiera de estas.
