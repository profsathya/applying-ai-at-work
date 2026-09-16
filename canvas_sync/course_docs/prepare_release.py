"""Download a trusted successful publication inventory and verify hosting."""
import io
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.request
import zipfile


def api(repo, path, token=None, raw=False):
    request = urllib.request.Request('https://api.github.com/repos/' + repo + path,
        headers={'Authorization': 'Bearer ' + (token or os.environ['GH_TOKEN']), 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read() if raw else json.load(response)


def deployment_succeeded(statuses):
    # GitHub marks older successful Pages deployments inactive once superseded.
    # That does not erase evidence that this exact release was deployed.
    return any(status.get('state') == 'success' for status in statuses)


def main():
    config = json.loads(Path('config/course-docs.json').read_text())
    repo = os.environ['GITHUB_REPOSITORY']
    # Always use newest successful release; a delayed callback must not restore
    # an older publication merely because its sync run was created later.
    runs = api(repo, '/actions/workflows/publish-canvas.yml/runs?branch=main&status=success&per_page=100')['workflow_runs']
    runs = sorted(runs, key=lambda r: r['id'], reverse=True)
    run = artifact = None
    for candidate in runs:
        if candidate['head_repository']['full_name'] != repo or candidate['head_branch'] != 'main':
            continue
        artifacts = api(repo, '/actions/runs/' + str(candidate['id']) + '/artifacts')['artifacts']
        selected = next((a for a in artifacts if a['name'] == config['release_artifact']), None)
        if selected is None:
            continue  # Other-course, hosted-only, or pre-feature successful run.
        if selected['expired']:
            raise ValueError('Newest eligible release artifact expired; republish rather than use stale fallback')
        run, artifact = candidate, selected
        break
    if not run:
        raise ValueError('No trusted successful main publication with a release inventory exists')
    subprocess.run(['git', 'merge-base', '--is-ancestor', run['head_sha'], 'HEAD'], check=True)
    archive = zipfile.ZipFile(io.BytesIO(api(repo, '/actions/artifacts/' + str(artifact['id']) + '/zip', raw=True)))
    candidates = [n for n in archive.namelist() if n == 'course-context-release.json']
    if len(candidates) != 1:
        raise ValueError('Expected exactly one root release inventory')
    content = archive.read(candidates[0])
    release = json.loads(content)
    if release.get('source_commit') != run['head_sha']:
        raise ValueError('Inventory source differs from successful publication')
    hosted = release.get('hosted_commit', '')
    if len(hosted) != 40 or any(c not in '0123456789abcdef' for c in hosted):
        raise ValueError('Missing exact hosted commit')
    token = os.environ.get('HOSTED_READ_TOKEN') or os.environ['GH_TOKEN']
    for attempt in range(40):
        deployments = api(config['hosted_repository'], '/deployments?environment=github-pages&sha=' + hosted, token)
        for deployment in deployments:
            statuses = api(config['hosted_repository'], '/deployments/' + str(deployment['id']) + '/statuses', token)
            if deployment_succeeded(statuses):
                Path('course-context-release.json').write_bytes(content)
                return
        time.sleep(15)
    raise ValueError('No successful Pages deployment for the exact hosted release; retry after deployment')


if __name__ == '__main__':
    main()
