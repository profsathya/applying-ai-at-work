# AI feedback check: authoring review

Course 180, standalone storage sprint 13. User authorized creating and publishing an optional demonstration of the repaired AI feedback. Editorial assessment is by the agents; no claim of participant learning or human review of final prose.

Sources: user request, docs/audits/2026-09-14-owned-course-ai-proxy.md, Sprint 4 AI Exchange source, course1/homepage.yaml, docs/AUTHORING.md and docs/AUTHORING_PRESENTATION.md, schema/frontmatter.schema.json, existing activity runtime. Author worker wrote one artifact; homepage worker updated only curated YAML. Parent reviewed the final body and prompts and changed the sample from a code block to a wrapping quotation, added the name-entry step, and made the rendered wrapper's submission instruction optional for zero-point, excluded, no-completion activities.

No prerequisites. Evidence is three generated questions plus a saved response and JSON export using a clearly fictional sample. Root cause of the old service is explicitly unconfirmed. AI does not grade or submit. Zero points, omit_from_final_grade true, completion_requirement none. No due date or rubric added. Separate module keeps the five-sprint schedule intact; scheduled homepage does not expose extra modules, so provide a Canvas link. No image needed for this short diagnostic.

Observed: artifact/homepage/full schema PASS; 231 unit tests PASS, including optional-wrapper regression. Module preview reports zero pages because AI Activity previews are unsupported; no automated visual pass claimed. Delivery-specific hosted renderer succeeded. Parent inspected the wrapper in browser at desktop and 390px phone width: explanatory sequence and launch/export controls are readable; wrapping sample eliminates initial horizontal overflow. Restored browser viewport. Runtime live generation/save/export and Canvas identity will be verified after publishing. No consequential missing design decision identified in this scope.

## Skills and version evidence
- .agents/skills/add-artifact/SKILL.md: SHA-256 `0c6b03504abb0a18ffce718c0bdbd0b86ffefbca536f7058d42a509833309d8a`
- .agents/skills/canvas-author/SKILL.md: SHA-256 `9f88d5913d8d51ea6f715391e128a7e0b0354835388834133663e6498eb05c4d`
- .agents/skills/maintain-homepage/SKILL.md: SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`
- .agents/skills/writing-to-teach/SKILL.md: SHA-256 `53c1d049c14a1fcfa6ba7edb5e24b52b1ea87fbdefa773ec1ab3c82169ab1f08`
- .agents/skills/writing-learning-goals/SKILL.md: SHA-256 `0a9427039031806b7eea78d5bf6a9fb22c629bf70b9cd20e42169fe817eca9da`
- .agents/skills/writing-assignments/SKILL.md: SHA-256 `469389aeb076ae0a290b14c2ff398df63633bc6a5e6b75b2ed5cad9b63e633b1`
- .agents/skills/reviewing-course-text/SKILL.md: SHA-256 `d678b608d5610c0314bab6276621bcac64cdf44898382b07deed606149626db2`
- .agents/skills/reviewing-course-text/references/review-record.md: SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`

## Final reviewed outputs
- course1/sprints/sprint-13/ai-feedback-check.md: SHA-256 `daac191bc5074fcb0c59c90a50970d10f1a638772f02c6474baa2f2f731d82ac`
- course1/homepage.yaml: SHA-256 `6288e7686861697979259335f668dddf9549d0f2bcc5e4884d7e21074815cc43`
