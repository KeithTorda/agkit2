# Inspect the computed result

Use computed styles when the render differs from source intent. Inspect the actual element and relevant ancestors, including pseudo-elements when they create the visible treatment. A class name or authored value is not evidence of the winning declaration.

For layout inspect bounding rectangles, display, position, containing block, min/max width/height, grid/flex tracks, shrink/grow, overflow, box sizing and transforms. For visual treatment inspect resolved foreground/background, opacity, fonts and actual loaded face, line height, letter spacing, shadows and relevant media/pseudo-element layers.

Trace a mismatch to origin/importance, layer order, specificity, scope, source order, inheritance, a conditional query, generated utility or runtime style. Inspect animation ownership too: a script can overwrite an otherwise correct CSS transform.

Compare repeated components using their intended semantic role. A different computed pixel value may be a responsive, content-driven or optical choice; it is not automatically a token violation. A shared token resolving to the wrong value across many screens is a real ownership concern.

Measure contrast on actual backgrounds and states. A static scanner cannot fully resolve an image crop, backdrop filter, translucent stack, inherited theme or a moving gradient. Record uncertainty rather than treating an unresolved color as a pass.

Change the owner of the demonstrated problem and recheck the real render. Do not accumulate increasingly specific patches just to make a screenshot match once.
