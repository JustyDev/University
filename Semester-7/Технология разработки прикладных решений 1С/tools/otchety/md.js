const { Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
        WidthType, ShadingType, BorderStyle, ExternalHyperlink } = require('docx');

const FONT = 'Times New Roman';
const SZ = 24;          // 12 pt
const CODE_FONT = 'Consolas';

function inlineRuns(text, base = {}) {
  // **bold**, `code`, [text](url) -> runs
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))/g;
  let last = 0, m;
  const push = (t, opts) => { if (t) out.push(new TextRun(Object.assign({ text: t, font: FONT, size: SZ }, base, opts))); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith('**')) push(tok.slice(2, -2), { bold: true });
    else if (tok.startsWith('`')) push(tok.slice(1, -1), { font: CODE_FONT, size: SZ - 4 });
    else {
      const mm = /^\[([^\]]+)\]\(([^)]+)\)$/.exec(tok);
      out.push(new ExternalHyperlink({
        link: mm[2],
        children: [new TextRun({ text: mm[1], font: FONT, size: SZ, style: 'Hyperlink' })],
      }));
    }
    last = m.index + tok.length;
  }
  push(text.slice(last));
  return out.length ? out : [new TextRun({ text: '', font: FONT, size: SZ })];
}

const SPACING = { line: 360, after: 120 };

function para(text, opts = {}) {
  return new Paragraph(Object.assign({ children: inlineRuns(text), spacing: SPACING,
    alignment: AlignmentType.JUSTIFIED, indent: { firstLine: 709 } }, opts));
}

function codeBlock(lines) {
  return lines.map((l, i) => new Paragraph({
    children: [new TextRun({ text: l || ' ', font: CODE_FONT, size: 20 })],
    spacing: { line: 240, after: i === lines.length - 1 ? 160 : 0, before: i === 0 ? 120 : 0 },
    shading: { type: ShadingType.CLEAR, fill: 'F4F4F4' },
    indent: { left: 340 },
  }));
}

const TOTAL = 9355; // ширина текста для A4 с полями 2/1.5 см (dxa)

function mkTable(rows) {
  const n = rows[0].length;
  const widths = [];
  for (let i = 0; i < n; i++) widths.push(Math.floor(TOTAL / n));
  widths[n - 1] = TOTAL - widths.slice(0, n - 1).reduce((a, b) => a + b, 0);
  return new Table({
    columnWidths: widths,
    width: { size: TOTAL, type: WidthType.DXA },
    rows: rows.map((cells, ri) => new TableRow({
      tableHeader: ri === 0,
      children: cells.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'EDEDED' } : undefined,
        children: [new Paragraph({
          children: inlineRuns(c, ri === 0 ? { bold: true } : {}),
          spacing: { line: 240, before: 40, after: 40 },
        })],
      })),
    })),
  });
}

/** Markdown -> массив элементов docx. skipH1 — не выводить первый заголовок. */
function mdToDocx(md, opts = {}) {
  const lines = md.replace(/\r/g, '').split('\n');
  const out = [];
  let i = 0, firstH1 = true;
  while (i < lines.length) {
    let l = lines[i];
    if (/^```/.test(l)) {
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) buf.push(lines[i++]);
      i++;
      out.push(...codeBlock(buf));
      continue;
    }
    if (/^\s*$/.test(l)) { i++; continue; }
    const h = /^(#{1,6})\s+(.*)$/.exec(l);
    if (h) {
      i++;
      if (h[1].length === 1 && firstH1) { firstH1 = false; if (opts.skipH1) continue; }
      const lvl = h[1].length === 1 ? HeadingLevel.HEADING_1
                : h[1].length === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3;
      out.push(new Paragraph({ children: inlineRuns(h[2], { bold: true, size: h[1].length === 1 ? 28 : 26 }),
        heading: lvl, spacing: { before: 240, after: 120 }, alignment: AlignmentType.LEFT }));
      continue;
    }
    if (/^\s*\|/.test(l)) {
      const rows = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) {
        const cells = lines[i].trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(s => s.trim());
        if (!cells.every(c => /^:?-{2,}:?$/.test(c))) rows.push(cells);
        i++;
      }
      const n = Math.max(...rows.map(r => r.length));
      rows.forEach(r => { while (r.length < n) r.push(''); });
      out.push(mkTable(rows));
      out.push(new Paragraph({ text: '', spacing: { after: 120 } }));
      continue;
    }
    if (/^\s*[-*]\s+/.test(l)) {
      while (i < lines.length && (/^\s*[-*]\s+/.test(lines[i]) || (/^\s{2,}\S/.test(lines[i]) && out.length))) {
        let item = lines[i].replace(/^\s*[-*]\s+/, '');
        i++;
        while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*[-*]\s+/.test(lines[i])) {
          item += ' ' + lines[i].trim(); i++;
        }
        out.push(new Paragraph({ children: inlineRuns(item), bullet: { level: 0 },
          spacing: { line: 300, after: 60 }, alignment: AlignmentType.JUSTIFIED }));
      }
      continue;
    }
    if (/^\s*>/.test(l)) {
      const buf = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) { buf.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
      out.push(new Paragraph({ children: inlineRuns(buf.join(' ').trim(), { italics: true }),
        spacing: SPACING, indent: { left: 567 }, alignment: AlignmentType.JUSTIFIED }));
      continue;
    }
    // обычный абзац (склеиваем до пустой строки); «1)» начинает новый пункт
    const NUM = /^\s*\d+[).]\s+/;
    const buf = [l]; i++;
    while (i < lines.length && !/^\s*$/.test(lines[i])
           && !/^(#{1,6}\s|```|\s*\||\s*[-*]\s|\s*>)/.test(lines[i]) && !NUM.test(lines[i])) {
      buf.push(lines[i]); i++;
    }
    out.push(para(buf.join(' ').replace(/\s+/g, ' ').trim()));
  }
  return out;
}

module.exports = { mdToDocx, para, inlineRuns, codeBlock, mkTable, FONT, SZ, SPACING };
