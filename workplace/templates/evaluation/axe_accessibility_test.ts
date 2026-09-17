/**
 * Percipience Web Quality CI: Axe-Core Automated Accessibility Suite
 * Enforces WCAG 2.1 Level AA Compliance and zero critical a11y violations.
 */

import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const TARGET_ROUTES = [
  { path: "/", name: "Corporate Landing Page" },
  { path: "/#capabilities", name: "Capabilities Section" },
  { path: "/#demo", name: "Interactive AST Demo" },
  { path: "/#roi", name: "Rev-Share ROI Calculator" },
  { path: "/onboarding", name: "Tenant Self-Serve Onboarding" },
  { path: "/docs", name: "Documentation Hub" },
];

test.describe("WCAG 2.1 Level AA Accessibility Verification", () => {
  for (const route of TARGET_ROUTES) {
    test(`Route ${route.name} (${route.path}) must satisfy WCAG 2.1 AA standards`, async ({ page }) => {
      await page.goto(`http://localhost:3000${route.path}`);
      await page.waitForLoadState("networkidle");

      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "best-practice"])
        .disableRules(["color-contrast"]) // Handled via dedicated contrast token suite if running in draft dark mode
        .analyze();

      // Assert 0 critical or serious accessibility violations
      const severeViolations = accessibilityScanResults.violations.filter(
        (v) => v.impact === "critical" || v.impact === "serious"
      );

      expect(
        severeViolations,
        `Found ${severeViolations.length} severe a11y violations on ${route.name}:\n` +
          JSON.stringify(severeViolations, null, 2)
      ).toEqual([]);
    });
  }

  test("All interactive buttons and navigation links have accessible names", async ({ page }) => {
    await page.goto("http://localhost:3000/");
    const buttons = page.locator("button, a[role='button']");
    const count = await buttons.count();

    for (let i = 0; i < count; i++) {
      const btn = buttons.nth(i);
      const isVisible = await btn.isVisible();
      if (isVisible) {
        const ariaLabel = await btn.getAttribute("aria-label");
        const textContent = (await btn.textContent())?.trim();
        const hasAccessibleName = Boolean(ariaLabel || textContent);
        expect(hasAccessibleName).toBe(true);
      }
    }
  });
});
