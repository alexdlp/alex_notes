# Alex's Notes

Blog personal de notas, apuntes y experimentos técnicos construido con Quarto y desplegado automáticamente en AWS S3.

## 🎯 Qué es esto

Mis notas personales sobre machine learning, matemáticas, finanzas y lo que me resulte interesante. Sin orden particular, sin categorías predefinidas. Solo escribo cuando algo me cuesta entender o cuando quiero documentar algo para no olvidarlo.

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

Crea archivos `.qmd` (Quarto Markdown) o `.ipynb` en `site/posts/`:

```bash
# Crear un nuevo post
touch site/posts/mi-nueva-nota.qmd
```

Estructura básica de un post:

```markdown
---
title: "Título de mi nota"
description: "Breve descripción"
author: "Alex de la Puente"
date: "2026-01-25"
categories: [machine-learning, matematicas]
---

## Contenido

Tu contenido aquí...

\```{python}
# Código ejecutable (opcional, requiere Python)
print("Hola mundo")
\```
```

### 2. Previsualizar localmente

```bash
# Desde el directorio site/
cd site
quarto preview

# Esto abre automáticamente http://localhost:4200
# Los cambios se reflejan automáticamente
```

O construir sin servidor:

```bash
cd site
quarto render
open ../_site/index.html
```

### 3. Publicar cambios

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
├── site/               # Todo el contenido de Quarto
│   ├── _quarto.yml     # Configuración principal
│   ├── index.qmd       # Página de inicio (lista posts automáticamente)
│   ├── styles.css      # Estilos personalizados
│   └── posts/          # Tus posts/notas (.qmd o .ipynb)
│       └── vae-elbo-loss.qmd
├── infra/              # Infraestructura Terraform
│   ├── main.tf
│   ├── s3.tf
│   └── variables.tf
├── .github/workflows/
│   └── deploy.yml      # CI/CD automático
├── _site/              # Salida de construcción (ignorado en git)
├── README.md
└── pyproject.toml
```

## 🔧 Comandos útiles

```bash
# Servidor de desarrollo con hot-reload
cd site && quarto preview

# Construir el sitio
cd site && quarto render

# Limpiar builds anteriores
rm -rf _site site/.quarto _freeze

# Ver logs de Terraform
cd infra && terraform show

# Sincronizar manualmente a S3 (si no quieres esperar al CI)
cd site && quarto render && aws s3 sync ../_site s3://alexnotes-blog-2026 --region eu-west-1 --delete

# Validar sintaxis de un archivo
quarto check site/posts/mi-post.qmd
```

## 🎨 Personalización

### Cambiar el tema

Edita `site/_quarto.yml`:

```yaml
format:
  html:
    theme:
      light: cosmo    # Opciones: flatly, minty, pulse, sandstone, etc.
      dark: darkly    # Para modo oscuro automático
```

Temas disponibles: https://quarto.org/docs/output-formats/html-themes.html

### Estilos personalizados

Edita `site/styles.css` para cambiar colores, fuentes, etc.

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
