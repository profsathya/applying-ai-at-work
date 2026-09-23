/* Client-side Word export; participant responses never reach an export service. */
(function (root) {
  'use strict';
  const encoder = new TextEncoder();
  const bytes = text => encoder.encode(text);
  const escape = text => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  function crc32(data) {
    let crc = 0xffffffff;
    for (const octet of data) {
      crc ^= octet;
      for (let i = 0; i < 8; i++) crc = (crc >>> 1) ^ (crc & 1 ? 0xedb88320 : 0);
    }
    return (crc ^ 0xffffffff) >>> 0;
  }
  function u16(value) { return [value & 255, (value >>> 8) & 255]; }
  function u32(value) { return [value & 255, (value >>> 8) & 255, (value >>> 16) & 255, (value >>> 24) & 255]; }
  function zip(entries) {
    const parts = [], directory = [];
    let offset = 0;
    for (const [name, text] of entries) {
      const nameBytes = bytes(name), data = bytes(text), crc = crc32(data);
      const local = new Uint8Array([
        ...u32(0x04034b50), ...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0),
        ...u32(crc), ...u32(data.length), ...u32(data.length), ...u16(nameBytes.length), ...u16(0),
      ]);
      parts.push(local, nameBytes, data);
      directory.push(new Uint8Array([
        ...u32(0x02014b50), ...u16(20), ...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0),
        ...u32(crc), ...u32(data.length), ...u32(data.length), ...u16(nameBytes.length), ...u16(0),
        ...u16(0), ...u16(0), ...u16(0), ...u32(0), ...u32(offset),
      ]), nameBytes);
      offset += local.length + nameBytes.length + data.length;
    }
    const directorySize = directory.reduce((sum, part) => sum + part.length, 0);
    parts.push(...directory, new Uint8Array([
      ...u32(0x06054b50), ...u16(0), ...u16(0), ...u16(entries.length), ...u16(entries.length),
      ...u32(directorySize), ...u32(offset), ...u16(0),
    ]));
    return new Blob(parts, {type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
  }
  function paragraph(text, style) {
    const heading = style ? '<w:pPr><w:pStyle w:val="' + style + '"/></w:pPr>' : '';
    return '<w:p>' + heading + '<w:r><w:t xml:space="preserve">' + escape(text) + '</w:t></w:r></w:p>';
  }
  function cell(text, width, header) {
    return '<w:tc><w:tcPr><w:tcW w:w="' + width + '" w:type="dxa"/>' +
      (header ? '<w:shd w:fill="F2F5F7"/>' : '') + '</w:tcPr>' +
      String(text).split('\n').map(line => header
        ? '<w:p><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">' + escape(line) + '</w:t></w:r></w:p>'
        : paragraph(line)).join('') + '</w:tc>';
  }
  function table(rows, weights, hasHeader = true) {
    const widths = weights ? weights.map(weight => Math.round(weight / weights.reduce((sum, n) => sum + n, 0) * 10500))
      : rows[0].length === 3 ? [2400, 4200, 3900] : [3500, 7000];
    return '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>' +
      ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'].map(edge =>
        '<w:' + edge + ' w:val="single" w:sz="4" w:color="B8C8D2"/>').join('') +
      '</w:tblBorders></w:tblPr><w:tblGrid>' + widths.map(width => '<w:gridCol w:w="' + width + '"/>').join('') + '</w:tblGrid>' +
      rows.map((row, index) => '<w:tr>' + (hasHeader && index === 0 ? '<w:trPr><w:tblHeader w:val="1"/></w:trPr>' : '') +
        row.map((value, column) => cell(value, widths[column], hasHeader && index === 0)).join('') + '</w:tr>').join('') + '</w:tbl>';
  }
  function build(config, answers) {
    const blocks = [paragraph(config.title, 'Title')];
    for (const line of config.documentPrefix || []) blocks.push(paragraph(line));
    for (const task of config.tasks) {
      blocks.push(paragraph(task.prompt, 'Heading1'));
      if (task.kind === 'table') {
        const rows = [...(task.header_rows === 0 ? [] : [task.columns.map(column => column.label)]),
          ...task.rows.map(row => globalThis.WalkthroughTables.filledRow(task, row, answers))];
        blocks.push(table(rows, task.columns.map(column => column.width || 1), task.header_rows !== 0));
      } else if (task.kind === 'group') {
        for (let i = 1; i <= task.repeat_count; i++) {
          blocks.push(paragraph(task.repeat_labels?.[i - 1] || 'Entry ' + i, 'Heading2'));
          const evidence = task.fields.some(field => field.evidence_status);
          const rows = [evidence ? ['Field', 'Your answer', 'Confirmed or Inferred, and why'] : ['Field', 'Your answer']];
          for (const field of task.fields) {
            const key = task.id + '.' + i + '.' + field.id;
            const status = answers[key + '.status'] || '';
            const reason = answers[key + '.reason'] || '';
            const row = [field.label, answers[key] || ''];
            if (evidence) row.push(field.evidence_status ? [status, reason].filter(Boolean).join(': ') : '');
            rows.push(row);
          }
          blocks.push(table(rows));
        }
      } else {
        const value = String(answers[task.id] || '');
        for (const line of value.split('\n')) blocks.push(paragraph(line));
      }
      for (const line of task.document_after || []) blocks.push(paragraph(line));
    }
    for (const line of config.documentSuffix || []) blocks.push(paragraph(line));
    const documentXml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' +
      blocks.join('') + '<w:sectPr/></w:body></w:document>';
    const types = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">' +
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>' +
      '<Default Extension="xml" ContentType="application/xml"/>' +
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>' +
      '</Types>';
    const relationships = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>' +
      '</Relationships>';
    return zip([['[Content_Types].xml', types], ['_rels/.rels', relationships], ['word/document.xml', documentXml]]);
  }
  root.WalkthroughDocx = {build};
}(globalThis));
