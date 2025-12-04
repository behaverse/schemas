# Behaverse Schemas - Documentation Branch

This branch contains the **documentation website infrastructure** for Behaverse schemas.

## Branch Purpose

- **`main` branch**: Contains only schema definitions (YAML/JSON files)
- **`gh-pages` branch**: Contains documentation generation and deployment code

## Structure

```
gh-pages/
├── docs/                      # Docusaurus documentation site
├── scripts/generate_docs.py   # Documentation generator
└── .github/workflows/         # CI/CD for docs deployment
```

## How It Works

1. CI workflow checks out schemas from `main` branch
2. Generates documentation pages from schema definitions
3. Builds Docusaurus static site
4. Deploys to GitHub Pages

## Local Development

```bash
# Checkout this branch
git checkout gh-pages

# Generate docs (fetches schemas from main)
git checkout main -- bcsvw/ collection/ dataset/ studyflow/
uv run scripts/generate_docs.py

# Start dev server
cd docs
npm install
npm start
```

## Deployment

Documentation automatically deploys to https://behaverse.org/schemas/ on every push to this branch.

---

**Note**: Schema files are maintained in the `main` branch. This branch only contains the documentation infrastructure.
