/**
 * Percipience Unit Test Suite: Form Validation, Content Schema & Rev-Share Calculation
 */

import { describe, it, expect } from "vitest";
import { CaseStudySchema, BlogPostSchema } from "../../src/content/config";
import { constructSEOMetadata } from "../../src/lib/seo";
import { getDictionary } from "../../src/lib/i18n";
import { generateSitemapXml, generateRobotsTxt } from "../../src/lib/sitemap_generator";

describe("Content Collection Schema Validation", () => {
  it("should successfully validate valid case study metadata", () => {
    const rawCaseStudy = {
      title: "FinScale Dynamics Token Reduction",
      description: "48.2% token savings achieved via AST pruning",
      client: "FinScale Dynamics",
      industry: "FinTech",
      publishDate: "2026-09-15",
      author: "Percipience Team",
      metrics: {
        tokenSavingsPct: 48.2,
        monthlyDollarSavings: 42800,
        rollbackLatencySec: 1.14,
        merkleBlocksValidated: 480,
      },
      tags: ["FinOps", "AST Pruning"],
      featured: true,
    };

    const parsed = CaseStudySchema.parse(rawCaseStudy);
    expect(parsed.metrics.tokenSavingsPct).toBe(48.2);
    expect(parsed.featured).toBe(true);
  });

  it("should validate blog post metadata schema", () => {
    const rawPost = {
      title: "AST Pruning vs Statistical Prompt Compression",
      description: "Deterministic AST compression",
      publishDate: "2026-09-14",
      author: "Percipience Research Group",
      authorRole: "Core Platform Engineering",
      readTimeMinutes: 6,
      category: "AI Engineering",
      tags: ["AST", "Tree-Sitter"],
    };

    const parsed = BlogPostSchema.parse(rawPost);
    expect(parsed.category).toBe("AI Engineering");
    expect(parsed.readTimeMinutes).toBe(6);
  });
});

describe("SEO & i18n Dictionary Engine", () => {
  it("should generate standardized OpenGraph and Twitter metadata", () => {
    const seo = constructSEOMetadata({ title: "Custom Title" });
    expect(seo.title).toContain("Custom Title");
    expect(seo.openGraph?.type).toBe("website");
    expect(seo.twitter?.card).toBe("summary_large_image");
  });

  it("should provide localized strings for en, es, de", () => {
    const enDict = getDictionary("en");
    const esDict = getDictionary("es");
    const deDict = getDictionary("de");

    expect(enDict.nav.capabilities).toBe("Capabilities");
    expect(esDict.nav.capabilities).toBe("Capacidades");
    expect(deDict.nav.capabilities).toBe("Funktionen");
  });
});

describe("Sitemap & Robots Generator", () => {
  it("should generate valid XML sitemap with entries", () => {
    const sitemap = generateSitemapXml();
    expect(sitemap).toContain("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
    expect(sitemap).toContain("<loc>https://percipience.neutronbinary.com/</loc>");
  });

  it("should generate compliant robots.txt with disallow paths", () => {
    const robots = generateRobotsTxt();
    expect(robots).toContain("User-agent: *");
    expect(robots).toContain("Disallow: /api/");
    expect(robots).toContain("Sitemap: https://percipience.neutronbinary.com/sitemap.xml");
  });
});
