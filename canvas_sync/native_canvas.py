"""Opt-in portable navigation for generated hosted course documents.

Canvas remains the authority for completion and submissions. This final renderer
pass touches only generator-owned navigation/progress markup, leaving authored
references, form controls, downloads and AI activity configuration intact.
"""
import json
import re


def apply_native_canvas(document: str, manifest: dict) -> str:
    if not manifest.get('hosted_html', {}).get('native_canvas_navigation'):
        return document
    if 'data-native-canvas-navigation' in document:
        return document
    document = re.sub(r'canvasUrl: activityContext === \'canvas\' \? "[^"]*" : null', 'canvasUrl: null', document)
    # A hosted iframe cannot reliably learn the enclosing course/assignment URL:
    # cross-origin referrer policies often expose only the origin. Instructions
    # use the enclosing Canvas controls instead of guessing destination IDs.
    document = re.sub(r'<a\b[^>]*\bdata-canvas-only\b[^>]*>.*?</a>', '', document, flags=re.S)
    # Scheduled navigation is generated from this deployment's manifest/state.
    # Keep its native module/item destinations separate from completion tracking.
    scheduled = 'id="course-schedule"' in document
    if not scheduled:
        document = re.sub(r'\sdata-canvas-(?:href|target)="[^"]*"', '', document)
    document = re.sub(r'<span class="progress-check"[^>]*><span class="progress-box"></span><span class="progress-label">.*?</span></span>', '', document, flags=re.S)
    document = re.sub(r'\sdata-(?:progress-id|progress-state|canvas-module-item-id|completion-requirement)="[^"]*"', '', document)
    document = re.sub(r'^[ \t]*<div class="progress-status" id="progress-status" hidden></div>\n', '', document, flags=re.M)
    # The directory's progress client is a single generator-owned block. Do not
    # touch other scripts (walkthrough drafts, DOCX downloads, AI, disclosure).
    document = re.sub(r'      var progressEndpoint = .*?      loadProgress\(\);\n', '', document, flags=re.S)
    # Scheduled homepages only transported progress tokens; remove that client
    # block as well, including the storage-blocked forwarding fallback.
    document = re.sub(r'  const hash = new URLSearchParams\(root.location.hash.slice\(1\)\);.*?(?=  function moduleHref)', '', document, flags=re.S)
    document = re.sub(r'    // Only carry a token[^\n]*\n    if \(unsavedToken[^\n]*\n', '', document)
    def portable_schedule(match):
        data = json.loads(match[2])
        data['native_completion'] = True
        return match[1] + json.dumps(data) + match[3]
    document = re.sub(r'(<script id="course-schedule" type="application/json">)(.*?)(</script>)', portable_schedule, document, flags=re.S)
    setup = '''<style data-native-canvas-navigation>
html.native-canvas-context .back-link { display: none !important; }
</style>
<script>
(function () {
  var ctx = new URLSearchParams(location.search).get('context') || (self !== top ? 'canvas' : 'web');
  if (ctx !== 'canvas') return;
  document.documentElement.classList.add('native-canvas-context');
})();
</script>
'''
    document = document.replace('</head>', setup + '</head>', 1)
    return document
