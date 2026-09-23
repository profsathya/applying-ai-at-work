/* Shared, answer-filled representation for table copying and feedback. */
(function (root) {
  'use strict';
  const escape = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const key = (task, row, column) => task.id + '.' + row.id + '.' + column.id;
  function answer(task, row, column, answers) {
    return String(answers[key(task, row, column)] || '');
  }
  function cellText(task, row, index, answers) {
    const cell = row.cells[index];
    const written = cell.response ? answer(task, row, task.columns[index], answers) : '';
    return [cell.text, written].filter(Boolean).join('\n');
  }
  function filledRow(task, row, answers) {
    return task.columns.map((_, index) => cellText(task, row, index, answers));
  }
  function rowResponse(task, row, answers) {
    if (!row.cells.some((cell, index) => cell.response &&
      answer(task, row, task.columns[index], answers).trim())) return '';
    return task.columns.map((column, index) => {
      const cell = row.cells[index];
      const written = cell.response ? answer(task, row, column, answers).trim() || '(not entered)' : '';
      return column.label + ': ' + [cell.text, written].filter(Boolean).join('\n');
    }).join('\n');
  }
  function html(task, answers) {
    const widths = task.columns.map(column => column.width || 1);
    const total = widths.reduce((sum, width) => sum + width, 0);
    const colgroup = '<colgroup>' + widths.map(width =>
      '<col style="width:' + (width / total * 100).toFixed(4) + '%">').join('') + '</colgroup>';
    const heads = task.columns.map(column =>
      '<th scope="col" style="border:1px solid #8999a5;padding:8px;background:#f2f5f7;text-align:left">' +
      escape(column.label) + '</th>').join('');
    const rows = task.rows.map(row => '<tr>' + filledRow(task, row, answers).map(value =>
      '<td style="border:1px solid #8999a5;padding:8px;vertical-align:top">' +
      escape(value).replace(/\n/g, '<br>') + '</td>').join('') + '</tr>').join('');
    return '<table style="border-collapse:collapse;width:100%;--walk-table-min-width:' +
      (task.columns.length * 180) + 'px">' + colgroup +
      '<thead><tr>' + heads + '</tr></thead><tbody>' + rows + '</tbody></table>';
  }
  function tsv(task, answers) {
    const quote = value => /[\t\r\n"]/.test(value) ? '"' + value.replace(/"/g, '""') + '"' : value;
    return [task.columns.map(column => column.label),
      ...task.rows.map(row => filledRow(task, row, answers))]
      .map(row => row.map(value => quote(String(value))).join('\t')).join('\n');
  }
  root.WalkthroughTables = {answer, cellText, filledRow, rowResponse, html, tsv};
}(globalThis));
