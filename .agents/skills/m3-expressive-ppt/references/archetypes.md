# Material 3 Expressive Archetypes Reference

This document provides slot specifications and visual layout descriptions for the 8 core slide archetypes.

---

### 1. `cover_hero` (Keynote Cover & Hero)
- **Visual Composition**:
  - Left column: Category pill, Large Display Title (Google Sans + YaHei), Subtitle description, Bottom metadata pills (Speaker, Date, Organization) with auto line wrapping.
  - Right column: 28dp elevated Bento Hero card with 12-lobed organic Scallop badge, central spark icon, hero tag, and "Official Edition" pill badge.
- **Slots**:
  - `category`: str (e.g. "PRODUCT ARCHITECTURE 2026")
  - `title`: str (multiline with `\n`)
  - `subtitle`: str
  - `speaker`: str
  - `date`: str
  - `org`: str
  - `hero_highlight`: str
  - `hero_badge_text`: str

---

### 2. `bento_grid` (Bento Modular Dashboard)
- **Visual Composition**:
  - Left column (Hero Card): Elevated container with spark icon, title, description, and white hero metric container with trend pill.
  - Right top card: Grid icon, title, description, and 3 horizontal pill chips.
  - Right bottom-left card: Vibrant Tertiary Container card, 12-lobed scallop badge with lightning icon, headline metric stat, title, and description.
  - Right bottom-right card: Elevated card with verified icon, title, and clean bullet points.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `hero_card`: `{chip, icon, title, subtitle, desc, metric_val, metric_label, trend}`
  - `card_top`: `{icon, title, desc, chips: [...]}`
  - `card_bot_left`: `{icon, stat, title, desc}`
  - `card_bot_right`: `{icon, title, bullets: [...]}`

---

### 3. `process_roadmap` (Timeline & Milestones)
- **Visual Composition**:
  - 4 horizontal phase cards side-by-side with 28dp radius.
  - Active phase is highlighted with Tertiary Container fill (vibrant accent) while completed/upcoming use Surface Container / Outlined.
  - Phase number pill, phase title, timestamp, icon, deliverable bullet points, and bottom milestone KPI pill.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `phases`: list of 4 items `{phase_num, name, time, status: 'COMPLETED'|'ACTIVE'|'UPCOMING', icon, deliverables: [...], kpi_chip}`

---

### 4. `dual_contrast` (Dual-Chroma Comparison)
- **Visual Composition**:
  - Side-by-side comparison: Left card (Surface container, baseline/traditional), Right card (Primary container, recommended/modern).
  - Floating "VS" badge centered between both cards, rendered with highest z-order.
  - Each card includes category pill, headline title, description, bullet checklist, and bottom hero metric container.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `left_plan`: `{chip, title, desc, points: [...], metric_val, metric_label, trend}`
  - `right_plan`: `{chip, title, desc, points: [...], metric_val, metric_label, trend}`

---

### 5. `kpi_metrics` (Quantitative KPI Wall)
- **Visual Composition**:
  - 4 side-by-side vertical metric cards.
  - Giant Display-sized quantitative numbers (40pt bold), vector metric icon, metric label, trend pill (+XX%), and description.
  - Highlighted card uses Primary Container fill.
  - Bottom wide takeaway banner with lightbulb icon and summary conclusion.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `metrics`: list of 4 items `{value, label, trend, icon, desc, highlight: bool}`
  - `takeaway_badge`: str
  - `takeaway_text`: str

---

### 6. `feature_list` (Three Pillars Matrix)
- **Visual Composition**:
  - 3 side-by-side vertical pillar cards.
  - Pillar number tag pill, vector badge, Display title, English subtitle, description, bullet points, and bottom status badge.
  - Highlighted pillar (typically Pillar 02) uses Primary Container fill.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `features`: list of 3 items `{tag, icon, title, subtitle, desc, points: [...], badge, highlight: bool}`

---

### 7. `quote_takeaway` (Executive Quote & Principles)
- **Visual Composition**:
  - Top wide hero quote card with 12-lobed scallop quotation mark, large bold quote statement, and author pill badge.
  - Bottom 3 side-by-side takeaway cards with icons, titles, and descriptions.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `quote_text`: str
  - `quote_author`: str
  - `quote_role`: str
  - `pillars`: list of 3 items `{icon, title, desc}`

---

### 8. `team_showcase` (Talent & Organization)
- **Visual Composition**:
  - 3 side-by-side profile cards.
  - Scallop avatar badge with role icon, person name, role pill, bio description, and bottom row of dynamic skill tag chips.
- **Slots**:
  - `category`, `title`, `subtitle`
  - `members`: list of 3 items `{name, role, icon, desc, tags: [...]}`
