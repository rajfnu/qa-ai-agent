# Sales Coach in Pocket – ImpactWon
_Agentic AI Platform for Right-to-Win Sales Coaching_


> Audience: AI Engineers and Data Scientists  
> Scope: End-to-end blueprint (agents, workflows, components, data, scoring, cost controls, delivery)

---

## 1. Vision
Digitize ImpactWon’s proprietary **4Cs (Credibility, Capability, Commitment, Control)** framework and **Right-to-Win (R2W)** methodology into a **multi-agent AI platform** that coaches sellers, scores deals, and enables executives to lead CEO-led sales effectively.

The system acts as a **“Coach in Your Pocket”** — providing real-time, contextual, and personalized guidance to sales teams through integrated AI agents.

- **Decision for what to be Agent, Workflow, ot Component** (decision rubric + updated roster).
- **Right-Model** (CEO Sales Plan, Attainment, Team, Remuneration, Pursuit, Power Plan) drives **prioritization, gating, & feature weights** across the 4Cs calculators. 
- **Right-Tools** (FOG, Engagement Excellence, Buyers/Beneficiaries/Backers, Find the Money, Client Profiles, Impact vs Activity) feed **signals** into Knowledge, Trust, Mastery, Influence, Outcome, Satisfaction. 
- Scoring aligns to **Credibility = Knowledge × Trust, Capability = Competence × Quantum, Commitment = Outcome × Satisfaction, Control = Mastery × Influence**; **YES/NO gate** (NO ⇒ max 50). 
- **Data buckets** & **LLM cost-controls** (RAG-first, short-prompt schema, output caching, vector hit-rate SLO, dedup embeddings) specified.

---

## 1.1) Agent, Workflow, Or Component – Decision Rubric

**Agent = autonomous decision-maker** that:
- Consumes **multi-source context**, applies **policy/method**, chooses **actions/next steps**, and produces **prescriptions** (e.g., NBM, plan rewrite).
- Requires **LLM reasoning** + tool use + **explainable rationale**.
- Can be **HITL-gated** (human-in-the-loop) before writing back to systems.

**Component = shared capability** that:
- Offers a **deterministic service** (CRUD, scoring math, search, indexing, sync).
- Is **stateless or state-scoped**, versioned, testable via contracts.
- Does **not** decide strategy; it **enables** agents.


## 2. Architecture Overview

### **2.1 Layered Design**

| Layer | Description | Tech Stack |
|-------|--------------|-------------|
| **Frontend (Web/Mobile)** | UI for Client Expert, Solution Master, Executive | React.js (Web), React Native (Mobile), Tailwind, shadcn/ui |
| **Backend APIs** | Core business logic, CRUD, scoring, orchestration | FastAPI (Python), Node.js (TypeScript) |
| **AI Agent Orchestration** | Graph-based multi-agent system | LangGraph + LangChain |
| **Memory & RAG Layer** | Persistent contextual memory & retrieval | LangMem + Weaviate / Azure AI Search |
| **Database** | Deals, users, scores, evidence | PostgreSQL, MongoDB |
| **Pipelines** | Data ingestion & embedding jobs | Airbyte, dbt, Prefect |
| **Infrastructure** | Cloud & CI/CD | Azure Cloud, Terraform IaC, Azure DevOps |
| **Monitoring** | Observability, analytics, dashboards | Datadog, App Insights, Mixpanel |

---

## 3. User Personas

1. **Client Expert (CE)** – Primary user; manages deals, receives AI coaching.
2. **Solution Master (SM)** – Provides technical expertise, validates Capability.
3. **Executive (Exec)** – Oversees portfolio, prioritizes deals, reallocates resources.
4. **Admin** – Manages organization onboarding, users, and billing.

---

## 4. Core Components

| Component | Description |
|------------|--------------|
| **Deal Service** | CRUD operations, status, ownership, stage tracking. |
| **Scoring Engine** | Calculates 4Cs and R2W from data, logs rationale. |
| **Coach Service** | Generates Next-Best-Move (NBM) using multi-agent orchestration. |
| **Agentic AI Fabric** | Graph of AI agents specialized per dimension. |
| **Integration Service** | Syncs CRM (Salesforce/HubSpot), Outlook, and other tools. |
| **Feedback Service** | Captures post-meeting notes and retrains local models. |
| **Admin Service** | Handles org onboarding, plans, and RBAC. |
| **Analytics Dashboard** | Visualizes trends, gaps, and performance. |

---

## 5. Agent Design (LangGraph)

| Agent | Role | Example Output |
|--------|------|----------------|
| **Company Agent** | Analyzes client & supplier data | Company insight brief |
| **Industry Agent** | Extracts trends & benchmarks | Market summary |
| **Client Agent** | Maps stakeholders & influence | Stakeholder map |
| **Deal Agent** | Computes deal health, suggests focus | R2W status & weak areas |
| **Right-Model Agent** | Aligns deal with CEO sales plan | Pursuit plan update |
| **Right-Tools Agent** | Suggests references & demos | Action cards |
| **Persona-Coach Agent** | Generates Next-Best-Move | “Secure CEO Meeting” action |
| **Feedback Agent** | Processes notes, updates scores | R2W delta |
| **Executive Agent** | Identifies systemic risks & interventions | Portfolio alert |
| **Memory Agent** | Stores contextual learnings (LangMem) | Long-term coaching history |

---

## 6. ⚙️ Scoring Algorithm Spec (4Cs + R2W)

### **6.1 Base Equation**

Right-to-Win (R2W) = Average(Credibility, Capability, Commitment, Control)

> Guard rule: if any C < 60 → cap R2W = 60  
> Licence-to-Sell = true if R2W ≥ 70 and all Cs ≥ 60

---

### **6.2 Component Formulas**

#### **Credibility = Knowledge × Trust**
| Sub-Factor | Data Signals | Formula |
|-------------|---------------|----------|
| Knowledge | % client-specific terms, embedding similarity, case relevance | 0.5×content relevance + 0.3×industry match + 0.2×reference count |
| Trust | Access level, executive engagement, sentiment | Sigmoid(access + sentiment + inbound ratio) |

→ **Credibility = Knowledge × Trust × 100**

---

#### **Capability = Competence × Quantum**
| Sub-Factor | Data Signals | Formula |
|-------------|---------------|----------|
| Competence | KPI impact, innovation vs benchmarks | Weighted mean of KPI uplift + innovation index |
| Quantum | Project scale, delivery history | (past_delivery_score + region_reference_score) / 2 |

---

#### **Commitment = Outcome × Satisfaction**
| Sub-Factor | Data Signals | Formula |
|-------------|---------------|----------|
| Outcome | Delivery reliability, contract recency | exp(-delay_days/τ) × reliability_index |
| Satisfaction | Advocacy level, NPS, adoption | (positive_feedback_rate × meeting_recency_weight) |

Cap Commitment ≤ 50 if no active deal (as per Stepping Stone rule).

---

#### **Control = Influence × Mastery × Question**
| Sub-Factor | Data Signals | Formula |
|-------------|---------------|----------|
| Influence | % Buyer/Backer/Beneficiary covered, meeting ownership | (role_coverage × engagement_depth) |
| Mastery | Proposal differentiation, competitor gap | NLP uniqueness index |
| Question | Binary: differentiator present in RFP | 1 if yes, 0 if no |

→ **Control = 0.5×Influence + 0.3×Mastery + 0.2×Question**

---

### **6.3 Scoring Output JSON**

```json
{
  "deal_id": "D-9876",
  "credibility": { "knowledge": 0.82, "trust": 0.76, "score": 62 },
  "capability": { "competence": 0.91, "quantum": 0.78, "score": 71 },
  "commitment": { "outcome": 0.60, "satisfaction": 0.70, "score": 63 },
  "control": { "influence": 0.68, "mastery": 0.80, "question": 1, "score": 72 },
  "right_to_win": 67,
  "licence_to_sell": false
}


⸻

7. 📡 Data Flow

Flow:
CRM / Outlook → Ingestion Pipeline (Airbyte/Prefect) → ETL (dbt) → Vector DB → AI Agents → Scoring Engine → Dashboard / Coach Chat.

⸻

8. 🔐 Security & Governance
	•	Auth: Entra ID B2C + OAuth2
	•	RBAC: Org > Team > Role hierarchy
	•	Data: Tenant isolation, private endpoints, Key Vault CMK
	•	Compliance: GDPR, DLP, consent tracking
	•	Audit: All read/write on sensitive objects logged in Log Analytics
	•	AI Governance: Model registry, bias evals, explainability logs

⸻

9. 📦 Deliverables / Modules

Phase	Key Deliverables	Duration
Phase 1 – MVE	Deal CRUD, Scoring Engine (4Cs), Coach Chat (Web), CRM Read-only	12 weeks
Phase 2 – MVP	Multi-Tenant infra, Mobile app, Billing, Exec Dashboard	+10 weeks
Phase 3 – Scale	Advanced analytics, what-if simulator, partner APIs	Continuous


⸻
10. Misc
## 10.1) Data Buckets & Sources (Company / Client / Industry / Deal)

**Company** (your org): references, cases, solution catalog, capacity, certifications, pricing guardrails.  
**Client**: accounts, contacts (Buyer/Beneficiary/Backer), meetings, emails, notes, satisfaction, budgets (“Find the Money”).   
**Industry**: benchmarks, trends, regulatory notes, competitor intel.  
**Deal**: opportunity meta, stage, proposals, pursuit/power plan snapshots, 4Cs history.

**Primary feeds**
- CRM (Salesforce/HubSpot): accounts/contacts/opportunities/activities.
- Email & Calendar (Microsoft Graph): meetings, attendees, recency/latency.
- File/Docs: proposals, SoWs, case studies (ADLS).
- Workbook constructs: Right-Model configs (CEO Sales Plan, Attainment, Team, Remuneration), Right-Tools libraries (FOG prompts/checklists, Engagement Excellence lenses, Client Profiles). 

---

## 10.2) Right-Model & Right-Tools → How They Influence 4Cs

### 10.2.1 Right-Model (plans) as **policy & weights**
Elements: **CEO Sales Plan, Attainment Plan, Team Plan, Remuneration Plan, Pursuit Plan, Power Plan, Right Clients, Right Team, Right Deals**. 

- **Eligibility / Gating:** If a deal is **not** a Right Client/Right Deal per CEO Sales Plan ⇒ **R2W soft-cap** at 60 until plan alignment tasks complete (e.g., retarget stakeholders, re-scope).  
- **Weights:** Attainment Plan **elevates** the weak-C weight in the scorer for in-plan Bedrock deals.  
- **Plan Compliance Feature:** % of Pursuit milestones met affects **Commitment (Outcome)** and **Control (Influence)**.  
- **Power Plan** is the operational canvas for the 4Cs and preserves the **YES/NO max-50 rule** on the four qualifying questions. 

### 10.2.2 Right-Tools (methods) as **signal extractors & normalizers**
- **FOG** (Fact / Opinion / Gossip): All textual evidence is labeled; **facts boost Knowledge & Mastery**, **opinions are discounted**, **gossip excluded** from scoring. 
- **Engagement Excellence (Six Lenses):** Completeness across lenses feeds **Knowledge** and **Influence** coverage. 
- **Buyers/Beneficiaries/Backers:** Role graph coverage and recency feed **Influence** and **Trust**. 
- **Find the Money:** Budget existence/owner/prioritization boosts **Commitment (Outcome,Satisfaction)** gates. 
- **Client Profiles & Traps:** Risk flags can **cap Control** until mitigations are logged. 
- **Impact over Activity:** Score changes track **impactful** actions only; activity without impact ignored. 

---

## 10.3) 4Cs Scoring Engine (Component)

**Canonical formulas** (from Right-to-Win guide) with YES/NO gating:  
- **Credibility = Knowledge × Trust**  
- **Capability = Competence × Quantum**  
- **Commitment = Outcome × Satisfaction**  
- **Control = Mastery × Influence**  
- If the corresponding **qualifying question** is answered **NO**, that C’s **max = 50**; **YES ⇒ up to 100**. 

### 10.3.1 Feature mapping (selected)
- **Knowledge:** (a) FOG-Fact ratio; (b) Six-Lens coverage; (c) proposal–strategy similarity; (d) case relevancy.   
- **Trust:** (a) exec access recency (CEO in 7 days); (b) inbound vs outbound ratio; (c) sentiment; (d) promise-kept streak. 
- **Competence:** (a) KPI uplift analogs; (b) top-quartile reference match; (c) method uniqueness excerpts.  
- **Quantum:** (a) count of regional/industry deployments; (b) scale match index (size vs history). 
- **Outcome:** (a) delivery to scope/SLA; (b) timeliness; (c) expansion. 
- **Satisfaction:** (a) NPS/CSAT proxies; (b) re-order cadence; (c) C-suite sponsorship.  
- **Mastery:** (a) distinct Impact Themes; (b) UVP presence; (c) “Only we can…” anchors. 
- **Influence:** (a) Buyer/Beneficiary/Backer coverage; (b) RFP fingerprints; (c) plan compliance. 

⸻

11. 🧭 Next Steps for Claude Code

Prompt

Create FastAPI endpoints for /deals, /score/{deal_id}/compute, and /coach/{deal_id}/next_best_move
Implement modular structure per the above outline.
Scaffold React frontend with login, dashboard, and AI chat window.

⸻

12. 🧪 Future Enhancements
	•	Conversational memory graph (LangMem)
	•	Simulation engine (“What if we improve Control by +5?”)
	•	Agent feedback explainability
	•	Model fine-tuning from historical coaching logs

⸻

13. 📚 References
	•	ImpactWon Requirements Document (Aug 2025)
	•	CEO-Led Sales Book & Power Plan Framework
	•	InTimeTec Proposal ImpactWon_V0.2
	•	DataInsightAI Platform Architecture

⸻

Author:
Rajeev Kumar (AI Architect)
InTimeTec – DataInsightAI

