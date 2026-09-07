const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, AlignmentType, PageBreak, ImageRun,
        HeadingLevel, LevelFormat, convertMillimetersToTwip, PageOrientation } = require('docx');
const { mdToDocx, para, FONT, SZ } = require('./md');
const LABS = require('./labs');

const SRC = process.argv[2] || '/home/claude/src';
const SHOTS = process.argv[3] || '/home/claude/shots';
const OUT = process.argv[4] || '/home/claude/out';
fs.mkdirSync(OUT, { recursive: true });
const listings = JSON.parse(fs.readFileSync(path.join(SRC, 'listings.json'), 'utf8'));

const DISCIPLINE = 'Технология разработки прикладных решений для системы «1С:Предприятие»';

function pngSize(buf) {
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}
const STUDENT = 'Сидоров Д.С., группа ИТС-123';
const TEACHER = 'ст. пр. Козлов А.М.';
const YEAR = '2026';

function c(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun(Object.assign({ text, font: FONT, size: SZ }, opts))],
    alignment: AlignmentType.CENTER, spacing: { line: 276, after: opts.after || 0 },
  });
}
function r(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun(Object.assign({ text, font: FONT, size: SZ }, opts))],
    alignment: AlignmentType.RIGHT, spacing: { line: 276, after: opts.after || 0 },
  });
}
const empty = (n = 1) => Array.from({ length: n }, () => c(''));

function titlePage(lab) {
  return [
    c('МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ'),
    c('РОССИЙСКОЙ ФЕДЕРАЦИИ', { after: 200 }),
    c('Федеральное государственное бюджетное образовательное учреждение', { bold: true }),
    c('высшего образования', { bold: true }),
    c('«Российский государственный университет им. А.Н. Косыгина', { bold: true }),
    c('(Технологии. Дизайн. Искусство)»', { bold: true, after: 200 }),
    c('Институт информационных технологий и цифровой трансформации'),
    ...empty(6),
    c(`Отчет по лабораторной работе № ${lab.n}`, { bold: true, size: 30, after: 160 }),
    c(`по дисциплине «${DISCIPLINE}»`.replace('»»', '»'), { bold: true, after: 160 }),
    c(`Тема: «${lab.tema}»`, { bold: true }),
    ...empty(6),
    r(`Выполнил: ${STUDENT}`),
    r(`Проверил: ${TEACHER}`),
    ...empty(4),
    c(`Москва, ${YEAR} г.`),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

function h(text, level = HeadingLevel.HEADING_1, size = 28) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size, bold: true })],
    heading: level, spacing: { before: 240, after: 160 },
  });
}

function imageBlock(file, caption, idx) {
  const buf = fs.readFileSync(file);
  const { w: pw, h: ph } = pngSize(buf);
  // вписываем в ширину текста 170 мм, но не выше 190 мм
  let wmm = 170, hmm = wmm * ph / pw;
  if (hmm > 190) { hmm = 190; wmm = hmm * pw / ph; }
  hmm = Math.round(hmm); wmm = Math.round(wmm);
  return [
    new Paragraph({
      children: [new ImageRun({ data: buf, type: 'png',
        transformation: { width: Math.round(wmm * 3.78), height: Math.round(hmm * 3.78) } })],
      alignment: AlignmentType.CENTER, spacing: { before: 160, after: 80 },
    }),
    new Paragraph({
      children: [new TextRun({ text: `Рисунок ${idx} — ${caption}`, font: FONT, size: SZ - 2, italics: true })],
      alignment: AlignmentType.CENTER, spacing: { after: 200 },
    }),
  ];
}

function codeListing(title, code, idx) {
  const lines = code.replace(/\r/g, '').replace(/\t/g, '    ').split('\n');
  const out = [new Paragraph({
    children: [new TextRun({ text: `Листинг ${idx} — ${title}`, font: FONT, size: SZ - 2, italics: true })],
    spacing: { before: 200, after: 80 },
  })];
  lines.forEach(l => out.push(new Paragraph({
    children: [new TextRun({ text: l || ' ', font: 'Consolas', size: 18 })],
    spacing: { line: 220, after: 0 },
  })));
  out.push(new Paragraph({ text: '', spacing: { after: 160 } }));
  return out;
}

function buildLab(lab) {
  const key = 'lab' + lab.n;
  const zadanie = fs.readFileSync(path.join(SRC, key + '.zadanie.md'), 'utf8');
  const readme = fs.readFileSync(path.join(SRC, key + '.readme.md'), 'utf8');
  const kids = [...titlePage(lab)];

  kids.push(h('1. Задание'));
  kids.push(...mdToDocx(zadanie, { skipH1: true }));

  kids.push(h('2. Ход работы'));
  kids.push(...mdToDocx(readme, { skipH1: true }));

  const shots = lab.shots.filter(s => fs.existsSync(path.join(SHOTS, s[0])));
  if (shots.length) {
    kids.push(h('3. Результат работы конфигурации'));
    shots.forEach((s, i) => kids.push(...imageBlock(path.join(SHOTS, s[0]), s[1], i + 1)));
  }

  const lst = listings[key] || [];
  if (lst.length) {
    kids.push(h(`${shots.length ? 4 : 3}. Листинги`));
    lst.forEach(([t, code], i) => kids.push(...codeListing(t, code, i + 1)));
  }

  kids.push(h(`${(shots.length ? 1 : 0) + (lst.length ? 1 : 0) + 3}. Вывод`));
  kids.push(para(lab.vyvod));

  const doc = new Document({
    creator: 'Сидоров Д.С.',
    title: `Отчет по лабораторной работе № ${lab.n}`,
    numbering: { config: [] },
    styles: {
      default: {
        document: { run: { font: FONT, size: SZ } },
        heading1: { run: { font: FONT, size: 28, bold: true, color: '000000' } },
        heading2: { run: { font: FONT, size: 26, bold: true, color: '000000' } },
        heading3: { run: { font: FONT, size: 24, bold: true, color: '000000' } },
      },
    },
    sections: [{
      properties: {
        page: {
          size: { orientation: PageOrientation.PORTRAIT },
          margin: {
            top: convertMillimetersToTwip(20), bottom: convertMillimetersToTwip(20),
            left: convertMillimetersToTwip(25), right: convertMillimetersToTwip(15),
          },
        },
      },
      children: kids,
    }],
  });
  return doc;
}

(async () => {
  for (const lab of LABS) {
    const doc = buildLab(lab);
    const buf = await Packer.toBuffer(doc);
    const dir = path.join(OUT, 'lab' + lab.n);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'отчёт.docx'), buf);
    console.log('lab' + lab.n, buf.length);
  }
})();
