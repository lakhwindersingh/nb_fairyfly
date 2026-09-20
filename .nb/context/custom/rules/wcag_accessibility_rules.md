# WCAG 2.1 AA Accessibility Rules

## 1. Visual & Contrast Rules
- **Normal Text Contrast**: Minimum contrast ratio of $4.5:1$ against the background.
- **Large Text Contrast (>= 18pt or 14pt bold)**: Minimum contrast ratio of $3.0:1$.
- **UI Components & Graphics**: Minimum contrast ratio of $3.0:1$ for borders, focus rings, and active states.

## 2. Keyboard & Screen Reader Accessibility
- **Full Keyboard Navigability**: Every interactive element (buttons, tabs, inputs, links) must be reachable and operable via <kbd>Tab</kbd>, <kbd>Enter</kbd>, and <kbd>Space</kbd>.
- **Visible Focus Rings**: Focus indicators must not be suppressed (`outline: none` without replacement is strictly forbidden).
- **ARIA Semantics**: All dynamic controls must specify appropriate ARIA roles (`role="tab"`, `aria-selected`, `aria-controls`, `aria-expanded`).
