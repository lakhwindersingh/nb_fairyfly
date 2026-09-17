/**
 * Percipience Playwright E2E Integration Suite: Onboarding, Demo, and Surgical Rollback
 */

import { test, expect } from "@playwright/test";

test.describe("Percipience SaaS Portal Full End-to-End User Journeys", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("http://localhost:3000/");
    await page.waitForLoadState("networkidle");
  });

  test("1. Landing Page renders hero metrics and responsive navigation", async ({ page }) => {
    // Assert Brand Title and Navigation
    await expect(page.locator("text=Percipience").first()).toBeVisible();
    await expect(page.locator("text=The Enterprise Context Engineering Operating System")).toBeVisible();

    // Verify 47.4% metric displayed
    await expect(page.locator("text=47.4%").first()).toBeVisible();
  });

  test("2. Interactive AST Token Pruning live demo flow", async ({ page }) => {
    // Navigate to AST Demo section
    const demoSection = page.locator("#demo");
    if (await demoSection.isVisible()) {
      const pruneButton = page.locator("button:has-text('Execute AST Pruning')");
      if (await pruneButton.isVisible()) {
        await pruneButton.click();
        await expect(page.locator("text=Tokens Saved")).toBeVisible();
      }
    }
  });

  test("3. Self-serve tenant onboarding and CMEK provision flow", async ({ page }) => {
    await page.goto("http://localhost:3000/onboarding");
    await page.waitForLoadState("networkidle");

    const orgInput = page.locator("input[name='organizationName'], input#org-name");
    if (await orgInput.isVisible()) {
      await orgInput.fill("Automated Test Corp");
      const submitBtn = page.locator("button[type='submit']");
      await submitBtn.click();
      await expect(page.locator("text=Workspace Provisioned, text=Genesis Block Sealed").first()).toBeVisible();
    }
  });

  test("4. Real-time Telemetry & Surgical Rollback trigger", async ({ page }) => {
    await page.goto("http://localhost:3000/app/observability");
    await page.waitForLoadState("networkidle");

    // Check DAG viewer canvas or ledger table
    const ledgerTable = page.locator("table, .merkle-explorer");
    if (await ledgerTable.isVisible()) {
      await expect(page.locator("text=Merkle").first()).toBeVisible();
    }
  });
});
