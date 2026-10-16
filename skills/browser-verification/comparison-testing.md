# Compare generated outputs fairly

Use this workflow when a user requests a paired comparison, such as checking whether revised instructions improve a generated page. Ordinary design and repair work needs relevant browser verification, not a mandatory A/B test. Use available project tools; a comparison does not require a new framework, dependency, or approval step.

## Hold the comparison conditions steady

Record the question and the conditions before building: the same brief, data fixture and date anchor, model/settings, asset access, stack, scope, and required controls. Give each builder the same time or revision opportunity and an independent starting context. Record unavoidable differences instead of calling the conditions identical. If the operational metric definitions differ legitimately, check each against its visible definition and the shared data; do not force equal labels or values after the fact.

Distinguish an independent generation from refinement. A builder's permitted inspection and repairs before its first completed handoff belong to that generation and should be disclosed. A later fix or additional attempt is refinement or another generation. Do not compare one side's first output with the other side's selectively chosen best result without saying so.

Freeze completed sources before shared QA. Preserve snapshots or hashes, original captures, raw test output, review notes, and the mapping from neutral sample IDs to conditions. When cloning a baseline, retain its referenced local assets and runtime files; copying only HTML/CSS/JS can manufacture missing-resource defects. Check the renderable asset set against the original. Inspect artifacts after freeze without quietly changing one side. If an app repair is needed, keep the original result and identify the repaired revision separately.

## Collect separate kinds of evidence

Use the same browser, viewports, representative content states, and task contract for both samples. Capture the untouched initial render before interactions. Include an intermediate layout when navigation or content arrangement changes there, and inspect captures at actual display size.

Keep these observations distinct:

- **Rendered fit:** clipping, wrapping, page overflow, crop, alignment, and contained table scrolling.
- **Legibility and task usability:** supporting text, chart labels/metadata, status meaning, secondary actions, and the next useful action. Inspect whether navigation leaves enough working width and whether important table columns remain usable. For narrow tables, exercise access to the final columns and assess whether additional content is discoverable from the initial view.
- **Functional behavior:** controls, filtering, sorting, empty recovery, exports, dialogs, navigation, focus, and other agreed flows. Test observed outcomes against the fixture. Functional passes do not award visual points.

For visual judgment, use neutral sample IDs and the same brief and rubric. When practical, have a reviewer assess the captures without kit identities, builder notes, source code, or functional results, then disclose the mapping afterward. Record who or what reviewed and what evidence they saw. A model review is a judgment under that rubric, not an objective design measurement. Keep independent functional results alongside the review instead of letting one score stand for both.

## Diagnose the test before blaming the output

Independent cases should navigate the saved original clean URL or use an appropriately isolated context. Reloading a URL that the app updates with active filters can leak state between cases. Verify the intended starting state.

Scope table checks to the semantic task region and target table or `tbody`; confirm its headers or row identity before measuring or interacting. A visually hidden accessible chart-data table may precede the visible orders table. Checking the first table can produce plausible but irrelevant results for geometry, coverage, and last-column reachability.

Preserve the original failure artifacts. Locate the cause in the app, harness, or environment and fix only the responsible layer. Confirm expected local-server favicon diagnostics separately from genuine application request failures. If a harness correction changes isolation or locator scope, rerun both samples with the same corrected checks and retain the initial results with an explanation. Do not count demonstrated harness errors as app defects or erase unfavorable product findings.

## Report the observed result and its limits

Publish the conditions, source versions, permitted refinement, rubric, actual viewports/states, independent functional results, defects, and unverified areas. Keep unfavorable findings even when they contradict the expected improvement. Choose any scoring scale for the stated question; do not turn a sample score into a universal target for fonts, widths, or aesthetics.

One brief and one completed generation per condition support a finding about that observed pair. They do not establish statistical causality, broad design superiority, or live-runtime behavior when only instruction snapshots were applied elsewhere. Identify subjective review, missing cross-browser or assistive-technology testing, and any other material limits. Additional runs are useful only when the comparison question warrants them.
