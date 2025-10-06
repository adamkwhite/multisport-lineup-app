#!/usr/bin/env python3
import os
import subprocess
import datetime
import shutil
from pathlib import Path

def run_tests_with_timestamped_results():
    """Run tests and organize results with timestamps while maintaining 'latest' links"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create test-results directory structure
    results_dir = Path('test-results')
    results_dir.mkdir(exist_ok=True)

    # Backend tests with timestamped coverage
    backend_coverage_dir = results_dir / f'backend-coverage-{timestamp}'
    subprocess.run([
        './lineup-venv/bin/pytest',
        'tests/api/',
        '--cov=app',
        '--cov-report=html:' + str(backend_coverage_dir),
        '--cov-report=xml:' + str(backend_coverage_dir / 'coverage.xml'),
        '--cov-report=term-missing',
        '--junit-xml=' + str(results_dir / f'backend-results-{timestamp}.xml')
    ])

    # Create/update 'latest' symlinks for easy access
    latest_backend = results_dir / 'backend-coverage-latest'
    if latest_backend.exists():
        latest_backend.unlink()
    latest_backend.symlink_to(backend_coverage_dir.name)

    # Frontend tests (Jest handles timestamping via config)
    subprocess.run(['npm', 'test', '--', '--coverage'])

    # Copy coverage files to root for SonarCube
    copy_coverage_for_sonarqube(timestamp, results_dir)

    print(f"\\n✅ Test results saved with timestamp: {timestamp}")
    print(f"📊 Latest backend coverage: test-results/backend-coverage-latest/index.html")
    print(f"📊 Latest frontend coverage: test-results/coverage-{timestamp}/index.html")
    print(f"📈 SonarCube coverage files: coverage.xml, lcov.info")

    # Cleanup old results (keep last 10)
    cleanup_old_results(results_dir, keep_count=10)

def copy_coverage_for_sonarqube(timestamp, results_dir):
    """Copy coverage files to root directory for SonarCube detection"""
    try:
        import shutil

        # Copy backend coverage XML
        backend_coverage_dir = results_dir / f'backend-coverage-{timestamp}'
        backend_xml = backend_coverage_dir / 'coverage.xml'
        if backend_xml.exists():
            shutil.copy2(backend_xml, 'coverage.xml')
            print(f"📄 Copied backend coverage to coverage.xml")

        # Find most recent frontend coverage directory (Jest uses different timestamp format)
        coverage_dirs = [
            d for d in results_dir.iterdir()
            if d.is_dir() and d.name.startswith('coverage-')
        ]
        if coverage_dirs:
            # Get the most recent one
            latest_frontend_dir = max(coverage_dirs, key=lambda x: x.stat().st_mtime)
            frontend_lcov = latest_frontend_dir / 'lcov.info'
            if frontend_lcov.exists():
                shutil.copy2(frontend_lcov, 'lcov.info')
                print(f"📄 Copied frontend coverage to lcov.info")

    except Exception as e:
        print(f"⚠️  Warning: Could not copy coverage files: {e}")

def cleanup_old_results(results_dir, keep_count=10):
    """Remove old test result directories, keeping only the most recent ones"""
    coverage_dirs = sorted([
        d for d in results_dir.iterdir()
        if d.is_dir() and (d.name.startswith('backend-coverage-') or d.name.startswith('coverage-'))
    ], key=lambda x: x.stat().st_mtime, reverse=True)

    for old_dir in coverage_dirs[keep_count:]:
        if 'latest' not in old_dir.name:
            shutil.rmtree(old_dir)
            print(f"🗑️  Cleaned up old results: {old_dir.name}")

if __name__ == '__main__':
    run_tests_with_timestamped_results()