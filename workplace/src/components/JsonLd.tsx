import React from "react";

export interface JsonLdProps {
  type: "Organization" | "SoftwareApplication" | "FAQPage";
  data?: Record<string, any>;
}

export const JsonLd: React.FC<JsonLdProps> = ({ type, data }) => {
  let schema: Record<string, any> = {};

  if (type === "Organization") {
    schema = {
      "@context": "https://schema.org",
      "@type": "Organization",
      name: "Neutron Binary",
      url: "https://percipience.neutronbinary.com",
      logo: "https://percipience.neutronbinary.com/logo.png",
      description:
        "Creator of Percipience, the Enterprise Context Engineering OS and Autonomous CI/CD Gatekeeper.",
      sameAs: [
        "https://github.com/neutronbinary",
        "https://twitter.com/neutronbinary",
        "https://linkedin.com/company/neutronbinary",
      ],
      ...data,
    };
  } else if (type === "SoftwareApplication") {
    schema = {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      name: "Percipience Context Engineering OS",
      operatingSystem: "Linux, macOS, Cloud Native (Kubernetes, AWS, GCP)",
      applicationCategory: "DeveloperApplication, DevOpsApplication, FinOpsApplication",
      offers: {
        "@type": "AggregateOffer",
        priceCurrency: "USD",
        lowPrice: "1499",
        highPrice: "9999",
        offerCount: "3",
      },
      description:
        "Autonomous context optimization, AST token pruning, cryptographic Merkle state ledger, and CI/CD verification gatekeeper for AI software engineering.",
      featureList: [
        "AST Token Pruning (47.4% average reduction)",
        "Cryptographic Merkle State Ledger",
        "Sub-1.2s Surgical Context Rollback",
        "Sealed Binary Enclaves (.nbpack)",
        "Ephemeral Git Worktrees Concurrency",
        "Autonomous Living Documentation Sync",
      ],
      ...data,
    };
  } else if (type === "FAQPage") {
    schema = {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: [
        {
          "@type": "Question",
          name: "How does Percipience achieve 47.4% LLM token savings?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Percipience parses TypeScript, Python, and Go codebases into Abstract Syntax Trees (ASTs) before prompt composition. It strips non-semantic tokens (comments, type definitions when not needed, unreferenced imports) and computes structural diffs, significantly reducing input context payload size.",
          },
        },
        {
          "@type": "Question",
          name: "What is the 15% revenue-share FinOps model?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Percipience tracks exact token reductions via a cryptographic token ledger. Customers pay a baseline platform fee plus 15% of the verified net financial savings generated on their model inference bills, ensuring risk-free positive ROI.",
          },
        },
        {
          "@type": "Question",
          name: "How does surgical rollback intercept context poisoning?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Percipience monitors AST diffs and test assertions on every turn. If an agent hallucinates invalid signatures or corrupts state, the PoisoningSentinel rewinds only the contaminated module to its previous recovery point checkpoint in under 1.2 seconds, without disrupting sibling agents.",
          },
        },
      ],
      ...data,
    };
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
};
