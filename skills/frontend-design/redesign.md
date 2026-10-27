# Redesign protocol and audit

Read before intentional visual redesign; small maintenance fixes follow the current approved design. Apply [SKILL.md](./SKILL.md) intake before choosing a new direction.

## 8.A Establish the scope
Ask one short style question only if the redesign direction is genuinely unclear; otherwise propose and state the direction. When relevant, offer the current brand as a proposed default and clarify preserve/evolve versus visual overhaul in the same conversation. Do not ask again merely because a design document already exists.

A request for polish does not automatically authorize a new identity, animation system, page architecture, or technology migration. A requested overhaul can change the visual language while preserving important product behavior and content.

## 8.B Inspect before editing
Scale the audit to the request. For a substantial redesign, inspect the actual rendered page and relevant code, then note:

- Working user flows, navigation, primary actions, content hierarchy, and recognizable brand details.
- Stack, package versions, styling/token pipeline, reusable components, assets, and font loading.
- Existing colors, typography, spacing, density, radius, elevation, theme scope, and motion.
- Demonstrated weaknesses: readability, spacing, alignment, clipping, overflow, inaccessible controls, misleading data, irrelevant assets, slow interactions, or broken states.
- URLs, metadata, anchor IDs, form contracts, analytics identifiers, and other integration surfaces affected by the proposed work.

Record useful existing tokens in `DESIGN.md` for a system-level change; do not delay a tiny bug fix to create a new spec. Reference current strengths as well as defects so a redesign does not erase the product's identity.

## 8.C Preserve what carries meaning
Keep working routes, content, data contracts, submitted values, keyboard behavior, and essential workflows unless the requested scope includes changing them. Respect real brand assets and copy voice. A user-authorized identity or navigation change is allowed; do not invent a separate approval gate for routine refinements already requested.

Call out a material scope change before doing work the user has not authorized, such as removing content, changing a production URL, rewriting legal terms, or migrating frameworks. This is a scope boundary, not a ban on necessary redesign work.

## 8.D Improve according to evidence
Choose the highest-value correction from the audit: composition, type, content, color, spacing, states, media, or interaction. There is no mandatory fix order. For a coherent existing product, a focused typography/spacing pass can be enough. A broken information hierarchy may need recomposition first.

Do not increase variance, motion, density, accent saturation, or image count merely because the work is called a redesign. Keep, reduce, or increase them only to serve the agreed direction. Do not add scroll reveals or an animation library as a proof of effort.

## 8.E Implement and verify
Reuse project components and existing stack. Make related changes together, then inspect the rendered result against the approved direction and the baseline. Check representative narrow and wide layouts and affected states, plus relevant project build/type/lint checks. Recheck corrected defects; expand validation when a new issue or integration risk warrants it.

A code grep is a lead, not a defect by itself: `h-screen`, inline styles, sharp corners, shadows, a serif, or a repeated card layout can be intentional. Determine the actual impact before changing it.

## 8.F Report the result
Describe what improved and the evidence used. Identify any missing real assets, inaccessible reference, unavailable preview, failing baseline check, or untested behavior specifically. Do not claim a full functional or accessibility pass from a static audit. Stop when the agreed scope is satisfied; do not expand a polish task into an unrelated rebuild.
