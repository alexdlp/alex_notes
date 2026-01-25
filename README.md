# Alex's Notes

Blog personal de notas, apuntes y experimentos técnicos construido con Quarto y desplegado automáticamente en AWS S3.

## 🎯 Qué es esto

Este repositorio contiene mis notas personales sobre Machine Learning, Finanzas, Desarrollo y otros temas. Está diseñado como un blog personal con contenido variado organizado por categorías, sin necesidad de seguir un orden lineal.

El sitio se construye automáticamente con Quarto y se despliega en AWS S3 cada vez que hago push a `main`.

## 🚀 Cómo empezar

### Requisitos previos

- **Quarto CLI** ([descargar](https://quarto.org/docs/get-started/))
- Python 3.12+ (opcional, solo si usas código ejecutable en posts)
- Terraform (solo para infraestructura)
- AWS CLI configurado (solo para despliegue manual)

### Instalación

```bash
# Instalar Quarto (macOS)
brew install quarto

# O descarga desde https://quarto.org/docs/get-started/

# Verificar instalación
quarto --version
```

## 📝 Flujo de trabajo habitual

### 1. Añadir nuevo contenido

Crea archivos `.qmd` (Quarto Markdown) o `.ipynb` en el directorio `posts/`:

```bash
# Crear un nuevo post
touch posts/mi-nueva-nota.qmd
```

Estructura básica de un post:

```markdown
---
title: "Título de mi nota"
description: "Breve descripción"
author: "Alex de la Puente"
date: "2026-01-25"
categories: [machine-learning, python]
---

## Introducción

Tu contenido aquí...

\```{python}
# Código ejecutable (opcional)
print("Hola mundo")
\```
```

Categorías disponibles:
- `machine-learning` → Aparece en /ml
- `finanzas` → Aparece en /finance
- `desarrollo` → Aparece en /dev

### 2. Previsualizar localmente

```bash
# Servidor de desarrollo (con hot-reload)
quarto preview

# Esto abre automáticamente http://localhost:4200
# Los cambios se reflejan automáticamente
```

O construir sin servidor:

```bash
# Solo construir
quarto render

# Abrir resultado
open _site/index.html
```

### 3. Organización automática

**No necesitas actualizar ningún índice manualmente.** Quarto descubre automáticamente:

- Todos los posts en `posts/` → Aparecen en `/posts.html`
- Posts con categoría `machine-learning` → Aparecen en `/ml`
- Posts con categoría `finanzas` → Aparecen en `/finance`
- Posts con categoría `desarrollo` → Aparecen en `/dev`

Los listados se ordenan automáticamente por fecha (más reciente primero).

### 4. Publicar cambios

```bash
git add .
git commit -m "Añade notas sobre [tema]"
git push origin main
```

El workflow de GitHub Actions (`deploy.yml`) se encargará de:
1. Instalar Quarto
2. Renderizar el sitio con `quarto render`
3. Sincronizar `_site/` a S3
4. El sitio estará disponible en la URL del bucket S3

## 🏗️ Infraestructura

### Desplegar infraestructura inicial

La primera vez, o si necesitas recrear la infraestructura:

```bash
cd infra/
terraform init
terraform plan
terraform apply
```

Esto crea:
- Bucket S3: `alexnotes-blog-2026`
- Configuración de website estático
- Política pública de lectura
- Región: `eu-west-1`

### Configurar secretos en GitHub

Para que el workflow funcione, configura estos secretos en tu repositorio:

1. Ve a Settings > Secrets and variables > Actions
2. Añade:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### URL del sitio

Una vez desplegado, el sitio estará en:
```
http://alexnotes-blog-2026.s3-website-eu-west-1.amazonaws.com
```

## 📁 Estructura del proyecto

```
.
├── posts/              # Tus posts/notas (archivos .qmd o .ipynb)
│   ├── ejemplo-ml.qmd
│   ├── ejemplo-finanzas.qmd
│   └── ejemplo-desarrollo.qmd
├── ml/                 # Página índice de Machine Learning
│   └── index.qmd
├── finance/            # Página índice de Finanzas
│   └── index.qmd
├── dev/                # Página índice de Desarrollo
│   └── index.qmd
├── infra/              # Infraestructura Terraform
│   ├── main.tf
│   ├── s3.tf
│   └── variables.tf
├── .github/workflows/
│   └── deploy.yml      # CI/CD automático
├── _quarto.yml         # Configuración principal de Quarto
├── index.qmd           # Página de inicio
├── posts.qmd           # Listado de todos los posts
├── styles.css          # Estilos personalizados
└── _site/              # Salida de construcción (ignorado en git)
```

## 🔧 Comandos útiles

```bash
# Servidor de desarrollo con hot-reload
quarto preview

# Construir el sitio
quarto render

# Limpiar builds anteriores
rm -rf _site .quarto

# Ver logs de Terraform
cd infra && terraform show

# Sincronizar manualmente a S3 (si no quieres esperar al CI)
quarto render && aws s3 sync _site s3://alexnotes-blog-2026 --region eu-west-1 --delete

# Validar sintaxis de un archivo
quarto check <archivo.qmd>
```

## 🎨 Personalización

### Cambiar el tema

Edita `_quarto.yml`:

```yaml
format:
  html:
    theme:
      light: cosmo    # Opciones: flatly, minty, pulse, sandstone, etc.
      dark: darkly    # Para modo oscuro automático
```

Temas disponibles: https://quarto.org/docs/output-formats/html-themes.html

### Añadir nueva categoría

1. Crea un directorio con `index.qmd`:

```bash
mkdir nueva-categoria
cat > nueva-categoria/index.qmd <<EOF
---
title: "Nueva Categoría"
listing:
  contents: ../posts
  include:
    categories: ["nueva-categoria"]
---
EOF
```

2. Añádela al navbar en `_quarto.yml`:

```yaml
navbar:
  left:
    - text: "Nueva Categoría"
      href: nueva-categoria/index.qmd
```

### Estilos personalizados

Edita `styles.css` para cambiar colores, fuentes, etc.

## 🐛 Troubleshooting

**Error: "quarto: command not found"**
```bash
# Verifica instalación
quarto --version

# Si no está instalado
brew install quarto
```

**Error al renderizar código Python**
```bash
# Asegúrate de tener Python y las librerías necesarias
pip install numpy pandas matplotlib jupyter

# O desactiva la ejecución en _quarto.yml:
execute:
  enabled: false
```

**El workflow de GitHub Actions falla**
- Revisa los secretos de AWS en Settings > Secrets and variables > Actions
- Verifica que tienes `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`

**Cambios no se reflejan en preview**
```bash
# Limpia el cache
rm -rf _site .quarto
quarto render
```

**Error: "Layout post not found"**
- Asegúrate de que los archivos en `posts/` tienen frontmatter válido
- Cada post debe tener al menos `title` y `date`

## 📚 Recursos

- [Quarto Documentation](https://quarto.org/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto Gallery](https://quarto.org/docs/gallery/) - Ejemplos de sitios
- [Markdown Basics](https://quarto.org/docs/authoring/markdown-basics.html)
- [Publishing to S3](https://quarto.org/docs/publishing/other.html#amazon-s3)

## 🚀 Próximos pasos sugeridos

Ver `MEJORAS.md` para propuestas de mejoras como:
- CloudFront para HTTPS
- Dominio personalizado
- Analytics
- Sistema de comentarios
- RSS feed automático

---

**Última actualización**: Enero 2026
