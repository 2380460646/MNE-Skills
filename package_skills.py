#!/usr/bin/env python3
"""Package all skills into .skill files"""

import sys
import zipfile
from pathlib import Path

def package_skill(skill_path, output_dir):
    """Package a skill folder into a .skill file."""
    skill_path = Path(skill_path).resolve()
    output_dir = Path(output_dir).resolve()

    # Validate skill folder exists
    if not skill_path.exists() or not skill_path.is_dir():
        print(f"Error: Skill folder not found: {skill_path}")
        return False

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        return False

    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create .skill file (zip archive)
    skill_name = skill_path.name
    output_file = output_dir / f"{skill_name}.skill"

    print(f"Packaging {skill_name}...")

    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)

    print(f"Created: {output_file}")
    return True

def main():
    # List of skill directories
    skills = [
        "mne-core",
        "mne-connectivity",
        "mne-icalabel",
        "mne-microstates",
        "autoreject"
    ]

    output_dir = "dist"

    print("Starting skill packaging...\n")

    success_count = 0
    for skill in skills:
        if package_skill(skill, output_dir):
            success_count += 1
        print()

    print(f"Packaging complete: {success_count}/{len(skills)} skills packaged successfully")

if __name__ == "__main__":
    main()
