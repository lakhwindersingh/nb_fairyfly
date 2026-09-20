# Enterprise SaaS Portal Domain Architecture

> **Autonomously Maintained by**: `agent_enterprise_saas_portal_architect`  
> **Status**: ✅ Verified Valid Mermaid  
> **Canonical Target**: `workplace/modules/mod_portal_marketing/` & `workplace/portal/server.py`

## 1. System Topology & Component Layout

```mermaid
graph TD
  subgraph Frontend_Layer["Client & Web Portal Layer"]
    ReactApp["React / Next.js Marketing & Portal<br/>(mod_portal_marketing)"]
    AdminApp["Admin Console & Telemetry Hub<br/>(user/outputs/dashboard/index.html)"]
  end

  subgraph Gateway_Layer["API Gateway & FinOps Server"]
    Gateway["Python Gateway Daemon<br/>(workplace/portal/server.py)"]
    Auth["Session Auth & RBAC Guard<br/>(/api/auth/login, /api/auth/session)"]
    StripeWebhook["Stripe / Paddle Webhook Handler<br/>(billing_webhook_contract.json)"]
  end

  subgraph Enclave_Layer["Cryptographic Ledger & Storage"]
    MerkleLedger["Merkle State Chain<br/>(context_ledger.yaml)"]
    WORMEgress["Immutable WORM Storage<br/>(AWS S3 / GCP Object Lock)"]
  end

  ReactApp --> Gateway
  AdminApp --> Gateway
  Gateway --> Auth
  Gateway --> StripeWebhook
  Gateway --> MerkleLedger
  MerkleLedger --> WORMEgress
```
