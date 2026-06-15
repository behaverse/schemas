#!/usr/bin/env python3
"""
Generate Docusaurus MDX documentation from schema definitions

This script reads the LinkML source of truth (schema.linkml.yaml) and generated
artifacts (field-definitions.json, schema.json) from each schema directory and
generates comprehensive MDX documentation pages for Docusaurus.

Source of truth per schema:
- catalog, dataset: schema.linkml.yaml (the tree_root class attributes; the
  `field_groups` schema-level annotation drives Overview grouping + field order)
- trial, event: field-definitions.json (generated render artifact)
- studyflow: schema.linkml.yaml
- bcsv: schema.json
The deprecated field-definitions.yaml files are NOT read by any code path.

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
import re

# Schema directories to process.
# `source` selects the loader branch in load_schema_data():
#   'linkml'   -> read schema.linkml.yaml tree_root class + field_groups annotation
#   'json'     -> read schema.json (bcsv)
#   'studyflow'-> read schema.linkml.yaml via linkml_to_json (classes/enums listing)
# `multi_table` / `vocabulary` -> read the generated field-definitions.json artifact.
SCHEMAS = {
    'bcsv': {
        'source': 'json',  # Uses schema.json directly
        'name': 'bcsv (Better CSV)',
        'icon': 'schema_B.png',
    },
    'catalog': {
        'source': 'linkml',  # tree_root class attributes + field_groups annotation
        'name': 'Catalog Schema',
        'icon': 'schema_C.png',
    },
    'dataset': {
        'source': 'linkml',  # tree_root class attributes + field_groups annotation
        'name': 'Dataset Schema',
        'icon': 'schema_D.png',
    },
    'studyflow': {
        'source': 'studyflow',  # LinkML classes/enums listing
        'name': 'Studyflow Schema',
        'icon': 'schema_S.png',
    },
    'trial': {
        'source': 'json',
        'multi_table': True,  # field-definitions.json has `tables`, not flat `fields`
        'name': 'Trial Schema',
        'icon': '',
    },
    'event': {
        'source': 'json',
        'vocabulary': True,  # envelope `fields` + a bdm: `vocabularies` block
        'name': 'Event Schema',
        'icon': '',
    },
    'vocabulary': {
        'source': 'terms',  # SKOS-style terms.yaml: schemes + concepts
        'skos_vocabulary': True,  # grouped Overview (one section per public scheme)
        'name': 'Behaverse Vocabulary',
        'icon': '',
    },
}

# Map a slot's `class_uri` / `slot_uri` CURIE (e.g. `sdo:Dataset`) to the `schema:`
# form the deprecated YAML used for the synthesized `@type` row.
_TYPE_PREFIX_TO_SCHEMA = {'sdo': 'schema'}

# How the deprecated field-definitions.yaml rendered a scalar LinkML range as a docs
# `type` (plus any implied JSON-Schema-style `constraints`).
_SCALAR_RANGE = {
    'string': ('string', None),
    'integer': ('integer', None),
    'float': ('number', None),
    'double': ('number', None),
    'decimal': ('number', None),
    'boolean': ('boolean', None),
    'date': ('string', ('format', 'date')),
    'datetime': ('string', ('format', 'date-time')),
    'time': ('string', ('format', 'time')),
    'uri': ('string', ('format', 'uri')),
    'uriorcurie': ('string', ('format', 'uri')),
}


def _curie_to_url(prefixes: Dict[str, str], curie: str) -> Optional[str]:
    """Expand a `prefix:local` CURIE to a full URL using the LinkML `prefixes` map."""
    if not curie or ':' not in curie:
        return None
    prefix, local = curie.split(':', 1)
    base = prefixes.get(prefix)
    return f"{base}{local}" if base else None


def _curie_to_schema_form(curie: str) -> str:
    """Render a class/slot CURIE the way the YAML did (e.g. `sdo:Dataset` -> `schema:Dataset`)."""
    if ':' not in curie:
        return curie
    prefix, local = curie.split(':', 1)
    return f"{_TYPE_PREFIX_TO_SCHEMA.get(prefix, prefix)}:{local}"


def _slot_requirement(slot: Dict[str, Any]) -> str:
    if slot.get('required'):
        return 'required'
    if slot.get('recommended'):
        return 'recommended'
    return 'optional'


def _slot_examples(slot: Dict[str, Any]) -> List[Any]:
    """LinkML examples are `[{value: x}, ...]`; the YAML path used a flat value list."""
    out = []
    for ex in slot.get('examples', []) or []:
        if isinstance(ex, dict) and 'value' in ex:
            out.append(ex['value'])
        else:
            out.append(ex)
    return out


def _slot_mappings(prefixes: Dict[str, str], slot: Dict[str, Any]) -> List[Dict[str, str]]:
    """Build the YAML-shaped `[{standard, property, url}]` list from slot_uri + exact_mappings."""
    mappings = []
    seen = set()
    for curie in ([slot['slot_uri']] if slot.get('slot_uri') else []) + list(slot.get('exact_mappings', []) or []):
        if curie in seen:
            continue
        seen.add(curie)
        prefix = curie.split(':', 1)[0] if ':' in curie else 'external'
        prop = curie.split(':', 1)[1] if ':' in curie else curie
        m = {'standard': prefix, 'property': prop}
        url = _curie_to_url(prefixes, curie)
        if url:
            m['url'] = url
        mappings.append(m)
    return mappings


def _slot_constraints(slot: Dict[str, Any], scalar_constraint=None,
                      enum_values=None) -> Dict[str, Any]:
    """Collect JSON-Schema-style constraints the YAML path surfaced for a slot."""
    c = {}
    if scalar_constraint:
        c[scalar_constraint[0]] = scalar_constraint[1]
    if slot.get('pattern'):
        c['pattern'] = slot['pattern']
    if 'minimum_value' in slot:
        c['minimum'] = slot['minimum_value']
    if 'maximum_value' in slot:
        c['maximum'] = slot['maximum_value']
    if 'minimum_cardinality' in slot:
        c['min_items'] = slot['minimum_cardinality']
    if 'maximum_cardinality' in slot:
        c['max_items'] = slot['maximum_cardinality']
    if enum_values:
        c['enum'] = enum_values
    return c


def _linkml_field_from_slot(name: str, slot: Dict[str, Any], group_id: str,
                            classes: Dict[str, Any], enums: Dict[str, Any],
                            prefixes: Dict[str, str],
                            include_object_props: bool = True) -> Dict[str, Any]:
    """Produce a docs field-dict (same shape the deprecated YAML emitted) from a LinkML slot."""
    slot = slot or {}
    rng = slot.get('range', 'string')
    multivalued = bool(slot.get('multivalued'))

    field: Dict[str, Any] = {
        'name': name,
        'description': slot.get('description', ''),
        'requirement': _slot_requirement(slot),
    }
    if group_id is not None:
        field['group'] = group_id

    scalar_constraint = None
    enum_values = None

    if rng in classes:  # range is an object (a referenced class)
        if multivalued:
            field['type'] = 'array'
            field['item_type'] = 'object'
        else:
            field['type'] = 'object'
        if include_object_props:
            obj_props = []
            for attr_name, attr_slot in (classes[rng].get('attributes') or {}).items():
                obj_props.append(_linkml_object_property(attr_name, attr_slot or {},
                                                         enums, prefixes))
            if obj_props:
                field['object_properties'] = obj_props
    elif rng in enums:  # range is an enumeration
        enum_values = list((enums[rng].get('permissible_values') or {}).keys())
        if multivalued:
            field['type'] = 'array'
            field['item_type'] = 'string'
        else:
            field['type'] = 'enum'
    else:  # scalar range
        scalar_type, scalar_constraint = _SCALAR_RANGE.get(rng, ('string', None))
        if multivalued:
            field['type'] = 'array'
            field['item_type'] = scalar_type
        else:
            field['type'] = scalar_type

    constraints = _slot_constraints(slot, scalar_constraint, enum_values)
    if constraints:
        field['constraints'] = constraints

    mappings = _slot_mappings(prefixes, slot)
    if mappings:
        field['mappings'] = mappings

    examples = _slot_examples(slot)
    if examples:
        field['examples'] = examples

    return field


def _linkml_object_property(name: str, slot: Dict[str, Any], enums: Dict[str, Any],
                            prefixes: Dict[str, str]) -> Dict[str, Any]:
    """A nested object-property dict (creator/curator/... sub-fields), YAML-shaped."""
    rng = slot.get('range', 'string')
    base_type = 'enum' if rng in enums else _SCALAR_RANGE.get(rng, ('string', None))[0]
    # Multivalued sub-fields rendered as `array` in the deprecated YAML path.
    ptype = 'array' if slot.get('multivalued') else base_type
    prop: Dict[str, Any] = {
        'name': name,
        'type': ptype,
        'required': bool(slot.get('required')),
        'description': slot.get('description', ''),
    }
    constraints = {}
    scalar_constraint = _SCALAR_RANGE.get(rng, ('string', None))[1]
    if scalar_constraint:
        constraints[scalar_constraint[0]] = scalar_constraint[1]
    if slot.get('pattern'):
        constraints['pattern'] = slot['pattern']
    if rng in enums:
        vals = list((enums[rng].get('permissible_values') or {}).keys())
        if vals:
            constraints['enum'] = vals
    if constraints:
        prop['constraints'] = constraints
    mappings = _slot_mappings(prefixes, slot)
    if mappings:
        prop['mappings'] = mappings
    return prop


def load_linkml_tree_root(schema_name: str, schema_dir: Path) -> Dict[str, Any]:
    """Load catalog/dataset Overview data from schema.linkml.yaml.

    Builds the same field-dict shape the deprecated field-definitions.yaml produced:
    fields from the tree_root class attributes (ordered by the `field_groups`
    annotation), a synthesized `@type` row, the field_groups list, and metadata.
    """
    linkml = yaml.safe_load((schema_dir / 'schema.linkml.yaml').read_text())
    classes = linkml.get('classes', {}) or {}
    enums = linkml.get('enums', {}) or {}
    prefixes = linkml.get('prefixes', {}) or {}

    # Locate the tree_root class (the single data class: Catalog / Dataset).
    root_name, root_cls = None, None
    for cname, cmeta in classes.items():
        if (cmeta or {}).get('tree_root'):
            root_name, root_cls = cname, (cmeta or {})
            break
    if root_cls is None:
        raise ValueError(f"{schema_name}: no tree_root class in schema.linkml.yaml")

    attributes = root_cls.get('attributes', {}) or {}

    # field_groups annotation: list of {id, name, description, fields:[...]}.
    fg_annotation = (((linkml.get('annotations') or {}).get('field_groups') or {})
                     .get('value') or [])
    # Map each field name -> its group id, and remember the annotation's field order.
    field_to_group: Dict[str, str] = {}
    ordered_names: List[str] = []
    for grp in fg_annotation:
        for fname in grp.get('fields', []) or []:
            field_to_group[fname] = grp['id']
            ordered_names.append(fname)

    # Group list for the Overview/sidebar (id, name, description only).
    field_groups = [{'id': g['id'], 'name': g.get('name', g['id']),
                     'description': g.get('description', '')} for g in fg_annotation]

    class_uri = root_cls.get('class_uri', '')
    type_value = _curie_to_schema_form(class_uri) if class_uri else schema_name

    fields: List[Dict[str, Any]] = []
    for fname in ordered_names:
        if fname == '@type':
            fields.append({
                'name': '@type',
                'group': field_to_group.get('@type', 'core_metadata'),
                'type': type_value,
                'requirement': 'optional',
                'description': ('JSON-LD node type (rdf:type) for schema.org / '
                                'Google Dataset Search discoverability.'),
            })
            continue
        if fname not in attributes:
            continue  # listed in annotation but not (yet) a slot; skip defensively
        fields.append(_linkml_field_from_slot(
            fname, attributes[fname], field_to_group.get(fname),
            classes, enums, prefixes))

    # Append any attributes not covered by the annotation, in declaration order.
    for fname, slot in attributes.items():
        if fname not in field_to_group:
            fields.append(_linkml_field_from_slot(
                fname, slot, None, classes, enums, prefixes))

    return {
        'metadata': {
            'name': linkml.get('title', schema_name),
            'version': str(linkml.get('version', '')).lstrip('v'),
            'namespace': linkml.get('id', f'https://behaverse.org/schemas/{schema_name}'),
            'description': linkml.get('description', ''),
        },
        'fields': fields,
        'field_groups': field_groups,
    }

def load_vocabulary_terms(schema_dir: Path) -> Dict[str, Any]:
    """Load the SKOS-style vocabulary from terms.yaml.

    Returns docs metadata + the public schemes (with their concepts grouped under each),
    EXCLUDING any scheme or concept with `status: internal` (kept for reference only).
    """
    terms = yaml.safe_load((schema_dir / 'terms.yaml').read_text())
    meta = terms.get('vocabulary_metadata', {}) or {}

    # Public schemes only (drop status: internal).
    schemes = []
    for scheme in terms.get('schemes', []) or []:
        if (scheme or {}).get('status') == 'internal':
            continue
        schemes.append({
            'id': scheme['id'],
            'label': scheme.get('label', scheme['id']),
            'description': scheme.get('description', ''),
            'concepts': [],
        })
    by_id = {s['id']: s for s in schemes}

    # Group public concepts under their (public) scheme.
    for concept in terms.get('concepts', []) or []:
        concept = concept or {}
        if concept.get('status') == 'internal':
            continue
        scheme = by_id.get(concept.get('scheme'))
        if scheme is None:
            continue  # scheme is internal/missing -> concept excluded with it
        scheme['concepts'].append({
            'id': concept['id'],
            'label': concept.get('label', concept['id']),
            'definition': concept.get('definition', ''),
            'data_type': concept.get('data_type', ''),
        })

    return {
        'metadata': {
            'name': meta.get('name', 'Behaverse Vocabulary'),
            'version': str(meta.get('version', '')).lstrip('v'),
            'namespace': meta.get('namespace',
                                  'https://behaverse.org/schemas/vocabulary'),
            'description': meta.get('description', ''),
        },
        'schemes': schemes,
    }


def _json_metadata(data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
    """Map a field-definitions.json top level to the docs `metadata` dict."""
    return {
        'name': data.get('schema', schema_name),
        'version': str(data.get('version', '')).lstrip('v'),
        'namespace': data.get('namespace', f'https://behaverse.org/schemas/{schema_name}'),
        'description': data.get('description', ''),
    }


def load_schema_data(schema_name: str) -> Dict[str, Any]:
    """Load schema data from the LinkML source / generated artifacts.

    NOTE: no branch reads the deprecated field-definitions.yaml.
    """
    schema_dir = Path(__file__).parent.parent / schema_name

    schema_info = SCHEMAS[schema_name]

    # trial: generated field-definitions.json with `tables` (multi-table layout).
    if schema_info.get('multi_table'):
        data = json.loads((schema_dir / 'field-definitions.json').read_text())
        return {'metadata': _json_metadata(data, schema_name), 'tables': data['tables']}

    # event: generated field-definitions.json with envelope `fields` + `vocabularies`.
    if schema_info.get('vocabulary'):
        data = json.loads((schema_dir / 'field-definitions.json').read_text())
        return {'metadata': _json_metadata(data, schema_name),
                'fields': data['fields'],
                'vocabularies': data.get('vocabularies', {})}

    # vocabulary: SKOS-style terms.yaml (schemes + concepts), excludes internal terms.
    if schema_info.get('skos_vocabulary'):
        return load_vocabulary_terms(schema_dir)

    # catalog, dataset: LinkML source of truth (tree_root class + field_groups).
    if schema_info.get('source') == 'linkml':
        return load_linkml_tree_root(schema_name, schema_dir)

    if schema_info.get('source') == 'studyflow':
        # Load from LinkML format (classes/enums listing)
        linkml_path = schema_dir / 'schema.linkml.yaml'
        if not linkml_path.exists():
            # Skip studyflow if schema.linkml.yaml doesn't exist
            return None
        with open(linkml_path, 'r') as f:
            linkml = yaml.safe_load(f)
        return {
            'metadata': {
                'name': linkml.get('title', 'Studyflow Schema'),
                'version': linkml.get('version', '').lstrip('v'),
                'namespace': linkml.get('id', 'https://behaverse.org/schemas/studyflow'),
                'description': linkml.get('description', 'Schema for defining the formal structure of studyflow diagrams'),
            },
            'fields': linkml_to_json(linkml),
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

def _derive_type(prop_def: Dict[str, Any]) -> str:
    """Human-readable type for the docs (handles enum / const / oneOf / format)."""
    if 'enum' in prop_def:
        return 'enum'
    if 'const' in prop_def:
        c = prop_def['const']
        return c if isinstance(c, str) else str(c)
    if 'oneOf' in prop_def:
        types = []
        for o in prop_def['oneOf']:
            if 'enum' in o:
                t = 'enum'
            elif 'type' in o:
                t = o['type']
            elif '$ref' in o:
                t = 'object'
            else:
                continue
            if t not in types:
                types.append(t)
        return ' / '.join(types) if types else 'string'
    t = prop_def.get('type', 'string')
    if 'format' in prop_def:
        t = f"{t} ({prop_def['format']})"
    return t


def convert_json_schema_to_fields(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert JSON Schema properties to field definitions format"""
    fields = []
    properties = schema.get('properties', {})
    required_fields = schema.get('required', [])
    
    # Process top-level properties
    for prop_name, prop_def in properties.items():
        field = {
            'name': prop_name,
            'type': _derive_type(prop_def),
            'description': prop_def.get('description', ''),
            'requirement': 'required' if prop_name in required_fields else 'optional',
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
    
    # For bcsv, also extract column properties from definitions
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
                prop_type = _derive_type(col_prop_def)
                
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

def linkml_to_json(linkml: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert LinkML format to field definitions format"""
    fields = []
    
    # Add classes from LinkML
    for cls_name, cls_meta in linkml.get('classes', {}).items():
        if cls_meta is None:
            cls_meta = {}
        
        # Build description from class metadata
        description = cls_meta.get('description', f'{cls_name} element type')
        if cls_meta.get('abstract'):
            description = f'[Abstract] {description}'
        
        field = {
            'name': cls_name,
            'type': 'class',
            'description': description,
            'requirement': 'optional',
        }
        
        # Add attributes as nested properties
        if cls_meta.get('attributes'):
            obj_props = []
            for attr_name, attr_meta in cls_meta['attributes'].items():
                if attr_meta is None:
                    attr_meta = {}
                obj_props.append({
                    'name': attr_name,
                    'type': attr_meta.get('range', 'string'),
                    'description': attr_meta.get('description', ''),
                    'required': attr_meta.get('required', False),
                })
            if obj_props:
                field['object_properties'] = obj_props
        
        fields.append(field)
    
    # Add enums from LinkML
    for enum_name, enum_meta in linkml.get('enums', {}).items():
        if enum_meta is None:
            enum_meta = {}
        
        values = list(enum_meta.get('permissible_values', {}).keys())
        field = {
            'name': enum_name,
            'type': 'enum',
            'description': enum_meta.get('description', f'{enum_name} enumeration'),
            'requirement': 'optional',
            'constraints': {'enum': values} if values else {},
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
    
    # For bcsv, separate table and column properties
    if schema_name == 'bcsv':
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
    if schema_name in ['bcsv', 'catalog', 'dataset']:
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
    
    # Add about page for bcsv, catalog, and dataset
    if schema_name in ['bcsv', 'catalog', 'dataset']:
        sidebar.append({
            'type': 'doc',
            'id': f'{schema_name}/about',
            'label': 'About',
        })
    
    # Filter out JSON-LD keywords
    fields = [f for f in fields if not f['name'].startswith('@')]
    
    # For bcsv, separate table-level and column-level properties
    if schema_name == 'bcsv':
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
        
        # Add examples page at the end for bcsv
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
        if schema_name in ['catalog', 'dataset']:
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
        if schema_name in ['catalog', 'dataset']:
            sidebar.append({
                'type': 'doc',
                'id': f'{schema_name}/examples',
                'label': 'Examples',
            })
    
    return sidebar


def _mdx_cell(text: str) -> str:
    """Escape a string for safe use inside an MDX markdown table cell."""
    s = (text or '').replace('|', '\\|').replace('\n', ' ')
    s = s.replace('{', '&#123;').replace('}', '&#125;').replace('<', '&lt;')
    return s.strip()


def _mdx_text(text: str) -> str:
    """Escape JSX-sensitive characters for MDX body prose (newlines preserved)."""
    return (text or '').replace('<', '&lt;').replace('{', '&#123;').replace('}', '&#125;')


def _schema_page_header(schema_name: str, metadata: Dict[str, Any]) -> str:
    version_str = f"v{metadata['version']}" if metadata.get('version') else "(not versioned)"
    return f"""---
id: index
title: {schema_name}
sidebar_label: Overview
slug: /{schema_name}
---

<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->

# {schema_name}

**Version**: {version_str}
**Namespace**: `{metadata['namespace']}`

{metadata['description']}
"""


def _slug(name: str) -> str:
    """Path/URL-safe slug for a table or section name (CamelCase -> kebab-case)."""
    s = re.sub(r'(?<!^)(?=[A-Z])', '-', str(name))
    s = re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()
    return s or 'item'


def _page_name(fname: str) -> str:
    """Docusaurus-safe file basename: a field called `index`/`readme` would otherwise
    become a folder-index doc and collapse its id, breaking the sidebar reference."""
    return f"{fname}-field" if fname.lower() in ('index', 'readme') else fname


def _member_frontmatter(page_id: str, display_name: str) -> str:
    """Frontmatter for a per-member page; `id` drives routing, `display_name` is shown."""
    reserved = ['null', 'true', 'false', 'yes', 'no', 'on', 'off']
    def q(v: str) -> str:
        return f'"{v}"' if (v.startswith('@') or v.lower() in reserved) else v
    return f"---\nid: {q(page_id)}\ntitle: {q(display_name)}\nsidebar_label: {q(display_name)}\n---\n"


def generate_member_page(field: Dict[str, Any], schema_name: str, section_note: str) -> str:
    """Per-field detail page for a trial table field or an event envelope field.

    Mirrors the property pages (badge + Details table) while carrying the member-level
    attributes trial/event use (range, categories, allowed values, notes).
    """
    name = field['name']
    description = field.get('description', 'No description available.')
    field_type = field.get('type', 'string')
    requirement = field.get('requirement', 'optional')

    mdx = _member_frontmatter(_page_name(name), name)
    mdx += "\n<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->\n\n"
    mdx += f"# {name}\n\n{generate_status_badge(requirement)}\n\n{_mdx_text(description)}\n\n"
    mdx += f":::info\n{section_note}\n:::\n\n"
    mdx += "## Details\n\n<div className=\"property-details\">\n\n"
    mdx += "| Property | Value |\n|:---------|:------|\n"
    mdx += f"| **Type** | `{field_type}` |\n"
    mdx += f"| **Requirement** | {requirement.lower()} |\n"
    if field.get('range'):
        mdx += f"| **Range** | {_mdx_cell(str(field['range']))} |\n"
    if field.get('categories'):
        cats = ', '.join(f'`{c}`' for c in field['categories'])
        mdx += f"| **Categories** | {cats} |\n"
    mdx += "\n</div>\n"

    constraints = field.get('constraints', {}) or {}
    if constraints.get('enum'):
        mdx += "\n## Allowed values\n\n" + ', '.join(f'`{v}`' for v in constraints['enum']) + "\n"

    notes = field.get('notes')
    if notes:
        mdx += "\n## Notes\n\n"
        for n in (notes if isinstance(notes, list) else [notes]):
            mdx += f"- {_mdx_cell(str(n))}\n"
    return mdx


def _strip_bdm(name: str) -> str:
    """Display form of a vocabulary term: drop the `bdm:` CURIE prefix (stated once per page)."""
    s = str(name)
    return s.split(':', 1)[1] if s.startswith('bdm:') else s


def _doc_frontmatter(doc_id: str, title: str) -> str:
    """Frontmatter for a standalone generated page (a table page / a vocabulary page)."""
    return (f"---\nid: {doc_id}\ntitle: {title}\nsidebar_label: {title}\n---\n\n"
            f"<!-- THIS FILE IS AUTO-GENERATED. DO NOT EDIT MANUALLY. -->\n")


def generate_trial_pages(schema_name: str, data: Dict[str, Any],
                         schema_docs_dir: Path, dry_run: bool) -> List[Dict[str, Any]]:
    """Trial (multi-table): an Overview hub, one page per table, one page per field.

    Each table is a sidebar category whose label links to that table's page (Docusaurus
    categories can't link to a #anchor), so clicking the header opens the table. Within a
    table, fields are grouped by their `categories` value (Key, Context, Task, …) — a
    section per category on the table page and a nested sub-category in the sidebar —
    mirroring how the Behaverse data-model site organises each table.
    """
    metadata = data['metadata']
    tables = data['tables']
    n_fields = sum(len(t.get('fields', [])) for t in tables)

    # --- Overview: a hub linking to each table page ---
    idx = [_schema_page_header(schema_name, metadata)]
    idx.append(f"\nTrial-level data is organised as **{len(tables)} tidy tables** "
               f"({n_fields} fields total), joined by `_id` foreign keys. Open a table "
               f"to browse its fields.\n")
    idx.append("| Table | Fields | Description |")
    idx.append("|:------|------:|:------------|")
    for t in tables:
        idx.append(f"| [{t['name']}]({_slug(t['name'])}.md) | {len(t.get('fields', []))} "
                   f"| {_mdx_cell(t.get('description', ''))} |")
    if not dry_run:
        (schema_docs_dir / 'index.md').write_text("\n".join(idx))

    sidebar: List[Dict[str, Any]] = [
        {'type': 'doc', 'id': f'{schema_name}/index', 'label': 'Overview'},
        {'type': 'doc', 'id': f'{schema_name}/about', 'label': 'About'},
    ]

    for table in tables:
        tslug = _slug(table['name'])
        # Each field carries a single category; group the table by category, preserving
        # first-appearance order (the YAML orders fields by category).
        cat_order: List[str] = []
        for f in table['fields']:
            cat = (f.get('categories') or ['Other'])[0]
            if cat not in cat_order:
                cat_order.append(cat)

        # --- per-table page: heading, description, notes, one field table per category ---
        tp = [_doc_frontmatter(tslug, table['name']), f"\n# {table['name']}\n"]
        if table.get('description'):
            tp.append(f"\n{_mdx_text(table['description'])}\n")
        for note in table.get('notes') or []:
            tp.append(f"\n:::note\n{_mdx_text(str(note))}\n:::\n")

        cat_groups: List[Dict[str, Any]] = []  # one sidebar sub-category per category
        for cat in cat_order:
            cfields = [f for f in table['fields']
                       if (f.get('categories') or ['Other'])[0] == cat]
            tp.append(f"\n## {cat}\n")
            tp.append("| Field | Type | Requirement | Description |")
            tp.append("|:------|:-----|:------------|:------------|")
            cat_items: List[str] = []
            for field in cfields:
                fname = field['name']
                pname = _page_name(fname)
                tp.append(f"| [{fname}]({tslug}/{pname}.md) "
                          f"| {_mdx_cell(field.get('type', ''))} "
                          f"| {field.get('requirement', 'optional')} "
                          f"| {_mdx_cell(field.get('description', ''))} |")
                if not dry_run:
                    tdir = schema_docs_dir / tslug
                    tdir.mkdir(parents=True, exist_ok=True)
                    note = (f"Part of the **{cat}** category of the "
                            f"**[{table['name']}](../{tslug}.md)** table in the "
                            f"`{schema_name}` schema.")
                    (tdir / f"{pname}.md").write_text(
                        generate_member_page(field, schema_name, note))
                cat_items.append(f"{schema_name}/{tslug}/{pname}")
            cat_groups.append({'type': 'category', 'label': cat, 'collapsed': True,
                               'items': cat_items})

        if not dry_run:
            (schema_docs_dir / f"{tslug}.md").write_text("\n".join(tp) + "\n")
        sidebar.append({'type': 'category', 'label': table['name'], 'collapsed': True,
                        'link': {'type': 'doc', 'id': f'{schema_name}/{tslug}'},
                        'items': cat_groups})

    return sidebar


def generate_event_pages(schema_name: str, data: Dict[str, Any],
                         schema_docs_dir: Path, dry_run: bool) -> List[Dict[str, Any]]:
    """Event: foreground the Behaverse `bdm:` controlled vocabulary (what we define); the
    xAPI Statement envelope is the external container, shown secondarily + explained in About."""
    metadata = data['metadata']
    fields = data['fields']
    vocab = data.get('vocabularies', {})
    ex = _strip_bdm(vocab['verbs'][0]['name']) if vocab.get('verbs') else 'example'
    bdm_note = (f"All terms live in the `bdm:` namespace; the canonical id of "
                f"`{ex}` is `bdm:{ex}`.")

    idx = [_schema_page_header(schema_name, metadata)]
    idx.append("\nA Behaverse **event** is an [xAPI](http://adlnet.gov/projects/xapi/) "
               "*Statement* — an `actor` / `verb` / `object` envelope — carrying the "
               "Behaverse **`bdm:` controlled vocabulary**. The envelope is the standard "
               "container (defined by xAPI); the vocabulary below is **what Behaverse "
               "defines**. See [About](about.md) for the xAPI background.\n")

    sidebar: List[Dict[str, Any]] = [
        {'type': 'doc', 'id': f'{schema_name}/index', 'label': 'Overview'},
        {'type': 'doc', 'id': f'{schema_name}/about', 'label': 'About'},
    ]

    def write_page(slug: str, title: str, body: str) -> None:
        if not dry_run:
            (schema_docs_dir / f"{slug}.md").write_text(
                _doc_frontmatter(slug, title) + f"\n# {title}\n\n{body}\n")

    # --- Controlled vocabulary (the focus) ---
    idx.append("\n## Controlled vocabulary — defined by Behaverse\n")
    idx.append(bdm_note + "\n")
    idx.append(f"- **[Verbs](verbs.md)** — {len(vocab.get('verbs', []))} actions an actor can perform.")
    idx.append(f"- **[Object types](object-types.md)** — {len(vocab.get('object_types', []))} kinds of thing an event is about.")
    idx.append(f"- **[Actor types](actor-types.md)** — {len(vocab.get('actor_types', []))} kinds of actor.\n")

    vocab_items: List[Dict[str, Any]] = []
    if vocab.get('verbs'):
        rows = [bdm_note + "\n", "| Verb | Layer | Object types | Description |",
                "|:-----|:------|:-------------|:------------|"]
        for x in vocab['verbs']:
            ots = ', '.join(_strip_bdm(o) for o in x.get('object_types', []))
            rows.append(f"| **{_strip_bdm(x['name'])}** | {x.get('layer', '')} | {ots} "
                        f"| {_mdx_cell(x.get('description', ''))} |")
        write_page('verbs', 'Verbs', "\n".join(rows))
        vocab_items.append({'type': 'doc', 'id': f'{schema_name}/verbs', 'label': 'Verbs'})

    for key, slug, title in (('object_types', 'object-types', 'Object types'),
                             ('actor_types', 'actor-types', 'Actor types')):
        if vocab.get(key):
            rows = [bdm_note + "\n", f"| {title[:-1]} | Description |", "|:------|:------------|"]
            for x in vocab[key]:
                rows.append(f"| **{_strip_bdm(x['name'])}** | {_mdx_cell(x.get('description', ''))} |")
            write_page(slug, title, "\n".join(rows))
            vocab_items.append({'type': 'doc', 'id': f'{schema_name}/{slug}', 'label': title})

    if vocab_items:
        sidebar.append({'type': 'category', 'label': 'Controlled vocabulary',
                        'collapsed': False, 'items': vocab_items})

    # --- xAPI envelope (external container, shown secondarily) ---
    idx.append("\n## Event envelope (xAPI — external)\n")
    idx.append("These are the standard **xAPI Statement** fields; Behaverse uses them as-is. "
               "They are the *container*, not what this schema defines — see [About](about.md).\n")
    idx.append("| Field | Type | Requirement | Description |")
    idx.append("|:------|:-----|:------------|:------------|")
    env_items: List[str] = []
    for field in fields:
        fname = field['name']
        pname = _page_name(fname)
        idx.append(f"| [{fname}](envelope/{pname}.md) "
                   f"| {_mdx_cell(field.get('type', ''))} "
                   f"| {field.get('requirement', 'optional')} "
                   f"| {_mdx_cell(field.get('description', ''))} |")
        if not dry_run:
            edir = schema_docs_dir / 'envelope'
            edir.mkdir(parents=True, exist_ok=True)
            note = "Part of the **xAPI Statement envelope** (external standard) used by `event`."
            (edir / f"{pname}.md").write_text(generate_member_page(field, schema_name, note))
        env_items.append(f"{schema_name}/envelope/{pname}")
    sidebar.append({'type': 'category', 'label': 'xAPI envelope', 'collapsed': True,
                    'items': env_items})

    if not dry_run:
        (schema_docs_dir / 'index.md').write_text("\n".join(idx))
    return sidebar


def generate_vocabulary_pages(schema_name: str, data: Dict[str, Any],
                              schema_docs_dir: Path, dry_run: bool) -> List[Dict[str, Any]]:
    """Vocabulary (SKOS): a single grouped Overview page — one section per public
    concept scheme, each listing its concepts in a table (label, definition,
    data_type when present). Internal-status schemes/concepts are already excluded
    by the loader. Sidebar mirrors the simpler schemas: Overview (+ About if present).
    """
    metadata = data['metadata']
    schemes = data['schemes']
    n_concepts = sum(len(s['concepts']) for s in schemes)

    idx = [_schema_page_header(schema_name, metadata)]
    idx.append(f"\nThis controlled vocabulary defines **{n_concepts} terms** across "
               f"**{len(schemes)} concept schemes**. Terms a single schema owns live "
               f"in that schema; this resource holds the cross-cutting terms no single "
               f"schema owns.\n")

    for scheme in schemes:
        idx.append(f"\n## {scheme['label']}\n")
        if scheme.get('description'):
            idx.append(f"\n{_mdx_text(scheme['description'])}\n")
        idx.append("| Term | Type | Definition |")
        idx.append("|:-----|:-----|:-----------|")
        for c in scheme['concepts']:
            dt = f"`{c['data_type']}`" if c.get('data_type') else ''
            idx.append(f"| **{_mdx_cell(c['label'])}** | {dt} "
                       f"| {_mdx_cell(c['definition'])} |")

    if not dry_run:
        (schema_docs_dir / 'index.md').write_text("\n".join(idx) + "\n")

    sidebar: List[Dict[str, Any]] = [
        {'type': 'doc', 'id': f'{schema_name}/index', 'label': 'Overview'},
    ]
    # Include a hand-written About page in the nav if one exists (trial/event convention).
    if (schema_docs_dir / 'about.md').exists():
        sidebar.append({'type': 'doc', 'id': f'{schema_name}/about', 'label': 'About'})

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

            # Multi-table (trial) and vocabulary (event) schemas: full per-field pages
            # grouped by table / section, with a structured (per-table) sidebar.
            if schema_info.get('multi_table'):
                sidebar_configs[f"{schema_name}Sidebar"] = generate_trial_pages(
                    schema_name, data, schema_docs_dir, dry_run)
                n = sum(len(t.get('fields', [])) for t in data['tables'])
                print(f"   ✓ Generated {len(data['tables'])} tables, {n} field pages")
                continue
            if schema_info.get('vocabulary'):
                sidebar_configs[f"{schema_name}Sidebar"] = generate_event_pages(
                    schema_name, data, schema_docs_dir, dry_run)
                print(f"   ✓ Generated envelope field pages + vocabulary pages")
                continue
            if schema_info.get('skos_vocabulary'):
                sidebar_configs[f"{schema_name}Sidebar"] = generate_vocabulary_pages(
                    schema_name, data, schema_docs_dir, dry_run)
                n = sum(len(s['concepts']) for s in data['schemes'])
                print(f"   ✓ Generated Overview with {len(data['schemes'])} schemes, "
                      f"{n} concepts")
                continue

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
                            'requirement': 'required' if obj_prop.get('required', False) else 'optional',
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
