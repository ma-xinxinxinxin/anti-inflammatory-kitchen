"""New-user installation and distribution acceptance tests, using isolated homes."""
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import install_skill as installer
import package_skill as builder


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'new user'

    def test_all_native_profiles_work_without_existing_configuration(self):
        for tool, folder in [('codex', '.agents'), ('claude', '.claude'),
                             ('cursor', '.cursor'), ('gemini', '.gemini')]:
            with self.subTest(tool=tool):
                target = installer.destination(tool, home=self.home)
                installer.install(target)
                self.assertEqual(target, self.home / folder / 'skills/kitchen')
                for name in builder.SKILL_FILES:
                    self.assertEqual((target / name).read_bytes(), (ROOT / 'kitchen' / name).read_bytes())
                result = subprocess.run(
                    [sys.executable, str(target / 'scripts/kitchen.py'), 'fridge', '--items', '菠菜, 豆腐, 三文鱼'],
                    cwd=self.temp.name, capture_output=True, encoding='utf-8',
                    env={**os.environ, 'PYTHONUTF8': '1'},
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('菠菜', result.stdout)
                rows = [line for line in result.stdout.splitlines()
                        if line.startswith('| ') and not line.startswith('| 类别')]
                self.assertEqual(len(rows), 19)

    def test_cli_project_install_with_spaces_and_no_user_state_changes(self):
        project = Path(self.temp.name) / 'my project'
        state = project / '.kitchen-state/kitchen-fridge.md'
        state.parent.mkdir(parents=True)
        state.write_text('Private fictional inventory', encoding='utf-8')
        before = state.read_bytes()
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/install_skill.py'),
                                 '--tool', 'cursor', '--scope', 'project', '--project', str(project)],
                                capture_output=True, encoding='utf-8', cwd=self.temp.name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((project / '.cursor/skills/kitchen/SKILL.md').is_file())
        self.assertEqual(state.read_bytes(), before)
        self.assertFalse((project / '.agents').exists())

    def test_legacy_codex_is_upgraded_in_place_without_duplicate(self):
        legacy = self.home / '.codex/skills/kitchen'
        legacy.mkdir(parents=True)
        (legacy / 'SKILL.md').write_text('old rules', encoding='utf-8')
        target = installer.destination('codex', home=self.home)
        self.assertEqual(target, legacy)
        result = installer.install(target, update=True)
        self.assertEqual((Path(result['backup']) / 'SKILL.md').read_text(), 'old rules')
        self.assertFalse((self.home / '.agents').exists())
        self.assertIn('v5.2', (legacy / 'SKILL.md').read_text(encoding='utf-8'))

    def test_duplicate_codex_locations_require_resolution(self):
        for folder in ['.codex', '.agents']:
            (self.home / folder / 'skills/kitchen').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'Two Codex'):
            installer.destination('codex', home=self.home)

    def test_existing_install_not_overwritten_without_update(self):
        target = installer.destination('claude', home=self.home)
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('custom rules')
        with self.assertRaises(FileExistsError):
            installer.install(target)
        self.assertEqual((target / 'SKILL.md').read_text(), 'custom rules')

    def test_update_preserves_custom_files_only_in_backup(self):
        target = installer.destination('gemini', home=self.home)
        target.mkdir(parents=True)
        (target / 'personal-note.txt').write_text('user customization')
        result = installer.install(target, update=True)
        backup = Path(result['backup'])
        self.assertNotIn(target.parent, backup.parents)
        self.assertEqual((backup / 'personal-note.txt').read_text(), 'user customization')
        self.assertFalse((target / 'personal-note.txt').exists())

    def test_dry_run_does_not_create_directories(self):
        target = installer.destination('cursor', home=self.home)
        installer.install(target, dry_run=True)
        self.assertFalse(self.home.exists())

    def test_project_must_be_explicit_and_exist(self):
        for project in [None, self.home / 'missing']:
            with self.assertRaises(ValueError):
                installer.destination('claude', scope='project', project=project)

    def test_source_cannot_be_installation_destination(self):
        with self.assertRaisesRegex(ValueError, 'source skill'):
            installer.install(ROOT / 'kitchen', update=True)

    @unittest.skipIf(os.name == 'nt', 'Windows symlinks require additional permissions')
    def test_symlink_target_is_not_replaced(self):
        real = Path(self.temp.name) / 'real'
        real.mkdir()
        link = Path(self.temp.name) / 'link'
        link.symlink_to(real, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            installer.install(link, update=True)
        self.assertTrue(link.is_symlink())


class DistributionTests(unittest.TestCase):
    def test_zip_extracts_to_complete_installable_skill(self):
        with ZipFile(io.BytesIO(builder.archive_bytes())) as archive:
            self.assertEqual(len(archive.namelist()), 7)
            self.assertEqual(archive.read('kitchen/SKILL.md'), (ROOT / 'kitchen/SKILL.md').read_bytes())
            with tempfile.TemporaryDirectory() as folder:
                archive.extractall(folder)
                skill = Path(folder) / 'kitchen'
                for ref in re.findall(r'\]\((references/[^)]+)\)', (skill / 'SKILL.md').read_text(encoding='utf-8')):
                    self.assertTrue((skill / ref).is_file(), ref)
                self.assertTrue((skill / 'scripts/kitchen.py').is_file())

    def test_accidental_private_files_are_excluded(self):
        # Place a fictional sentinel outside the allowlist, then ensure neither format leaks it.
        with tempfile.NamedTemporaryFile(dir=ROOT / 'kitchen', prefix='private-test-', suffix='.md') as f:
            f.write(b'PRIVATE-SENTINEL-DO-NOT-SHIP')
            f.flush()
            with ZipFile(io.BytesIO(builder.archive_bytes())) as archive:
                self.assertNotIn('kitchen/' + Path(f.name).name, archive.namelist())
                self.assertFalse(any(b'PRIVATE-SENTINEL' in archive.read(name) for name in archive.namelist()))
            self.assertNotIn(b'PRIVATE-SENTINEL', builder.chat_guide())

    def test_chat_guide_is_self_contained_for_references(self):
        guide = builder.chat_guide().decode('utf-8')
        self.assertIn('v5.2', guide)
        self.assertNotRegex(guide, r'\]\(references/')
        for anchor in ['workflow', 'food-table', 'state-files', 'recipe-rules', 'visuals']:
            self.assertIn(f'<a id="{anchor}"></a>', guide)
        self.assertIn('not an account-wide skill installation', guide)
        self.assertIn('Python helper is not included', guide)

    def test_committed_downloads_are_current(self):
        for name, content in builder.distributions().items():
            self.assertEqual((ROOT / 'downloads' / name).read_bytes(), content, name)

    def test_readme_language_tabs_and_local_document_links(self):
        for filename, other in [('README.md', 'README.en.md'), ('README.en.md', 'README.md')]:
            content = (ROOT / filename).read_text(encoding='utf-8')
            self.assertIn(f'href="{other}"', content)
        for doc in [ROOT / 'README.md', ROOT / 'README.en.md', *sorted((ROOT / 'docs').glob('*.md'))]:
            content = doc.read_text(encoding='utf-8')
            for link in re.findall(r'\]\(([^)]+)\)|href="([^"]+)"', content):
                target = next(part for part in link if part).split('#')[0]
                if target and not re.match(r'\w+://', target):
                    self.assertTrue((doc.parent / target).exists(), f'{doc.name}: {target}')


if __name__ == '__main__':
    unittest.main()
