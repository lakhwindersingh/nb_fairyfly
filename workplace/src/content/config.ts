import { z } from "zod";

export const CaseStudySchema = z.object({
  title: z.string(),
  description: z.string(),
  client: z.string(),
  industry: z.string(),
  publishDate: z.string(),
  author: z.string(),
  metrics: z.object({
    tokenSavingsPct: z.number(),
    monthlyDollarSavings: z.number(),
    rollbackLatencySec: z.number(),
    merkleBlocksValidated: z.number(),
  }),
  tags: z.array(z.string()),
  featured: z.boolean().default(false),
});

export const BlogPostSchema = z.object({
  title: z.string(),
  description: z.string(),
  publishDate: z.string(),
  author: z.string(),
  authorRole: z.string(),
  readTimeMinutes: z.number(),
  category: z.enum(["FinOps", "Architecture", "Security", "AI Engineering", "CI/CD"]),
  tags: z.array(z.string()),
  canonicalUrl: z.string().optional(),
});

export type CaseStudy = z.infer<typeof CaseStudySchema>;
export type BlogPost = z.infer<typeof BlogPostSchema>;
