---
name: Jurisprudence Precision
colors:
  surface: '#f6faff'
  surface-dim: '#cddcea'
  surface-bright: '#f6faff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#ebf5ff'
  surface-container: '#e1f0fe'
  surface-container-high: '#dbeaf8'
  surface-container-highest: '#d6e4f2'
  on-surface: '#0f1d27'
  on-surface-variant: '#3e4946'
  inverse-surface: '#24323c'
  inverse-on-surface: '#e5f2ff'
  outline: '#6e7976'
  outline-variant: '#bdc9c5'
  surface-tint: '#006b5e'
  primary: '#005f54'
  on-primary: '#ffffff'
  primary-container: '#0f7a6c'
  on-primary-container: '#abffee'
  inverse-primary: '#7dd6c6'
  secondary: '#26695e'
  on-secondary: '#ffffff'
  secondary-container: '#abecdf'
  on-secondary-container: '#2c6d62'
  tertiary: '#893f0d'
  on-tertiary: '#ffffff'
  tertiary-container: '#a85624'
  on-tertiary-container: '#ffebe3'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#99f3e1'
  primary-fixed-dim: '#7dd6c6'
  on-primary-fixed: '#00201b'
  on-primary-fixed-variant: '#005046'
  secondary-fixed: '#aeefe1'
  secondary-fixed-dim: '#92d3c6'
  on-secondary-fixed: '#00201b'
  on-secondary-fixed-variant: '#015046'
  tertiary-fixed: '#ffdbca'
  tertiary-fixed-dim: '#ffb690'
  on-tertiary-fixed: '#341100'
  on-tertiary-fixed-variant: '#783200'
  background: '#f6faff'
  on-background: '#0f1d27'
  surface-variant: '#d6e4f2'
typography:
  display-lg:
    fontFamily: Merriweather
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Merriweather
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Merriweather
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Merriweather
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 30px
    letterSpacing: 0em
  headline-sm:
    fontFamily: Merriweather
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 26px
    letterSpacing: 0em
  body-lg:
    fontFamily: Source Sans 3
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: 0em
  body-md:
    fontFamily: Source Sans 3
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Source Sans 3
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Source Sans 3
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Source Sans 3
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  citation-code:
    fontFamily: Source Sans 3
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.25rem
  margin: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system embodies the gravitas, rigor, and clarity expected of enterprise legal operations. Designed for corporate general counsels, compliance directors, and legal analysts interacting with high-stakes generative intelligence, the interface delivers institutional authority without clinical sterility. 

The aesthetic marries classical editorial legal typography with clean, contemporary functionalism. Instead of playful tech tropes, neon gradients, or consumer AI flourishes, the product utilizes structural clarity, deliberate quietude, and rigorous information hierarchies. The visual atmosphere evokes the feeling of reviewing an authoritative legal brief printed on premium parchment paper, updated dynamically through precise computational precision.

Key emotional attributes:
- **Judicial Authority:** Grounded, unshakeable, reliable, and strictly audit-ready.
- **Intellectual Clarity:** Highly legible across dense statutes, clause comparisons, and source citations.
- **Sober Transparency:** Visible lineage, unambiguous attribution, and deliberate communication of system boundaries and domain refusals.

## Colors

The palette draws inspiration from traditional legal chambers, archival ink, and clean architectural drafting surfaces.

### Functional Roles
- **Primary (`#0F7A6C` / Accent Teal):** Dedicated to primary action vectors, verified semantic links, highlighted search matches, active navigation markers, and verified citations.
- **Primary Deep (`#0A554B` / Accent Deep):** Used for primary button hover/pressed states, dense data table primary headers, and deep visual anchors.
- **Base Surfaces:**
  - **Paper (`#EEF3F1`):** The ambient root canvas color, delivering a cool, soft sage undertone that eliminates harsh glare during prolonged document review sessions.
  - **Panel (`#F7FAF8`):** The primary card, drawer, and table background, providing subtle layer separation against the canvas.
- **Typography & Structure:**
  - **Ink (`#13212B`):** Deep iron-gall black for primary titles, body text, and structural icons requiring total contrast.
  - **Ink Soft (`#2A3D4A`):** Secondary structural copy, metadata, timestamps, table headers, and inactive navigational items.
  - **Line (`#C5D4CC`):** Crisp 1px borders, subtle cell dividers, and structural bounding boxes.
- **Semantic Feedback:**
  - **Warning / Out-of-Domain (`#9A4B1A`):** Muted earthen amber for confidence warnings, domain bounds warnings, and out-of-scope refusals.
  - **Danger / Critical Error (`#8B2E2E`):** Restrained terracotta red for missing statutory references, revoked certificates, or invalid legal instruments.

## Typography

Typography establishes an immediate dual-cadence: Merriweather confers academic authority to strategic synthesis, section summaries, and statutory clause headers, while Source Sans 3 provides high legibility across long-form legal paragraphs, audit logs, and multidimensional data matrices.

- **Headlines & Document Titles:** Set in Merriweather with tight tracking and calibrated leading to avoid visual collision between complex legal phrasing and clause numbering.
- **Analytical & Body Text:** Rendered in Source Sans 3 at regular weights. Line heights remain generous (1.5x - 1.6x) to preserve scanning endurance across multi-page contract audits.
- **Citations & Meta Labels:** Compact, semi-bold sans-serif styling in uppercase or high-contrast small caps ensures that statutory references (e.g., `DOC-REF 492/QD-BTC`) stand out from surrounding narrative prose.

## Layout & Spacing

The layout operates on a 12-column structural grid system built for dual-pane and three-pane operational workflows typical of RAG interfaces:
1. **Left Rail (Persistent, 260px - 300px):** Workspace selection, domain knowledge bases, and index health.
2. **Center Stage (Fluid, Min 640px):** The inquiry timeline, synthesis outputs, and cross-examination workspace.
3. **Right Inspector (Collapsible, 360px - 440px):** Direct citation lineage, PDF source viewer, clause comparison, and audit metadata.

### Breakpoints & Adaptive Logic
- **Desktop (1440px+):** Full 3-pane layout active concurrently. Canvas margins sit at `2.5rem` (`space-xl`), gutters at `1.25rem`.
- **Laptop / Small Desktop (1024px – 1439px):** Inspector pane shifts to a floating slide-over drawer anchored to the right border.
- **Tablet (768px – 1023px):** Workspace rail collapses into an icon bar or overlay menu; center stage expands to fill safe width.
- **Mobile (< 768px):** Single-column stack. Content prioritized strictly: Query Input > Summary Synthesis > Sticky Citation Drawer Trigger.

## Elevation & Depth

Visual hierarchy is primarily communicated through tonal layering and razor-sharp border definition, strictly avoiding exaggerated shadows or artificial blurs.

- **Level 0 (Canvas):** Pure `#EEF3F1` (`Paper`). Completely flat.
- **Level 1 (Cards, Data Panels, Form Modules):** `#F7FAF8` (`Panel`) framed with a continuous 1px `#C5D4CC` (`Line`) border. Shadow is subtle and diffuse: `0 1px 3px rgba(19, 33, 43, 0.04)`.
- **Level 2 (Popovers, Citations, Flyouts):** `#F7FAF8` surface, 1px `#C5D4CC` border, backed with directional depth: `0 4px 16px rgba(19, 33, 43, 0.08)`.
- **Level 3 (Modal Dialogues, Redline Overlays):** `#FFFFFF` surface with strict 1px `#13212B` (15% opacity) border and grounded drop elevation: `0 12px 32px rgba(19, 33, 43, 0.14)`.

## Shapes

The interface balances modern ergonomics with institutional structure by adhering to a consistent 10px - 12px corner radius (`roundedness: 2`).

- **Inputs, Buttons, and Standard Cards:** Fixed at `10px` (`0.625rem`) to maintain architectural precision without severe sharpness.
- **Containers, Modals, and Inspection Panels:** Scaled to `12px` (`0.75rem`) to soften structural boundaries against the parchment canvas.
- **Badges, Legal Citations, and Filter Chips:** Set to `6px` (`0.375rem`) to prevent round pill shapes, anchoring them as micro-documents rather than casual consumer tags.

## Components

### Buttons
- **Primary:** Filled `#0F7A6C` background with `#F7FAF8` text. Hover shifts to `#0A554B`. 10px radius, 0 1px 2px rgba(0,0,0,0.06).
- **Secondary / Outlined:** `#F7FAF8` background, 1px `#C5D4CC` border, `#13212B` text. Hover induces `#EEF3F1` surface fill and `#0F7A6C` border.
- **Danger:** Subtle `#8B2E2E` 1px border on transparent or `#F7FAF8` surface, with `#8B2E2E` text for confirmation actions.

### Citations & Source Badges (RAG Specific)
- **Inline Citation Marker:** Styled as superscript or bracketed micro-chips (e.g., `[Luật DN 2020 §4]`). `#EEF3F1` background, 1px `#0F7A6C` (40% opacity) border, `#0F7A6C` bold typography. Hover highlights the correlated source text in the document viewer.
- **Citation Card:** Displayed within the Right Inspector. Houses the exact passage excerpt, confidence coefficient, and statutory reference link. Bordered with a 2px left accent bar in `#0F7A6C`.

### Knowledge Base & Domain Indicators
- **Scope Indicator:** Pill-free rectangular micro-panels specifying the active corpus (e.g., `CORPUS: THUẾ & TÀI CHÍNH 2024`). Text in `#2A3D4A` with a leading 6px circle indicator (solid `#0F7A6C` for synced, amber for reindexing).

### Refusal & Out-of-Domain States
- **Domain Refusal Alert:** Rendered within a `#F7FAF8` container with a distinct 3px left border in `#9A4B1A` (`Warn`). The text clearly states query divergence from current jurisdictional corpora without apologetic or anthropomorphic phrasing, followed by suggested permissible queries within scope.

### Form Inputs & Search Command
- **Legal Prompt Bar:** Elevated card-style text input on `#FFFFFF` or `#F7FAF8` with 1px `#C5D4CC` border. Focus state transforms the border to 1.5px `#0F7A6C` with zero chromatic glow.
- **Checkboxes & Radios:** Sharp-cornered (3px for checkboxes, circular for radios) utilizing `#0F7A6C` fill upon selection with high-contrast `#FFFFFF` check vectors.

### Tables & Legal Grids
- **Header Cells:** `#EEF3F1` surface background, 1px bottom border in `#C5D4CC`, uppercase labels in `#2A3D4A` font weight 600.
- **Row Styling:** Alternating rows strictly avoid loud banding; separation is achieved via clean 1px hairline horizontal rules in `#C5D4CC`.