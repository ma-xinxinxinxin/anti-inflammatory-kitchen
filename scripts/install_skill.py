#!/usr/bin/env python3
"""Install the reviewed local skill into a supported agent's discovery directory.

No network calls, package installs, or changes to the agent's configuration.
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import tempfile
import uuid

from package_skill import ROOT, skill_files

PROFILES = {
    'codex': '.agents/skills',
    'claude': '.claude/skills',
    'cursor': '.cursor/skills',
    'gemini': '.gemini/skills',
    'agents': '.agents/skills',
}


def destination(tool, scope='user', project=None, home=None):
    if scope == 'project':
        if project is None:
            raise ValueError('--scope project requires --project /path/to/project')
        base = Path(project).expanduser().resolve()
        if not base.is_dir():
            raise ValueError('The project folder must already exist')
    else:
        base = Path(home) if home is not None else Path.home()
    target = base / PROFILES[tool] / 'kitchen'
    if tool == 'codex' and scope == 'user':
        legacy = base / '.codex/skills/kitchen'
        if legacy.exists() or legacy.is_symlink():
            if target.exists() or target.is_symlink():
                raise ValueError('Two Codex installations found (.agents and .codex); keep one before updating')
            return legacy
    return target


def install(target, *, update=False, dry_run=False):
    target = Path(target).expanduser().absolute()
    files = skill_files()
    if target.is_symlink():
        raise ValueError('Refusing to replace a symlink; select a real destination')
    resolved = target.resolve()
    if resolved == ROOT / 'kitchen' or ROOT / 'kitchen' in resolved.parents:
        raise ValueError('The source skill cannot be the installation destination')
    if target.exists() and not target.is_dir():
        raise ValueError('Installation destination is not a directory')
    if target.exists() and not update:
        raise FileExistsError(f'{target} already exists. Use --update to back it up before replacement.')
    if dry_run:
        return {'destination': str(target), 'files': len(files), 'dry_run': True}
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.kitchen-install-', dir=target.parent))
    backup = None
    try:
        for relative, source in files:
            output = stage / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, output)
        if target.exists():
            # Keep backups outside skills/ so agents do not discover duplicate skills.
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            backup = target.parent.parent / 'skill-backups' / f'kitchen-{stamp}-{uuid.uuid4().hex[:8]}'
            backup.parent.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
        try:
            stage.rename(target)
        except OSError:
            if backup is not None:
                backup.rename(target)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return {'destination': str(target), 'files': len(files), 'backup': str(backup) if backup else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tool', choices=PROFILES, required=True)
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--update', action='store_true', help='Back up an existing install, then replace it')
    parser.add_argument('--dry-run', action='store_true', help='Print the destination without writing')
    args = parser.parse_args()
    try:
        result = install(destination(args.tool, args.scope, args.project), update=args.update, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(('Would install: ' if args.dry_run else 'Installed: ') + result['destination'])
    if result.get('backup'):
        print('Previous installation backed up: ' + result['backup'])
    if not args.dry_run:
        print('Open a new agent session and ask it to use kitchen. This is a local installation, not cloud/mobile synchronization.')


if __name__ == '__main__':
    main()
