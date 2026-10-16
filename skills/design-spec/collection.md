# Optional reference collection

Begin with the user's style and references from the shared design intake. Use this collection when they want suggestions or a particular pattern needs investigation. References are choices, not mandatory visual systems or package recommendations. Inspect the current source before claiming its present behavior; third-party design descriptions may be stale.

Borrow a named quality—task hierarchy, typography, density, crop, state feedback or motion—not a product's entire identity. An audience informs usability and content; it does not enforce one aesthetic. Cross-domain borrowing can be useful, such as editorial typography for a finance brand or a clear queue pattern for a school office.

## Interface and motion patterns

| Resource | Useful reason to inspect | Adoption boundary |
|---|---|---|
| [BrewedOps Motion Library](https://brewedops.cloud/motionlibrary/) | User-selected option for interface/motion inspiration, self-contained HTML examples and prompts; relevant categories include hero, dashboard, login, mobile, GSAP and 3D treatments | Select a relevant pattern, inspect source, adapt to approved direction; no automatic runtime/package or library vendoring |
| [GOV.UK Design System](https://design-system.service.gov.uk/) | Public-service task patterns, forms, content and error recovery | Check applicability; its brand identity and governance do not automatically apply to another country or organization |
| [U.S. Web Design System](https://designsystem.digital.gov/) | Accessible public-service component structure and guidance | Use an imposed standard only when the actual project requires it |
| [Material Design](https://m3.material.io/) | Cross-device component behavior, semantic color and motion relationships | A reference does not require installing a Material package |
| [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) | Native platform behavior and interaction conventions | Check actual target/version; do not copy iOS behavior indiscriminately to Android/web |
| [Microsoft Fluent](https://fluent2.microsoft.design/) | Product component states, adaptive layouts and typography relationships | Use relevant concepts or a deliberately chosen compatible implementation |
| [IBM Carbon](https://carbondesignsystem.com/) | Dense enterprise data, forms and component states | Preserve the user's brand and actual product scope |

These resources have their own terms and may change. Verify current documentation and package compatibility when implementation relies on them.

## Study by product need

- **Public services:** clear requirements, status, eligibility, cost, accessible forms and authoritative dated content. Consider relevant official service flows, without making every civic site monochrome.
- **Money and operations:** amount/fee clarity, confirmation, status, recovery, exact values and stable data density. Inspect products the user actually uses; a live financial interface must not be inferred from an old screenshot.
- **Commerce and retail:** product media, variants, price, availability, delivery and purchase flow. Local audience expectations may inform density, but do not fabricate urgency, ratings or inventory.
- **Content/editorial:** reading hierarchy, caption/credit relationships, long-form measure, navigation and imagery. Editorial qualities can work outside publishing.
- **Professional tools:** information hierarchy, useful defaults, keyboard workflow, tables, bulk actions and honest async states. Density should fit the frequency and task, not a “SaaS” stereotype.
- **Creative/campaign:** type character, art direction, rhythm, material, brand expression and motion. Preserve readability, navigation and performance while allowing rich visuals.
- **Native mobile:** system navigation, permission behavior, touch, scaling, safe areas and interruptions. Use current platform guidance plus brand references.

## Adopt a BrewedOps pattern deliberately

The [library license](https://brewedops.cloud/motionlibrary/legal/license/) should be consulted for the selected use. Do not reproduce or repackage its library as this kit's own component collection. Third-party libraries, fonts, images and marks carry their own terms; a code example's availability does not replace checking those actual assets. Sample identities, data and product claims are not factual content for the user's project.

Read selected source before adaptation. Check scripts and external network dependencies, reduced-motion/static behavior, semantic structure, keyboard/touch interaction, responsive sizing, lifecycle cleanup and cost. Do not run unreviewed external demo code as a required workflow. Recreate useful ideas in the supported project stack when appropriate; do not install GSAP/3D or use every effect just because the reference does.

Record the source link and quality borrowed in `DESIGN.md` when it will help maintainers. A URL added to the option list is not a new universal design preference, and does not trigger duplicate intake after the direction is already answered.
