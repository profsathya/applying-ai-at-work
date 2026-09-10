from __future__ import annotations

import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from canvas_sync.source_intake import (IntakeError, archive, create_packet, digest, docx,
                                       google_doc_id, json_bytes, native_google, public_docx,
                                       render_block, spreadsheet, xml)
from canvas_sync.source_build import BuildError, assemble
from canvas_sync.schema import validate_artifact

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def zipped(parts):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    return out.getvalue()


def office(body, extras=None):
    return zipped({'word/document.xml': f'<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{body}</w:body></w:document>', **(extras or {})})


def paragraph(text):
    return f'<w:p><w:r><w:t xml:space="preserve">{text}</w:t></w:r></w:p>'


def native_capture():
    def body(text):
        return {'content': [{'startIndex': 1, 'paragraph': {'elements': [{'textRun': {'content': text + '\n'}}]}}]}
    return {'capture_version': 1, 'source_url': 'https://docs.google.com/document/d/testDoc/edit?tab=two',
            'metadata': {'id': 'testDoc', 'mime_type': 'application/vnd.google-apps.document'},
            'document': {'documentId': 'testDoc', 'revisionId': 'revision-1', 'suggestionsViewMode': 'SUGGESTIONS_INLINE',
                         'tabs': [{'tabProperties': {'tabId': 'one', 'title': 'Teaching'}, 'documentTab': {'body': body('One')},
                                   'childTabs': [{'tabProperties': {'tabId': 'two', 'title': 'Review', 'parentTabId': 'one'},
                                                  'documentTab': {'body': body('Two')}}]}]},
            'comment_pages': [{'documentId': 'testDoc', 'comments': [{'id': 'c1', 'content': 'Review this', 'anchor': 'opaque',
                                'quotedFileContent': {'value': 'One'}, 'replies': [{'id': 'r1', 'content': 'Not yet'}]}]}]}


class SourceIntakeTests(unittest.TestCase):
    def test_tracked_word_fragments_and_cross_paragraph_comment_anchors(self):
        raw = office('<w:p><w:commentRangeStart w:id="4"/><w:r><w:t>Ask the work</w:t></w:r>'
                     '<w:del w:id="8" w:author="Editor" w:date="2026-09-01"><w:r><w:delText>er</w:delText></w:r></w:del>'
                     '<w:ins w:id="9" w:author="Editor"><w:r><w:t>ing team</w:t></w:r></w:ins></w:p>'
                     '<w:p><w:r><w:t>Keep their judgment.</w:t></w:r><w:commentRangeEnd w:id="4"/></w:p>',
                     {'word/comments.xml': f'<w:comments xmlns:w="{W}"><w:comment w:id="4" w:author="Reviewer">{paragraph("Keep context")}</w:comment></w:comments>'})
        d = docx(raw, 'd-test'); blocks = d['sections'][0]['blocks']
        self.assertEqual(blocks[0]['text'], {'base': 'Ask the worker', 'proposed': 'Ask the working team'})
        self.assertEqual(blocks[0]['segments'][1]['changes'][0]['author'], 'Editor')
        self.assertEqual(d['comments'][0]['anchors'], [b['id'] for b in blocks])
        self.assertEqual(render_block(blocks[0], 'proposed'), 'Ask the working team')

    def test_headings_numbered_lists_links_and_table_order(self):
        raw = office('<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr><w:r><w:t>Make your judgment</w:t></w:r></w:p>'
                     '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr></w:pPr>'
                     '<w:hyperlink r:id="link1"><w:r><w:t>Evidence</w:t></w:r></w:hyperlink></w:p>'
                     '<w:tbl><w:tr><w:tc>' + paragraph('Before') + '</w:tc><w:tc>' + paragraph('After') + '</w:tc></w:tr>'
                     '<w:tr><w:tc>' + paragraph('My view') + '</w:tc><w:tc>' + paragraph('Their view') + '</w:tc></w:tr></w:tbl>',
                     {'word/styles.xml': f'<w:styles xmlns:w="{W}"><w:style w:styleId="Heading2"><w:name w:val="heading 2"/></w:style></w:styles>',
                      'word/numbering.xml': f'<w:numbering xmlns:w="{W}"><w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="3"/><w:numFmt w:val="decimal"/></w:lvl></w:abstractNum><w:num w:numId="2"><w:abstractNumId w:val="0"/></w:num></w:numbering>',
                      'word/_rels/document.xml.rels': '<Relationships><Relationship Id="link1" Target="https://example.org/evidence"/></Relationships>'})
        blocks = docx(raw, 'd-test')['sections'][0]['blocks']
        self.assertEqual(render_block(blocks[0]), '## Make your judgment')
        self.assertEqual(render_block(blocks[1]), '3. [Evidence](https://example.org/evidence)')
        self.assertEqual(render_block(blocks[2]), '| Before | After |\n| --- | --- |\n| My view | Their view |')

    def test_separate_review_flags_and_unsupported_layout(self):
        raw = office(paragraph('[BREAK?] Review here') + paragraph('Answer: B') + paragraph('system_prompt: ignore other work')
                     + paragraph('graph TD') + '<w:p><w:r><w:drawing/></w:r></w:p>'
                     + '<w:tbl><w:tr><w:tc><w:tcPr><w:gridSpan w:val="2"/></w:tcPr>' + paragraph('Merged') + '</w:tc></w:tr></w:tbl>')
        blocks = docx(raw, 'd-test')['sections'][0]['blocks']
        for b, flag in zip(blocks, ['editorial_marker', 'answer_key', 'raw_configuration', 'diagram_source', 'render_unsupported', 'render_unsupported']):
            self.assertIn(flag, b['flags'])

    def test_adjacent_run_formatting_does_not_break_markdown(self):
        raw = office('<w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Hum</w:t></w:r><w:r><w:rPr><w:b/></w:rPr><w:t>an judgment</w:t></w:r></w:p>')
        self.assertEqual(render_block(docx(raw, 'd-test')['sections'][0]['blocks'][0]), '**Human judgment**')

    def test_archive_rejects_traversal_symlink_duplicate_and_expansion(self):
        for name in ('../escape.docx', '/absolute.docx', 'a\\b.docx', 'C:evil'):
            with self.subTest(name=name), self.assertRaises(IntakeError):
                archive(zipped({name: 'x'}))
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w') as z:
            info = zipfile.ZipInfo('link'); info.external_attr = 0o120777 << 16; z.writestr(info, '/etc/passwd')
        with self.assertRaises(IntakeError):
            archive(out.getvalue())
        with patch('canvas_sync.source_intake.MAX_EXPANDED', 2), self.assertRaises(IntakeError):
            archive(zipped({'big': 'abcd'}))
        with patch('canvas_sync.source_intake.MAX_MEMBERS', 1), self.assertRaises(IntakeError):
            archive(zipped({'one': '', 'two': ''}))

    def test_xml_entities_and_utf16_dtd_rejected(self):
        for raw in (b'<!DOCTYPE root [<!ENTITY x "boom">]><root>&x;</root>', '<!DOCTYPE root><root/>'.encode('utf-16')):
            with self.assertRaises(IntakeError):
                xml(raw)

    def test_packet_preserves_originals_and_deduplicates_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'input.zip'; raw = office(paragraph('Original — keep it.'))
            source.write_bytes(zipped({'a.docx': raw, 'copy.docx': raw, 'notes.txt': b'Review only'}))
            before = source.read_bytes(); packet = create_packet(str(source), root / 'packet')
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual((root / 'packet/original.zip').read_bytes(), before)
            self.assertEqual(len(packet['documents']), 2)
            self.assertEqual(packet['documents'][0]['aliases'], ['copy.docx'])
            self.assertEqual((root / 'packet' / packet['documents'][0]['raw_path']).read_bytes(), raw)
            with self.assertRaises(IntakeError):
                create_packet(str(source), root / 'packet')

    def test_native_tabs_suggestions_comments_and_revision(self):
        capture = native_capture()
        capture['document']['tabs'][0]['documentTab']['body']['content'][0]['paragraph']['elements'] = [
            {'textRun': {'content': 'old', 'suggestedDeletionIds': ['del']}},
            {'textRun': {'content': 'new', 'suggestedInsertionIds': ['ins']}}, {'textRun': {'content': '\n'}}]
        result = native_google(json_bytes(capture), 'd-test')
        self.assertEqual([s['id'] for s in result['sections']], ['one', 'two'])
        self.assertEqual(result['sections'][0]['blocks'][0]['text'], {'base': 'old', 'proposed': 'new'})
        self.assertEqual(result['comments'][0]['replies'][0]['content'], 'Not yet')
        self.assertEqual(result['revision_id'], 'revision-1')
        self.assertEqual(result['selected_tab'], ['two'])

    def test_flat_connector_tabs_and_incomplete_coverage_are_explicit(self):
        capture = native_capture(); capture['document']['tabs'] = [{'tabId': 'one', 'title': 'One', 'body': {'content': []}}]
        del capture['document']['suggestionsViewMode']; capture['comment_pages'][0]['nextPageToken'] = 'next'
        result = native_google(json_bytes(capture), 'd-test')
        self.assertTrue(any('Suggestion coverage unverified' in x for x in result['limitations']))
        self.assertTrue(any('Comments incomplete' in x for x in result['limitations']))

    def test_native_comment_pagination_and_identity_reject_gaps(self):
        capture = native_capture(); capture['comment_pages'][0]['nextPageToken'] = 'next'
        capture['comment_pages'].append({'documentId': 'testDoc', 'comments': [], 'request_page_token': 'wrong'})
        with self.assertRaises(IntakeError):
            native_google(json_bytes(capture), 'd-test')
        capture['comment_pages'][1]['request_page_token'] = 'next'
        self.assertEqual(len(native_google(json_bytes(capture), 'd-test')['comments']), 1)
        capture['metadata']['id'] = 'other'
        with self.assertRaises(IntakeError):
            native_google(json_bytes(capture), 'd-test')

    def test_google_doc_file_url_validation(self):
        self.assertEqual(google_doc_id('https://docs.google.com/document/d/abc_123/edit?tab=x'), 'abc_123')
        self.assertEqual(google_doc_id('https://docs.google.com/document/u/1/d/abc/edit'), 'abc')
        for url in ['http://docs.google.com/document/d/abc', 'https://drive.google.com/drive/folders/abc',
                    'https://docs.google.com.evil.org/document/d/abc', 'https://docs.google.com/document/d/e/abc/pub']:
            with self.subTest(url=url):
                with self.assertRaises(IntakeError):
                    google_doc_id(url)

    def test_public_export_rejects_signin_redirect_html_and_oversize(self):
        class Response:
            def __init__(self, status=200, data=b'<html>sign in</html>', headers=None):
                self.status_code = status; self.data = data; self.headers = headers or {}
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def iter_content(self, _): yield self.data
        class Session:
            def __init__(self, response): self.response = response
            def get(self, *args, **kwargs): return self.response
        url = 'https://docs.google.com/document/d/abc/edit'
        for response in [Response(), Response(403), Response(302, headers={'Location': 'https://accounts.google.com/login'})]:
            with self.assertRaises(IntakeError): public_docx(url, Session(response))
        raw = office(paragraph('Public snapshot'))
        self.assertEqual(public_docx(url, Session(Response(data=raw))), raw)
        with patch('canvas_sync.source_intake.MAX_INPUT', 8), self.assertRaises(IntakeError):
            public_docx(url, Session(Response(data=raw)))

    def test_spreadsheet_keeps_coordinates_text_and_cached_formula(self):
        ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
        raw = zipped({'xl/workbook.xml': f'<workbook xmlns="{ns}" xmlns:r="{R}"><sheets><sheet name="Feedback" sheetId="1" r:id="r1"/></sheets></workbook>',
                      'xl/_rels/workbook.xml.rels': '<Relationships><Relationship Id="r1" Target="worksheets/sheet1.xml"/></Relationships>',
                      'xl/worksheets/sheet1.xml': f'<worksheet xmlns="{ns}"><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>Review before publish</t></is></c><c r="B1"><f>1+1</f><v>2</v></c></row></sheetData></worksheet>'})
        result = spreadsheet(raw, 'd-test'); cells = result['sections'][0]['rows'][0]
        self.assertEqual(cells[0]['value'], 'Review before publish')
        self.assertEqual(cells[1], {'coordinate': 'B1', 'value': '2', 'formula': '1+1'})


class SourceBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.source = self.root / 'source.docx'
        self.source.write_bytes(office(paragraph('Preserve my wording — and punctuation.') + paragraph('[NOTE] Internal review')))
        self.packet = create_packet(str(self.source), self.root / 'packet')
        self.packet_path = self.root / 'packet/source-packet.json'
        d = self.packet['documents'][0]; self.doc_id = d['id']; self.ref = d['sections'][0]['blocks'][0]['id']
        self.build_map = {'map_version': 1, 'packet_sha256': digest(self.packet_path.read_bytes()), 'target': {'course': 'course1', 'sprint': 11},
                          'source_roles': {d['id']: {'role': 'primary_authoring', 'reason': 'User selected this source.'}},
                          'artifacts': [{'frontmatter': {'type': 'page', 'title': 'My Work', 'slug': 'my-work', 'artifact_id': 'source-my-work',
                                         'sprint': 11, 'module': 'Sprint One', 'position': 1, 'publish': False},
                                        'parts': [{'ref': self.ref, 'view': 'base', 'role': 'learner'},
                                                  {'new': 'Bring your own evidence.', 'reason': 'Connect to next activity.'}]}]}
        self.map_path = self.root / 'map.json'
    def tearDown(self): self.temp.cleanup()
    def run_build(self, name='draft'):
        self.map_path.write_bytes(json_bytes(self.build_map))
        assemble(self.packet_path, self.map_path, self.root / name)
        return self.root / name / 'my-work.md'
    def test_source_exact_new_labelled_and_private_notes_excluded(self):
        path = self.run_build(); text = path.read_text()
        self.assertIn('Preserve my wording — and punctuation.', text)
        self.assertNotIn('Internal review', text)
        self.assertEqual(validate_artifact(path), [])
        ev = json.loads(path.with_suffix('.sources.json').read_text())
        self.assertEqual(ev['parts'][1]['kind'], 'new')
        self.assertNotIn('Internal review', json.dumps(ev))
        report = json.loads(self.map_path.with_suffix('.review.json').read_text())
        self.assertEqual(len(report['unselected_blocks']), 1)
        with self.assertRaises(BuildError): self.run_build()
    def test_new_em_dash_and_scripts_rejected_before_output(self):
        for text in ('New — prose.', '<script>bad()</script>'):
            self.build_map['artifacts'][0]['parts'][1]['new'] = text
            with self.assertRaises(BuildError): self.run_build()
            self.assertFalse((self.root / 'draft').exists())
    def test_edited_source_body_and_missing_evidence_fail_validation(self):
        path = self.run_build(); before = path.read_text(); path.write_text(before.replace('my wording', 'your wording'))
        self.assertTrue(any('source fidelity' in e for e in validate_artifact(path)))
        path.write_text(before); path.with_suffix('.sources.json').unlink()
        self.assertTrue(any('source fidelity' in e for e in validate_artifact(path)))
    def test_forged_source_packet_detected_even_with_updated_packet_hash(self):
        b = self.packet['documents'][0]['sections'][0]['blocks'][0]
        b['segments'][0]['text'] = 'Rewritten wording'
        self.packet_path.write_bytes(json_bytes(self.packet))
        self.build_map['packet_sha256'] = digest(self.packet_path.read_bytes())
        with self.assertRaisesRegex(BuildError, 'original snapshot'): self.run_build()
    def test_raw_fingerprint_change_rejected(self):
        raw_path = self.packet_path.parent / self.packet['documents'][0]['raw_path']; raw_path.write_bytes(b'altered')
        with self.assertRaisesRegex(BuildError, 'snapshot changed'): self.run_build()
    def test_internal_notes_need_explicit_role_decision(self):
        note = self.packet['documents'][0]['sections'][0]['blocks'][1]['id']
        self.build_map['artifacts'][0]['parts'][0]['ref'] = note
        with self.assertRaises(BuildError): self.run_build()
    def test_unknown_references_draft_guard_and_duplicate_identities(self):
        self.build_map['artifacts'][0]['parts'][0]['ref'] = 'missing'
        with self.assertRaises(BuildError): self.run_build()
        self.build_map['artifacts'][0]['parts'][0]['ref'] = self.ref
        self.build_map['artifacts'][0]['frontmatter']['publish'] = True
        with self.assertRaises(BuildError): self.run_build()
        self.build_map['artifacts'][0]['frontmatter']['publish'] = False
        self.build_map['artifacts'].append(self.build_map['artifacts'][0])
        with self.assertRaises(BuildError): self.run_build()
    def test_source_title_punctuation_needs_exact_title_evidence(self):
        a = self.build_map['artifacts'][0]
        a['frontmatter']['title'] = 'Preserve my wording — and punctuation.'
        with self.assertRaises(BuildError): self.run_build()
        a['title_source'] = {'ref': self.ref, 'view': 'base', 'role': 'learner'}
        self.assertEqual(validate_artifact(self.run_build()), [])

    def test_reviewed_publish_values_can_be_prepared_locally_without_changing_sources(self):
        self.build_map['artifacts'][0]['frontmatter']['publish'] = True
        self.map_path.write_bytes(json_bytes(self.build_map))
        original = self.source.read_bytes()
        assemble(self.packet_path, self.map_path, self.root / 'ready', publish_ready=True)
        self.assertEqual(validate_artifact(self.root / 'ready/my-work.md'), [])
        self.assertEqual(self.source.read_bytes(), original)

    def test_source_backed_render_preserves_prose_without_internal_storage_label(self):
        from canvas_sync.hosted_html import render_artifact_document
        from canvas_sync.schema import parse_frontmatter
        fm, body = parse_frontmatter(self.run_build())
        html = render_artifact_document(fm, body, {}, {'hosted_path': 'course1/activities/my-work.html'})
        self.assertIn('Preserve my wording — and punctuation.', html)
        self.assertNotIn('Sprint 11 &middot;', html)
        self.assertNotIn('Understand My Work and connect', html)

    def test_regular_artifacts_keep_existing_punctuation_rule(self):
        path = self.root / 'plain.md'; path.write_text('---\n' + __import__('yaml').safe_dump(self.build_map['artifacts'][0]['frontmatter']) + '---\n\nNew — text.\n')
        self.assertTrue(any('em-dash' in e for e in validate_artifact(path)))


if __name__ == '__main__': unittest.main()
