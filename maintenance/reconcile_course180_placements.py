"""Prepare local state/progress JSON for eight already-removed placements.

No Canvas or GitHub calls. Supply fresh input files; review output diffs before
applying through the protected state/hosted release workflow. Never run a broad
publisher merely to apply these metadata changes.
"""
import argparse
import copy
import json
from pathlib import Path

# original assignment, removed item, replacement assignment, retained item, module
PAIRS = [(7151,17979,7184,18019,2079), (7152,17980,7183,18018,2079),
         (7169,18001,7178,18011,2084), (7158,17990,7166,17998,2081),
         (7159,17991,7165,17997,2081), (7176,18009,7179,18012,2084),
         (7160,17992,7168,18000,2082), (7134,17954,7167,17999,2082)]

def reconcile(state, progress):
    state, progress = copy.deepcopy(state), copy.deepcopy(progress)
    if state.get('instance', {}).get('course_id') != 180 or state.get('instance', {}).get('base_url', '').rstrip('/') != 'https://cti-courses.instructure.com':
        raise ValueError('Expected CTI course 180 deployment state')
    if progress.get('canvasCourseId') != 180:
        raise ValueError('Expected course 180 progress map')
    for original, removed, replacement, retained, module in PAIRS:
        entries = list(state['artifacts'].values())
        sources = [e for e in entries if e.get('canvas_type') == 'assignment' and e.get('canvas_id') == original]
        targets = [e for e in entries if e.get('canvas_type') == 'assignment' and e.get('canvas_id') == replacement]
        if len(sources) != 1 or len(targets) != 1:
            raise ValueError(f'Ambiguous deployment identities for {original}')
        source, target = sources[0], targets[0]
        if source.get('canvas_module_item_id') not in (removed, None) or source.get('canvas_module_id') != module:
            raise ValueError(f'Original placement drift for {original}')
        if target.get('canvas_module_item_id') != retained or target.get('canvas_module_id') != module:
            raise ValueError(f'Walkthrough placement drift for {replacement}')
        rows = [e for e in progress['items'] if e.get('canvasType') == 'assignment' and e.get('canvasId') == original]
        if len(rows) != 1 or rows[0].get('canvasModuleItemId') not in (removed, None):
            raise ValueError(f'Progress mapping drift for {original}')
        source['canvas_module_item_id'] = None
        source.pop('completion_requirement', None)
        rows[0]['canvasModuleItemId'] = None
        rows[0]['completionRequirement'] = None
    return state, progress

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state',type=Path,required=True)
    p.add_argument('--progress',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    state,progress=reconcile(json.loads(a.state.read_text()),json.loads(a.progress.read_text()))
    a.output_dir.mkdir(parents=True,exist_ok=True)
    for name,data in [('production.json',state),('progress-map.json',progress)]:
        path=a.output_dir/name
        with path.open('x') as f:
            f.write(json.dumps(data,indent=2)+'\n')
    print('Prepared local outputs only; review exactly 8 placement IDs and 8 completion requirements in each file.')
