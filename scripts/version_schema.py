#!/usr/bin/env python3
"""
Schema Versioning Script

Automates the versioning process for Behaverse schemas:
1. Detects which schema changed
2. Archives the old version to versions/ directory
3. Bumps the version using CalVer (YY.MMDD format)
4. Updates the CHANGELOG.md with changes
5. Commits changes and triggers deployment

Usage:
    python scripts/version_schema.py <schema_name> [--message "Change description"]
    
    schema_name: bcsvw, collection, dataset, or studyflow
    --message: Description of changes (required)

Example:
    python scripts/version_schema.py bcsvw --message "Add new validation rules"
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


def get_calver() -> str:
    """Generate CalVer version string (YY.MMDD)."""
    now = datetime.now()
    return f"{now.strftime('%y.%m%d')}"


def read_schema(schema_path: Path) -> Dict:
    """Read and parse JSON schema file."""
    with open(schema_path, 'r') as f:
        return json.load(f)


def write_schema(schema_path: Path, schema: Dict) -> None:
    """Write schema to JSON file with pretty formatting."""
    with open(schema_path, 'w') as f:
        json.dump(schema, f, indent=2)
        f.write('\n')  # Ensure trailing newline


def archive_version(schema_dir: Path, current_version: str) -> Path:
    """Archive current schema version to versions/ directory."""
    schema_file = schema_dir / "schema.json"
    versions_dir = schema_dir / "versions"
    versions_dir.mkdir(exist_ok=True)
    
    # Create versioned filename
    archived_file = versions_dir / f"schema-v{current_version}.json"
    
    # Copy current schema to versions
    shutil.copy2(schema_file, archived_file)
    print(f"✓ Archived version {current_version} to {archived_file}")
    
    return archived_file


def update_changelog(schema_dir: Path, old_version: str, new_version: str, 
                     change_message: str) -> None:
    """Update CHANGELOG.md with new version entry."""
    changelog_path = schema_dir / "CHANGELOG.md"
    
    if not changelog_path.exists():
        print(f"⚠ Warning: {changelog_path} not found, skipping changelog update")
        return
    
    with open(changelog_path, 'r') as f:
        content = f.read()
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Create new changelog entry
    new_entry = f"""
## [{new_version}] - {today}

### Changed
- {change_message}
"""
    
    # Find where to insert (after the header, before the first version)
    lines = content.split('\n')
    insert_idx = None
    
    for i, line in enumerate(lines):
        if line.startswith('## ['):
            insert_idx = i
            break
    
    if insert_idx is None:
        # If no version found, append at end
        new_content = content + new_entry
    else:
        # Insert before first version
        lines.insert(insert_idx, new_entry.strip())
        lines.insert(insert_idx + 1, '')
        new_content = '\n'.join(lines)
    
    with open(changelog_path, 'w') as f:
        f.write(new_content)
    
    print(f"✓ Updated {changelog_path}")


def bump_version(schema_dir: Path, change_message: str) -> tuple[str, str]:
    """
    Bump schema version and update files.
    
    Returns:
        tuple: (old_version, new_version)
    """
    schema_file = schema_dir / "schema.json"
    
    if not schema_file.exists():
        print(f"✗ Error: {schema_file} not found")
        sys.exit(1)
    
    # Read current schema
    schema = read_schema(schema_file)
    old_version = schema.get('version', 'unknown')
    new_version = get_calver()
    
    print(f"Schema: {schema_dir.name}")
    print(f"Old version: {old_version}")
    print(f"New version: {new_version}")
    
    if old_version == new_version:
        print(f"⚠ Warning: Version unchanged ({new_version}). Multiple updates on same day will have same version.")
    
    # Archive old version
    archive_version(schema_dir, old_version)
    
    # Update version in schema
    schema['version'] = new_version
    write_schema(schema_file, schema)
    print(f"✓ Updated version in {schema_file}")
    
    # Update changelog
    update_changelog(schema_dir, old_version, new_version, change_message)
    
    return old_version, new_version


def main():
    parser = argparse.ArgumentParser(
        description='Version a Behaverse schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'schema',
        choices=['bcsvw', 'collection', 'dataset', 'studyflow'],
        help='Schema to version'
    )
    parser.add_argument(
        '--message', '-m',
        required=True,
        help='Description of changes for CHANGELOG'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    args = parser.parse_args()
    
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    schema_dir = project_root / args.schema
    
    if not schema_dir.exists():
        print(f"✗ Error: Schema directory {schema_dir} not found")
        sys.exit(1)
    
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
        schema_file = schema_dir / "schema.json"
        if schema_file.exists():
            schema = read_schema(schema_file)
            old_version = schema.get('version', 'unknown')
            new_version = get_calver()
            print(f"Would bump {args.schema} from {old_version} to {new_version}")
            print(f"Would add changelog entry: {args.message}")
        return
    
    # Perform versioning
    old_version, new_version = bump_version(schema_dir, args.message)
    
    print(f"\n✓ Versioning complete!")
    print(f"\nNext steps:")
    print(f"  1. Review the changes in {args.schema}/")
    print(f"  2. Commit: git add {args.schema}/ && git commit -m 'chore({args.schema}): bump version to {new_version}'")
    print(f"  3. Push: git push origin main")
    print(f"  4. The deployment workflow will automatically regenerate docs")


if __name__ == '__main__':
    main()
