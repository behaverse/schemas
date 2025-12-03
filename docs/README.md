# Behaverse Schemas Documentation

This directory contains the Docusaurus-based documentation site for Behaverse schemas.

## Overview

The documentation is **auto-generated** from the schema definitions in:
- `collection/field-definitions.yaml`
- `dataset/field-definitions.yaml`
- `bcsvw/schema.json`
- `studyflow/schema.moddle.json`

## Quick Start

### Prerequisites

- Python 3.10+ with [uv](https://github.com/astral-sh/uv)
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install Node.js dependencies
cd docs
npm install

# Generate documentation from schemas
cd ..
uv run scripts/generate_docs.py
```

### Development

```bash
# Start development server
cd docs
npm start
```

This will open the site at `http://localhost:3000`. The site will hot-reload when you make changes.

### Build for Production

```bash
# Generate docs from schemas
uv run scripts/generate_docs.py

# Build static site
cd docs
npm run build

# Serve the built site
npm run serve
```

## How It Works

1. **`scripts/generate_docs.py`** reads schema definitions and generates:
   - Index pages for each schema
   - Individual property pages (e.g., `/dataset/name`, `/collection/inclusion_criteria`)
   - Sidebar configuration (`docs/sidebars.js`)

2. **Docusaurus** builds a static React site with:
   - Search functionality (Algolia)
   - Navigation across all 4 schemas
   - Responsive design
   - Dark mode support

3. **GitHub Actions** automatically:
   - Generates docs on every push
   - Builds and deploys to GitHub Pages
   - Available at `https://behaverse.org/schemas/`

## Customization

### Theme

Edit `docs/src/css/custom.css` to customize colors and styles.

### Configuration

Edit `docs/docusaurus.config.js` to change:
- Site metadata
- Navigation items
- Footer links
- Search settings (Algolia)

### Content

- **Schema READMEs**: Convert existing `README.md` files to MDX format in `docs/docs/<schema>/`
- **Examples**: Add example pages in `docs/docs/<schema>/examples/`
- **Custom pages**: Add any additional MDX files as needed

## Directory Structure

```
docs/
├── docs/                      # Documentation content (auto-generated + manual)
│   ├── bcsvw/
│   │   ├── index.md          # Auto-generated
│   │   ├── ordered.md        # Auto-generated property page
│   │   └── examples/         # Manual examples
│   ├── collection/
│   ├── dataset/
│   └── studyflow/
├── src/
│   └── css/
│       └── custom.css        # Custom styling
├── static/                    # Static assets (images, etc.)
├── docusaurus.config.js      # Main configuration
├── sidebars.js               # Auto-generated sidebar config
└── package.json              # Node.js dependencies
```

## Workflow

### Adding a New Property

1. Add the property to `<schema>/field-definitions.yaml`
2. Run `uv run <schema>/scripts/generate_schema_files.py` to update `schema.json`
3. Run `uv run scripts/generate_docs.py` to generate documentation
4. Commit and push - GitHub Actions will deploy automatically

### Updating Documentation

```bash
# 1. Update schema definitions
vim dataset/field-definitions.yaml

# 2. Regenerate schema files
uv run dataset/scripts/generate_schema_files.py

# 3. Regenerate documentation
uv run scripts/generate_docs.py

# 4. Preview changes
cd docs && npm start

# 5. Commit and push
git add .
git commit -m "docs: update dataset schema"
git push
```

## Search Configuration

The site uses Algolia DocSearch for search functionality. To enable:

1. Apply for Algolia DocSearch (free for open source)
2. Update `algolia` configuration in `docusaurus.config.js` with your credentials
3. Algolia will crawl the site and index content

Alternatively, use local search plugins for offline search capability.

## Deployment

The site automatically deploys to GitHub Pages on every push to `main` via GitHub Actions (`.github/workflows/deploy-docs.yml`).

### Manual Deployment

```bash
# Build the site
cd docs
npm run build

# Deploy to GitHub Pages
GIT_USER=<your-github-username> npm run deploy
```

## License

Documentation is licensed under CC BY 4.0, same as the schemas.
