#!/usr/bin/env python3
"""
Generate Docusaurus MDX documentation from schema definitions

This script reads field-definitions.yaml and schema.json files from each schema
directory and generates comprehensive MDX documentation pages for Docusaurus.

AUTOMATICALLY GENERATED FILES (DO NOT EDIT MANUALLY):
- docs/docs/{schema}/index.md - Overview page with all properties
- docs/docs/{schema}/{property}.md - Individual property pages
- docs/docs/{schema}/{object}/{property}.md - Nested object property pages
- docs/sidebars.js - Navigation sidebar configuration

MANUALLY EDITABLE FILES:
- docs/docs/{schema}/about.md - Schema motivation and features
- docs/docs/{schema}/examples.md - Usage examples
- docs/docusaurus.config.js - Site configuration
- docs/src/css/custom.css - Styling

Usage:
    uv run scripts/generate_docs.py
    uv run scripts/generate_docs.py --check  # Dry run
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys

# Schema directories to process
SCHEMAS = {
    'bcsvw': {
        'has_field_definitions': False,  # Uses schema.json directly
        'name': 'bcsvw (Behaverse CSV for the Web)',
        'icon': 'schema_B.png',
    },
    'collection': {
        'has_field_definitions': True,
        'name': 'Collection Schema',
        'icon': 'schema_C.png',
    },
    'dataset': {
        'has_field_definitions': True,
        'name': 'Dataset Schema',
        'icon': 'schema_D.png',
    },
    'studyflow': {
        'has_field_definitions': False,  # Uses moddle/linkml format
        'name': 'Studyflow Schema',
        'icon': 'schema_S.png',
    },
}

def load_schema_data(schema_name: str) -> Dict[str, Any]:
    """Load schema data from field-definitions.yaml or schema.json"""
    schema_dir = Path(__file__).parent.parent / schema_name
    
    schema_info = SCHEMAS[schema_name]
    
    if schema_info['has_field_definitions']:
        # Load from field-definitions.yaml
        definitions_path = schema_dir / 'field-definitions.yaml'
        with open(definitions_path, 'r') as f:
            data = yaml.safe_load(f)
        return {
            'metadata': data['schema_metadata'],
            'fields': data['fields'],
            'field_groups': data.get('field_groups', []),
        }
    elif schema_name == 'studyflow':
        # Load from moddle format
        moddle_path = schema_dir / 'schema.moddle.json'
        if not moddle_path.exists():
            # Skip studyflow if schema.moddle.json doesn't exist
            return None
        with open(moddle_path, 'r') as f:
            moddle = json.load(f)
        return {
            'metadata': {
                'name': moddle.get('name', 'Studyflow Schema'),
                'version': '25.0414',  # From README
                'namespace': moddle.get('uri', 'https://behaverse.org/schemas/studyflow'),
                'description': 'Schema for defining the formal structure of studyflow diagrams',
            },
            'fields': convert_moddle_to_fields(moddle),
            'field_groups': [],
        }
    else:
        # Load from schema.json
        schema_path = schema_dir / 'schema.json'
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Read version from schema file
        # First try direct version field, then extract from $id URL
        version = schema.get('version', '')
        if not version and '$id' in schema:
            # Extract version from $id URL (e.g., .../dataset/v25.1201/schema.json)
            id_parts = schema['$id'].split('/')
            for part in id_parts:
                if part.startswith('v') and any(c.isdigit() for c in part):
                    version = part[1:]  # Remove 'v' prefix
                    break
        
        return {
            'metadata': {
                'name': schema.get('title', schema_name),
                'version': version,
                'namespace': schema.get('$id', '').rsplit('/', 1)[0] if '$id' in schema else f'https://behaverse.org/schemas/{schema_name}',
                'description': schema.get('description', ''),
            },
            'fields': convert_json_schema_to_fields(schema),
            'field_groups': [],
        }

def convert_json_schema_to_fields(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert JSON Schema properties to field definitions format"""
    fields = []
    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])
    
    # Process top-level properties
    for prop_name, prop_def in properties.items():
        field = {
            'name': prop_name,
            'type': prop_def.get('type', 'string'),
            'description': prop_def.get('description', ''),
            'status': 'required' if prop_name in required_fields else 'optional',
        }
        
        # Add mappings if equivalentProperty exists
        if 'equivalentProperty' in prop_def:
            equiv = prop_def['equivalentProperty']
            if isinstance(equiv, str):
                equiv = [equiv]
            field['mappings'] = [{'url': url, 'standard': 'external'} for url in equiv]
        
        # Add constraints
        constraints = {}
        for key in ['pattern', 'format', 'minimum', 'minLength', 'enum']:
            if key in prop_def:
                constraints[key] = prop_def[key]
        if constraints:
            field['constraints'] = constraints
        
        fields.append(field)
    
    # For bcsvw, also extract column properties from definitions
    if 'definitions' in schema and 'column' in schema['definitions']:
        column_def = schema['definitions']['column']
        if 'properties' in column_def:
            column_props = column_def['properties']
            column_required = column_def.get('required', [])
            
            # Skip camelCase versions if snake_case equivalent exists
            # (e.g., skip minLength if min_length exists)
            camelcase_to_skip = set()
            for prop_name in column_props.keys():
                # Check if this is a snake_case version of a camelCase property
                if '_' in prop_name:
                    # Convert to camelCase to find the original
                    parts = prop_name.split('_')
                    camelcase = parts[0] + ''.join(word.capitalize() for word in parts[1:])
                    if camelcase in column_props:
                        camelcase_to_skip.add(camelcase)
            
            for col_prop_name, col_prop_def in column_props.items():
                # Skip camelCase properties that have snake_case equivalents
                if col_prop_name in camelcase_to_skip:
                    continue
                
                # Determine type
                prop_type = col_prop_def.get('type', 'string')
                if 'enum' in col_prop_def:
                    prop_type = 'enum'
                elif 'oneOf' in col_prop_def:
                    # Get the most common type from oneOf
                    types = [item.get('type') for item in col_prop_def['oneOf'] if 'type' in item]
                    prop_type = types[0] if types else 'string'
                
                field = {
                    'name': col_prop_name,
                    'type': prop_type,
                    'description': col_prop_def.get('description', ''),
                    'requirement': 'required' if col_prop_name in column_required else 'optional',
                    'context': 'column',  # Mark as column property
                }
                
                # Add constraints
                constraints = {}
                for key in ['pattern', 'format', 'minimum', 'maximum', 'minLength', 'maxLength', 'enum', 'minItems']:
                    if key in col_prop_def:
                        constraints[key] = col_prop_def[key]
                
                # Handle items for array types
                if prop_type == 'array' and 'items' in col_prop_def:
                    items_def = col_prop_def['items']
                    if 'type' in items_def:
                        field['item_type'] = items_def['type']
                    if 'enum' in items_def:
                        constraints['items_enum'] = items_def['enum']
                
                if constraints:
                    field['constraints'] = constraints
                
                fields.append(field)
    
    return fields

def convert_moddle_to_fields(moddle: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert moddle format to field definitions format (simplified for studyflow)"""
    # For studyflow, we'll create minimal documentation pointing to main docs
    fields = []
    
    # Add types from moddle
    for type_def in moddle.get('types', []):
        field = {
            'name': type_def.get('name', 'unknown'),
            'type': 'element',
            'description': type_def.get('description', 'Studyflow element type'),
            'requirement': 'optional',
        }
        fields.append(field)
    
    return fields

def generate_status_badge(status: str) -> str:
    """Generate MDX badge component for field status"""
    status_lower = status.lower()
    badge_class = status_lower
    if status_lower in ['required', 'recommended', 'optional']:
        return f'<span className="property-badge {badge_class}">{status.upper()}</span>'
    return ''

def generate_property_page(field: Dict[str, Any], metadata: Dict[str, Any], schema_name: str) -> str:
    """Generate MDX documentation page for a single property"""
    
    # Extract field information
    name = field['name']
    description = field.get('description', 'No description available.')
    field_type = field.get('type', 'string')
    requirement = field.get('requirement', 'optional')
    parent_property = field.get('parent_property', None)
    
    # Escape special characters in YAML front matter
    # YAML reserved words that need quoting
    yaml_reserved = ['null', 'true', 'false', 'yes', 'no', 'on', 'off']
    
    safe_name = name
    safe_title = name
    sidebar_label = name
    
    if name.startswith('@') or name.lower() in yaml_reserved:
        # Quote values with @ or YAML reserved words to prevent YAML parsing errors
        safe_name = f'"{name}"'
        safe_title = f'"{name}"'
        sidebar_label = f'"{name}"'
    
    # Build the MDX content with parent context if this is a nested property
    parent_note = ""
    if parent_property:
        parent_note = f"\n:::info\nThis property is part of the [`{parent_property}`](../{parent_property}) object.\n:::\n"
    
    mdx = f"""---
id: {safe_name}
title: {safe_title}
sidebar_label: {sidebar_label}
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# {name}

{generate_status_badge(requirement)}

{description}
{parent_note}

## Details

<div className="property-details">

| Property | Value |
|:---------|:------|
| **Type** | `{field_type}` |
| **Requirement** | {requirement.lower()} |
| **Namespace URI** | <code className="namespace-uri">{metadata['namespace']}#{name}</code> |

</div>
"""
    
    # Add mappings section if available
    # if 'mappings' in field and field['mappings']:
    #     mdx += "\n## Equivalent Properties\n\n"
    #     mdx += "<div className=\"mappings-section\">\n\n"
    #     mdx += "This property maps to the following standard vocabularies:\n\n"
    #     for mapping in field['mappings']:
    #         standard = mapping.get('standard', 'external')
    #         url = mapping.get('url', '')
    #         property_name = mapping.get('property', url.split('#')[-1].split('/')[-1])
    #         mdx += f"- **{standard}**: [`{property_name}`]({url})\n"
    #     mdx += "\n</div>\n"
    
    # Add constraints section if available
    if 'constraints' in field:
        mdx += "\n## Constraints\n\n"
        constraints = field['constraints']
        if 'pattern' in constraints:
            mdx += f"- **Pattern**: `{constraints['pattern']}`\n"
        if 'format' in constraints:
            mdx += f"- **Format**: `{constraints['format']}`\n"
        if 'minimum' in constraints:
            mdx += f"- **Minimum**: `{constraints['minimum']}`\n"
        if 'min_length' in constraints:
            mdx += f"- **Minimum Length**: `{constraints['min_length']}`\n"
        if 'enum' in constraints:
            mdx += f"- **Allowed Values**: {', '.join(f'`{v}`' for v in constraints['enum'])}\n"
    
    # Add examples section if available
    if 'examples' in field and field['examples']:
        mdx += "\n## Examples\n\n"
        mdx += "<div className=\"examples-section\">\n\n"
        for i, example in enumerate(field['examples'], 1):
            if isinstance(example, str):
                mdx += f"```\n{example}\n```\n\n"
            else:
                mdx += f"```json\n{json.dumps(example, indent=2)}\n```\n\n"
        mdx += "</div>\n"
    
    # Add item type info for arrays
    if field_type == 'array' and 'item_type' in field:
        mdx += f"\n## Array Items\n\n"
        mdx += f"Each item in this array is of type: `{field['item_type']}`\n"
        
        if 'object_properties' in field:
            mdx += "\n### Object Properties\n\n"
            mdx += "| Property | Type | Description |\n"
            mdx += "|----------|------|-------------|\n"
            parent_name = field['name']
            for obj_prop in field['object_properties']:
                obj_name = obj_prop['name']
                obj_type = obj_prop['type']
                obj_desc = obj_prop.get('description', '')
                mdx += f"| [`{obj_name}`]({parent_name}/{obj_name}) | `{obj_type}` | {obj_desc} |\n"
    
    return mdx

def generate_index_page(schema_name: str, data: Dict[str, Any]) -> str:
    """Generate index/overview page for a schema"""
    metadata = data['metadata']
    fields = data['fields']
    field_groups = data.get('field_groups', [])
    
    # Format version string
    version_str = f"v{metadata['version']}" if metadata['version'] else "(not versioned)"
    
    # Use simple schema name as title
    page_title = schema_name
    
    # Get schema icon if available
    schema_icon = SCHEMAS.get(schema_name, {}).get('icon', '')
    icon_html = f"<img src={{require('@site/static/assets/img/{schema_icon}').default}} height=\"80\" style={{{{verticalAlign: 'middle'}}}} /> " if schema_icon else ""
    
    mdx = f"""---
id: index
title: {page_title}
sidebar_label: Overview
slug: /{schema_name}
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# {icon_html}{page_title}

**Version**: {version_str}  
**Namespace**: `{metadata['namespace']}`

{metadata['description']}

## Properties

This schema defines **{len(fields)} properties** for describing {schema_name} metadata.

"""
    
    # For bcsvw, separate table and column properties
    if schema_name == 'bcsvw':
        table_fields = [f for f in fields if f.get('context') != 'column']
        column_fields = [f for f in fields if f.get('context') == 'column']
        
        mdx += "### Table Properties\n\n"
        mdx += "| Property | Type | Requirement | Description |\n"
        mdx += "|:---------|:-----|:------------|:------------|\n"
        for field in table_fields:
            desc = field.get('description', '')[:80] + '...' if len(field.get('description', '')) > 80 else field.get('description', '')
            mdx += f"| [{field['name']}]({schema_name}/{field['name']}) | `{field['type']}` | {field.get('requirement', 'optional')} | {desc} |\n"
        
        mdx += "\n### Column Properties\n\n"
        mdx += "These properties are used within the `table_schema.columns` array to describe individual columns.\n\n"
        mdx += "| Property | Type | Requirement | Description |\n"
        mdx += "|:---------|:-----|:------------|:------------|\n"
        for field in column_fields:
            desc = field.get('description', '')[:80] + '...' if len(field.get('description', '')) > 80 else field.get('description', '')
            mdx += f"| [{field['name']}]({schema_name}/{field['name']}) | `{field['type']}` | {field.get('requirement', 'optional')} | {desc} |\n"
    elif field_groups:
        for group in field_groups:
            group_fields = [f for f in fields if f.get('group') == group['id']]
            if group_fields:
                mdx += f"### {group['name']}\n\n"
                mdx += f"{group.get('description', '')}\n\n"
                mdx += "| Property | Type | Requirement | Description |\n"
                mdx += "|:---------|:-----|:------------|:------------|\n"
                for field in group_fields:
                    desc = field.get('description', '')[:80] + '...' if len(field.get('description', '')) > 80 else field.get('description', '')
                    mdx += f"| [{field['name']}]({schema_name}/{field['name']}) | `{field['type']}` | {field.get('requirement', 'optional')} | {desc} |\n"
                
                mdx += "\n"
                
                # Add nested object properties documentation after the main table
                for field in group_fields:
                    if 'object_properties' in field and field['object_properties']:
                        parent_name = field['name']
                        mdx += f"#### {parent_name.replace('_', ' ').title()} Object\n\n"
                        mdx += f"Each {parent_name} in the `{parent_name}` array is an object with the following properties:\n\n"
                        mdx += "| Property | Type | Requirement | Description |\n"
                        mdx += "|:---------|:-----|:------------|:------------|\n"
                        for obj_prop in field['object_properties']:
                            obj_name = obj_prop['name']
                            obj_type = obj_prop['type']
                            obj_required = "required" if obj_prop.get('required', False) else "optional"
                            obj_desc = obj_prop.get('description', '')
                            # Add constraint info to description if present
                            if 'constraints' in obj_prop:
                                if 'pattern' in obj_prop['constraints']:
                                    pattern = obj_prop['constraints']['pattern'].replace('\\\\', '\\')
                                    # Format ORCID pattern nicely
                                    if 'orcid' in obj_name.lower():
                                        obj_desc += " (format: 0000-0000-0000-0000)"
                                elif 'format' in obj_prop['constraints']:
                                    obj_desc += f" (format: {obj_prop['constraints']['format']})"
                            mdx += f"| [{obj_name}]({schema_name}/{parent_name}/{obj_name}) | `{obj_type}` | {obj_required} | {obj_desc} |\n"
                        
                        # Add example for the parent field if available
                        if 'examples' in field and field['examples']:
                            mdx += f"\n**Example:**\n```json\n{{\n  \"{parent_name}\": "
                            import json
                            mdx += json.dumps(field['examples'][0], indent=2)
                            mdx += "\n}\n```\n"
                        mdx += "\n"
                mdx += "\n"
    else:
        mdx += "### All Properties\n\n"
        mdx += "| Property | Type | Requirement | Description |\n"
        mdx += "|:---------|:-----|:------------|:------------|\n"
        for field in fields:
            desc = field.get('description', '')[:80] + '...' if len(field.get('description', '')) > 80 else field.get('description', '')
            mdx += f"| [{field['name']}]({schema_name}/{field['name']}) | `{field['type']}` | {field.get('requirement', 'optional')} | {desc} |\n"
    
    # Update examples link for schemas with examples pages
    if schema_name in ['bcsvw', 'collection', 'dataset']:
        examples_link = f'[examples]({schema_name}/examples)'
    else:
        examples_link = f'[examples](./{schema_name}/examples)'
    
    mdx += f"""
## Usage

See the {examples_link} for practical usage patterns.

## Version History

The current version of `{schema_name}` is `{version_str}`.

Older versions are available in the [`{schema_name}/versions/`](https://github.com/behaverse/schemas/tree/main/{schema_name}/versions) directory.
"""
    
    return mdx

def generate_sidebar_config(schema_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate sidebar configuration for a schema"""
    fields = data['fields']
    field_groups = data.get('field_groups', [])
    
    sidebar = [
        {
            'type': 'doc',
            'id': f'{schema_name}/index',
            'label': 'Overview',
        }
    ]
    
    # Add about page for bcsvw, collection, and dataset
    if schema_name in ['bcsvw', 'collection', 'dataset']:
        sidebar.append({
            'type': 'doc',
            'id': f'{schema_name}/about',
            'label': 'About',
        })
    
    # Filter out JSON-LD keywords
    fields = [f for f in fields if not f['name'].startswith('@')]
    
    # For bcsvw, separate table-level and column-level properties
    if schema_name == 'bcsvw':
        table_fields = [f for f in fields if f.get('context') != 'column']
        column_fields = [f for f in fields if f.get('context') == 'column']
        
        if table_fields:
            sidebar.append({
                'type': 'category',
                'label': 'Table Properties',
                'collapsed': True,
                'items': [f"{schema_name}/{field['name']}" for field in table_fields]
            })
        
        if column_fields:
            sidebar.append({
                'type': 'category',
                'label': 'Column Properties',
                'collapsed': True,
                'items': [f"{schema_name}/{field['name']}" for field in column_fields]
            })
        
        # Add examples page at the end for bcsvw
        sidebar.append({
            'type': 'doc',
            'id': f'{schema_name}/examples',
            'label': 'Examples',
        })
    elif field_groups:
        # Group properties by field groups
        for group in field_groups:
            group_fields = [f for f in fields if f.get('group') == group['id']]
            if group_fields:
                sidebar.append({
                    'type': 'category',
                    'label': group['name'],
                    'collapsed': True,
                    'items': [f"{schema_name}/{field['name']}" for field in group_fields]
                })
        
        # Add examples page at the end for schemas with field groups
        if schema_name in ['collection', 'dataset']:
            sidebar.append({
                'type': 'doc',
                'id': f'{schema_name}/examples',
                'label': 'Examples',
            })
    else:
        # All properties in one category
        sidebar.append({
            'type': 'category',
            'label': 'Properties',
            'collapsed': True,
            'items': [f"{schema_name}/{field['name']}" for field in fields]
        })
        
        # Add examples page at the end if not already added
        if schema_name in ['collection', 'dataset']:
            sidebar.append({
                'type': 'doc',
                'id': f'{schema_name}/examples',
                'label': 'Examples',
            })
    
    return sidebar

def main():
    """Main execution function"""
    dry_run = '--check' in sys.argv
    
    # Base directories
    repo_root = Path(__file__).parent.parent
    docs_dir = repo_root / 'docs' / 'docs'
    
    if not dry_run:
        docs_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Generating Docusaurus documentation...")
    print(f"   Mode: {'DRY RUN' if dry_run else 'WRITE'}")
    print()
    
    sidebar_configs = {}
    
    # Process each schema
    for schema_name, schema_info in SCHEMAS.items():
        print(f"📁 Processing {schema_name}...")
        
        try:
            # Load schema data
            data = load_schema_data(schema_name)
            if data is None:
                print(f"   ⊘ Skipping (schema files not found)")
                continue
            
            # Create schema directory
            schema_docs_dir = docs_dir / schema_name
            if not dry_run:
                schema_docs_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate index page
            index_content = generate_index_page(schema_name, data)
            index_path = schema_docs_dir / 'index.md'
            if not dry_run:
                index_path.write_text(index_content)
            print(f"   ✓ Generated index page")
            
            # Generate property pages
            fields_count = 0
            for field in data['fields']:
                # Skip JSON-LD keywords (properties starting with @)
                if field['name'].startswith('@'):
                    continue
                    
                property_content = generate_property_page(field, data['metadata'], schema_name)
                property_path = schema_docs_dir / f"{field['name']}.md"
                if not dry_run:
                    property_path.write_text(property_content)
                fields_count += 1
                
                # Generate pages for nested object properties
                if 'object_properties' in field:
                    parent_name = field['name']
                    parent_dir = schema_docs_dir / parent_name
                    if not dry_run:
                        parent_dir.mkdir(parents=True, exist_ok=True)
                    
                    for obj_prop in field['object_properties']:
                        nested_field = {
                            'name': obj_prop['name'],
                            'type': obj_prop['type'],
                            'description': obj_prop.get('description', ''),
                            'status': 'required' if obj_prop.get('required', False) else 'optional',
                            'parent_property': parent_name,
                        }
                        if 'constraints' in obj_prop:
                            nested_field['constraints'] = obj_prop['constraints']
                        
                        nested_content = generate_property_page(nested_field, data['metadata'], schema_name)
                        nested_path = parent_dir / f"{obj_prop['name']}.md"
                        if not dry_run:
                            nested_path.write_text(nested_content)
                        fields_count += 1
            
            print(f"   ✓ Generated {fields_count} property pages")
            
            # Generate sidebar config
            sidebar_configs[f"{schema_name}Sidebar"] = generate_sidebar_config(schema_name, data)
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
            import traceback
            traceback.print_exc()
    
    # Write sidebar configuration
    if not dry_run:
        sidebars_path = repo_root / 'docs' / 'sidebars.js'
        sidebar_js = f"""/**
 * Auto-generated sidebars configuration
 * Generated on: {datetime.now().isoformat()}
 * 
 * DO NOT EDIT THIS FILE MANUALLY
 * Run: uv run scripts/generate_docs.py
 */

// @ts-check

/** @type {{import('@docusaurus/plugin-content-docs').SidebarsConfig}} */
const sidebars = {json.dumps(sidebar_configs, indent=2)};

export default sidebars;
"""
        sidebars_path.write_text(sidebar_js)
        print(f"\n✓ Generated sidebars.js")
    
    print(f"\n✅ Documentation generation complete!")
    print(f"   Run 'cd docs && npm install && npm start' to preview")

if __name__ == '__main__':
    main()
