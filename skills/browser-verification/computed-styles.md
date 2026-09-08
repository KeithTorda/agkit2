# Reading computed styles against the tokens

Read when checking token conformance on a project for the first time, or when you need the dump snippet. The protocol is in [SKILL.md](./SKILL.md) §4.

Do not eyeball this. Antigravity's JavaScript execution policy is on, so collect the real values
with `getComputedStyle` and compare them as data:

```js
// Dump computed values for the region you changed, then diff against DESIGN.md
[...document.querySelectorAll('main *')].slice(0, 80).map(el => {
  const s = getComputedStyle(el);
  return {
    el: el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''),
    color: s.color, bg: s.backgroundColor, size: s.fontSize,
    pad: s.padding, gap: s.gap, radius: s.borderRadius,
  };
});
```

Then reduce to the distinct values per property — a page using nine different font sizes or six
greys has a token problem regardless of how any single element looks.

```text
WRONG (what source review concludes)
  "className='text-slate-600 p-5' — looks consistent with the design."

RIGHT (what the render actually reports)
  Computed: color rgb(71,85,105) · padding 20px · font-size 15px
  DESIGN.md scale: text-secondary #5A6472 · spacing 16/24 · type 14/16/20
  → 3 token violations: color off-scale, 20px not on the spacing scale, 15px not on the type scale.
```

Off-scale values are how a design drifts into mush one component at a time. Catch them at the
render or they ship.
