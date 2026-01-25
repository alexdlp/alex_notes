# Alex's Notes

Blog personal de notas, apuntes y experimentos técnicos construido con MyST (Markedly Structured Text) y desplegado automáticamente en AWS S3.

## Qué es esto

Este repositorio contiene mis notas personales sobre estudios, aprendizajes y desarrollos varios. Está diseñado como un blog de notas más que como un libro tradicional, con contenido variado y no necesariamente estructurado de forma lineal.

El sitio se construye automáticamente y se despliega en AWS S3 cada vez que hago push a `main`.

## Cómo empezar

### Requisitos previos

- Python 3.12+ (usa `uv` o `pip`)
- Terraform (solo para infraestructura)
- AWS CLI configurado (solo para despliegue manual)

### Instalación local

```bash
# Con uv (recomendado)
uv sync

# O con pip
pip install -e .
```

## Flujo de trabajo habitual

### 1. Añadir nuevo contenido

Crea archivos `.md` o `.ipynb` en el directorio raíz o en subcarpetas organizadas por tema:

```bash
# Ejemplo de estructura que podrías usar
mkdir -p topics/machine-learning
touch topics/machine-learning/intro.md
```

Edita el contenido usando Markdown o Jupyter notebooks.

### 2. Previsualizar localmente

```bash
# Construir el sitio
jupyter-book build --html

# Abrir en el navegador
open _build/html/index.html
```

Para desarrollo activo, MyST también permite servidor local:

```bash
myst start
```

### 3. Actualizar la tabla de contenidos

Edita `myst.yml` para añadir nuevas páginas a la navegación. La estructura actual es:

```yaml
site:
  template: book-theme
```

Puedes añadir secciones manualmente en `myst.yml` o dejar que MyST auto-descubra el contenido.

### 4. Publicar cambios

```bash
git add .
git commit -m "Añade notas sobre [tema]"
git push origin main
```

El workflow de GitHub Actions (`deploy.yml`) se encargará de:
1. Instalar dependencias
2. Construir el sitio con `jupyter-book build --html`
3. Sincronizar `_build/html/` a S3
4. El sitio estará disponible en la URL del bucket S3

## Infraestructura

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

## Estructura del proyecto

```
.
├── infra/              # Infraestructura Terraform
│   ├── main.tf         # Provider AWS
│   ├── s3.tf           # Bucket S3 y configuración
│   └── variables.tf    # Variables (región, nombre)
├── .github/workflows/
│   └── deploy.yml      # CI/CD automático
├── myst.yml            # Configuración de MyST
├── pyproject.toml      # Dependencias Python
├── index.md            # Página de inicio
└── _build/             # Salida de construcción (ignorado en git)
```

## Comandos útiles

```bash
# Construir el sitio
jupyter-book build --html

# Limpiar builds anteriores
jupyter-book clean .

# Servidor de desarrollo MyST
myst start

# Ver logs de Terraform
cd infra && terraform show

# Sincronizar manualmente a S3 (si no quieres esperar al CI)
aws s3 sync _build/html s3://alexnotes-blog-2026 --region eu-west-1
```

## Personalización

### Cambiar el tema

Edita `myst.yml`:

```yaml
site:
  template: book-theme  # Otras opciones: article-theme
  options:
    favicon: favicon.ico
    logo: site_logo.png
```

### Metadatos del proyecto

También en `myst.yml`:

```yaml
project:
  title: Alex's notes
  description: My personal notes and experiments
  authors:
    - name: Alex de la Puente
```

## Troubleshooting

**Error al construir**: Asegúrate de tener todas las dependencias instaladas
```bash
uv sync  # o pip install -e .
```

**El workflow falla**: Revisa los secretos de AWS en GitHub Actions

**Cambios no se reflejan**: Limpia el cache de construcción
```bash
jupyter-book clean .
jupyter-book build --html
```

## 📚 Recursos

- [MyST Documentation](https://mystmd.org/)
- [Jupyter Book Guide](https://jupyterbook.org/)
- [MyST Markdown Syntax](https://mystmd.org/guide/syntax-overview)

---

**Última actualización**: Enero 2026
