# Decision Log


---

**2026-04-20 - First real canvas-course-builder build (course1)**

Executed first real canvas-course-builder build against De Anza canvas course 180. Planner produced 35 artifacts across 6 modules. Build completed after resolving the permission-mode bug and adding python3 allowlist entries. Loop now handles overloaded API errors with retry-with-backoff. Top-level README restructured to be builder + teammate-usage focused; certificate overview moved to context/certificate-overview.md. Lessons captured in AGENTS.md (cross-iteration memory), CLAUDE.md (developer reference), and README.md (operator reference).

---

**2026-04-20 - Adopted canvas-course-builder; answered "delivery platform" open question**

Adopted the canvas-course-builder scaffold as the delivery pipeline: a Ralph-loop-driven system that generates canvas artifacts directly from canvas-agnostic markdown via the Canvas REST API. Canvas is now the delivery platform. Canvas-agnostic markdown in this repo is the source of truth; per-canvas-course manifests (one per course shell) map MD files to canvas IDs. The legacy iframe-embedding pattern used in CST349 and CST395 is archived to archive/legacy-iframe-template/ for reference. The corresponding entry in open-questions.md is now resolved.

Timestamped record of significant design decisions and their reasoning. Newest entries at the top.

---

**2026-04-09 — Corrected frameworks.md to distinguish meta-habits from capabilities**

Corrected frameworks.md to distinguish meta-habits (Slow Down, Know Yourself, Take the Lead) from capabilities (SDL, IS, AB). Earlier draft conflated them. Meta-habits are behavioral practices — how a practitioner shows up to the work. Capabilities are what develops over time by practicing those habits in real work. Updated glossary to match.

**2026-04-08 — Course structure decided**

Each 10-week course consists of Week 1 orientation + 4 two-week sprints + Week 10 capstone. Rationale: working professionals need orientation before being asked to produce, and a consolidation/demonstration moment at the end. This shape is load-bearing for SDT — orientation creates the autonomy moment (participants choose their problem), capstone creates the competence moment (participants demonstrate what they can now do). The sprint cadence provides rhythm without micromanaging weekly deliverables.

**2026-04-08 — Repository initialized**

Repository initialized as the design starting point for the "Applying AI at Work" certificate. Audience defined as working professionals. Frameworks-only approach for module content — the team will develop specific module content, sprint themes, weekly briefings, and assessments within the prescribed structure. This repo does not inherit from or depend on CST349 or CST395.
