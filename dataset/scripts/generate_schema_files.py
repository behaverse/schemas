#!/usr/bin/env python3
"""
Generate JSON Schema and JSON-LD Context from field-definitions.yaml

This script reads the field definitions YAML file and generates:
1. schema.json (JSON Schema for validation)
2. context.jsonld (JSON-LD Context for semantic web)

Usage:
    python scripts/generate_schema_files.py
    python scripts/generate_schema_files.py --check  # Dry run, show what would change
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
import sys

def load_field_definitions() -> Dict[str, Any]:
    """Load the field definitions YAML file."""
    schema_dir = Path(__file__).parent.parent
    definitions_path = schema_dir / 'field-definitions.yaml'
    
    with open(definitions_path, 'r') as f:
        return yaml.safe_load(f)

def build_member_schema(op: Dict[str, Any]) -> Dict[str, Any]:
    """JSON Schema for a single object sub-property.

    Handles nested arrays so that an `enum` constraint lands on `items` (the
    allowed element values), never on the array itself.
    """
    constraints = op.get('constraints', {})
    if op['type'] == 'array':
        schema: Dict[str, Any] = {'type': 'array'}
        if 'description' in op:
            schema['description'] = op['description']
        items: Dict[str, Any] = {'type': op.get('item_type', 'string')}
        if 'enum' in constraints:
            items['enum'] = constraints['enum']
        schema['items'] = items
        if 'min_items' in constraints:
            schema['minItems'] = constraints['min_items']
        if 'max_items' in constraints:
            schema['maxItems'] = constraints['max_items']
        return schema

    schema = {'type': op['type']}
    if 'description' in op:
        schema['description'] = op['description']
    for key in ('format', 'pattern', 'minimum', 'enum'):
        if key in constraints:
            schema[key] = constraints[key]
    return schema


def generate_json_schema(definitions: Dict[str, Any]) -> Dict[str, Any]:
    """Generate JSON Schema from field definitions."""
    metadata = definitions['schema_metadata']
    fields = definitions['fields']
    
    # Required fields
    required_fields = [f['name'] for f in fields if f.get('requirement') == 'required']

    # Build properties
    properties = {}
    for field in fields:
        # `@type` is a JSON-LD node-type declaration, not a typed property:
        # emit it as a fixed `const`, not `type` (which would be invalid JSON Schema).
        if field['name'] == '@type':
            properties['@type'] = {
                'const': field['type'],
                'title': 'Type',
                'description': field['description'],
            }
            continue

        # `enum`-typed fields are string-valued; the enum values carry the constraint.
        json_type = 'string' if field['type'] == 'enum' else field['type']
        prop = {
            'type': json_type,
            'title': field['name'].replace('_', ' ').title(),
            'description': field['description']
        }
        
        # Add equivalentProperty from mappings
        if 'mappings' in field:
            equiv_props = []
            for mapping in field['mappings']:
                if 'url' in mapping:
                    equiv_props.append(mapping['url'])
                elif mapping['standard'] == 'behaverse':
                    equiv_props.append(f"{metadata['namespace']}#{mapping['property']}")
            if equiv_props:
                prop['equivalentProperty'] = equiv_props if len(equiv_props) > 1 else equiv_props[0]
        
        # Add constraints
        if 'constraints' in field:
            constraints = field['constraints']
            if 'pattern' in constraints:
                prop['pattern'] = constraints['pattern']
            if 'format' in constraints:
                prop['format'] = constraints['format']
            if 'minimum' in constraints:
                prop['minimum'] = constraints['minimum']
            if 'min_length' in constraints:
                prop['minLength'] = constraints['min_length']
            if 'min_items' in constraints:
                prop['minItems'] = constraints['min_items']
            if 'max_items' in constraints:
                prop['maxItems'] = constraints['max_items']
            # `enum` on an array field constrains the *elements*, so it belongs on
            # `items` (handled below), not on the array itself.
            if 'enum' in constraints and field['type'] != 'array':
                prop['enum'] = constraints['enum']

        # Handle arrays
        if field['type'] == 'array':
            item_type = field.get('item_type', 'string')
            if item_type == 'object' and 'object_properties' in field:
                # Complex object array
                obj_props = {}
                obj_required = []
                for obj_prop in field['object_properties']:
                    obj_props[obj_prop['name']] = build_member_schema(obj_prop)
                    if obj_prop.get('required'):
                        obj_required.append(obj_prop['name'])

                prop['items'] = {
                    'type': 'object',
                    'properties': obj_props
                }
                if obj_required:
                    prop['items']['required'] = obj_required
            else:
                items = {'type': item_type}
                if 'enum' in field.get('constraints', {}):
                    items['enum'] = field['constraints']['enum']
                prop['items'] = items

        # Handle objects
        if field['type'] == 'object' and 'object_properties' in field:
            obj_props = {}
            for obj_prop in field['object_properties']:
                obj_props[obj_prop['name']] = build_member_schema(obj_prop)
            prop['properties'] = obj_props
        
        properties[field['name']] = prop
    
    # Build schema
    schema = {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        '$id': f"{metadata['namespace']}/v{metadata['version']}/schema.json",
        'title': metadata['name'],
        'description': metadata['description'],
        'version': metadata['version'],
        'type': 'object',
        'required': required_fields,
        'properties': properties
    }
    
    return schema

def generate_jsonld_context(definitions: Dict[str, Any]) -> Dict[str, Any]:
    """Generate JSON-LD Context from field definitions."""
    metadata = definitions['schema_metadata']
    fields = definitions['fields']
    
    context = {
        '@vocab': f"{metadata['namespace']}#",
        'behaverse': f"{metadata['namespace']}#",
        'schema': 'https://schema.org/',
        'dc': 'http://purl.org/dc/terms/',
        'bids': 'https://bids-specification.readthedocs.io/en/stable/',
        'ddi': 'https://ddialliance.org/Specification/DDI-Lifecycle/3.3/',
        'xsd': 'http://www.w3.org/2001/XMLSchema#'
    }

    # Add field mappings
    for field in fields:
        # `@type` is the JSON-LD keyword for node type; never redefine it as a term.
        if field['name'] == '@type':
            continue
        field_context = {}
        
        # Find primary mapping (prefer schema.org, then datacite, then custom)
        primary_mapping = None
        if 'mappings' in field:
            for mapping in field['mappings']:
                if mapping['standard'] == 'schema.org' and 'url' in mapping:
                    primary_mapping = mapping['url']
                    break
            
            if not primary_mapping:
                for mapping in field['mappings']:
                    if 'url' in mapping:
                        primary_mapping = mapping['url']
                        break
                    elif mapping['standard'] == 'behaverse':
                        primary_mapping = f"behaverse:{mapping['property']}"
                        break
        
        if primary_mapping:
            field_context['@id'] = primary_mapping
        else:
            field_context['@id'] = f"behaverse:{field['name']}"
        
        # Add type mappings
        if field['type'] in ('string', 'enum'):
            if field.get('constraints', {}).get('format') == 'date':
                field_context['@type'] = 'xsd:date'
            elif field.get('constraints', {}).get('format') == 'uri':
                field_context['@type'] = '@id'
            else:
                field_context['@type'] = 'xsd:string'
        elif field['type'] == 'integer':
            field_context['@type'] = 'xsd:integer'
        elif field['type'] == 'number':
            field_context['@type'] = 'xsd:decimal'
        elif field['type'] == 'boolean':
            field_context['@type'] = 'xsd:boolean'
        elif field['type'] == 'array':
            if field.get('item_type') == 'number':
                field_context['@container'] = '@list'
            else:
                field_context['@container'] = '@set'
            # URL-valued array items are node references, not string literals.
            if field.get('constraints', {}).get('format') == 'uri':
                field_context['@type'] = '@id'
        elif field['type'] == 'object':
            field_context['@type'] = '@id'
        
        context[field['name']] = field_context

        # Emit flat context terms for structured sub-properties that carry their own
        # mapping (e.g. creator/curator -> email, orcid, affiliation), so they don't
        # leak to @vocab. Skipped if already defined by a top-level field.
        for obj_prop in field.get('object_properties', []):
            if 'mappings' not in obj_prop:
                continue
            url = next((m['url'] for m in obj_prop['mappings'] if 'url' in m), None)
            if url and obj_prop['name'] not in context:
                context[obj_prop['name']] = {'@id': url}

    return {'@context': context}

def save_json_file(data: Dict[str, Any], path: Path, check_mode: bool = False) -> bool:
    """Save JSON file with pretty formatting."""
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    if check_mode:
        if path.exists():
            with open(path, 'r') as f:
                existing = f.read()
            if existing.strip() != json_str.strip():
                print(f"Would update: {path}")
                return True
        else:
            print(f"Would create: {path}")
            return True
        return False
    else:
        with open(path, 'w') as f:
            f.write(json_str)
        print(f"✓ Generated: {path}")
        return True

def main():
    """Main entry point."""
    check_mode = '--check' in sys.argv
    
    if check_mode:
        print("Running in check mode (dry run)...\n")
    
    # Load definitions
    try:
        definitions = load_field_definitions()
    except Exception as e:
        print(f"✗ Failed to load field definitions: {e}")
        sys.exit(1)
    
    # Generate schemas
    schema_dir = Path(__file__).parent.parent
    
    try:
        # Generate JSON Schema
        json_schema = generate_json_schema(definitions)
        schema_path = schema_dir / 'schema.json'
        changed1 = save_json_file(json_schema, schema_path, check_mode)
        
        # Generate JSON-LD Context
        jsonld_context = generate_jsonld_context(definitions)
        context_path = schema_dir / 'context.jsonld'
        changed2 = save_json_file(jsonld_context, context_path, check_mode)
        
        if check_mode:
            if changed1 or changed2:
                print("\n⚠ Schema files would be modified. Run without --check to apply changes.")
                sys.exit(1)
            else:
                print("\n✓ Schema files are up to date.")
        else:
            print("\n✓ Schema generation complete!")
            
    except Exception as e:
        print(f"\n✗ Error generating schemas: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
