# Editable documents — DOCX (and when not to)

Read when the recipient must **open the file and change it**. If they only need to read, print or
file it, produce a PDF instead ([pdf.md](./pdf.md)) — a Word document sent as a final deliverable
will be reformatted by whatever version of Word opens it.

## When DOCX is the right answer

- A government or institutional submission whose template is a Word file and must stay one.
- A contract, memo, or letter the recipient will edit, comment on, or track changes in.
- A document that enters someone else's workflow where Word is the tool — HR, legal, records.

Everything else is a PDF. "Send them the Word file so they can print it" is a PDF.

## Fill a template — never build from scratch

Generating a complex document element by element is slow to write, impossible to restyle, and
produces files that look subtly wrong. Instead: take the real `.docx`, put placeholders in it, and
fill them.

- **Node** — `docxtemplater`: placeholders are `{name}`, `{#items}…{/items}` for loops.
- **Python** — `docxtpl` (Jinja syntax inside the document) over raw `python-docx` for templates;
  `python-docx` when you must construct structure.
- **PHP** — `PHPWord`'s `TemplateProcessor`: `setValue`, `cloneRow` for tables.

The template is maintained by whoever owns the document's design — usually not you — in Word. Keep
it in the repo, versioned, and treat a template change like a code change.

```php
// PHPWord — fill a template, clone a table row per item
$tpl = new \PhpOffice\PhpWord\TemplateProcessor(storage_path('templates/coe.docx'));
$tpl->setValue('employee_name', htmlspecialchars($employee->full_name, ENT_XML1));
$tpl->setValue('issued_on', now('Asia/Manila')->format('F j, Y'));
$tpl->cloneRow('item_desc', count($items));
foreach ($items as $i => $item) {
    $tpl->setValue('item_desc#'.($i+1), htmlspecialchars($item->description, ENT_XML1));
    $tpl->setValue('item_amount#'.($i+1), number_format($item->centavos / 100, 2));
}
$tpl->saveAs($path);
```

## The traps

1. **Escape every value.** A `&`, `<`, or `>` from user data corrupts the document XML and Word
   refuses to open the file — with a message that does not say why. Escape as XML, always.
2. **A placeholder Word split across runs never matches.** Typing `{name}` while autocorrect or
   spellcheck is active can store it as three separate runs, and the library will not find it. Type
   placeholders in one go, or paste as plain text, and test the template with real data before
   trusting it.
3. **Line breaks are not `\n`.** Use the library's break element, or the text runs together.
4. **Images need explicit dimensions** or they arrive at the wrong scale.
5. **Fonts follow the recipient's machine.** If the template uses a font they lack, Word substitutes
   and the layout shifts. Stick to fonts that are actually installed everywhere the document goes.
6. **DOCX → PDF is not free.** LibreOffice headless can convert, but it is a separate binary, a
   separate failure mode, and it re-flows the layout. If a PDF is the real deliverable, generate the
   PDF directly instead of converting.

## Done

- The file opens in Word without a repair prompt — tested with real data, including a value
  containing `&` and a name with `ñ`.
- Every placeholder is filled; none is left visible in the output.
- Tables with repeated rows were tested at 0, 1, and many items.
- The template lives in the repo and its origin is recorded, so the next change starts from the
  authority's current version.
