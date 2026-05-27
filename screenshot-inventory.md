# Screenshot Inventory

## Current draft (2026-05-25 rewrite)

- `screenshots/evidence-dashboard.png` — opening hero (May 22 capture of the live system during the EV charging anecdote that opens the article).
- `screenshots/data-fusion-sankey.png` — §2 closer, illustrating the five-vendors-into-one-state-graph thesis with concrete live numbers.
- `screenshots/state-machine-policy-engine.png` — §5 (policy engine). Shows the Franklin policy modes plus Rivian/ChargePoint and EcoFlow advisory lanes with transition triggers.
- `screenshots/churn-reduction-chart.png` — §6 evidence. Per-hour transition counts for `write_allowed` and `target_charge_w`, before/after the retune-fix deploy at 10:33 PDT. 97-98% reduction.
- `screenshots/drift-sentinel-card.png` — §6 artifact. Card view of `sensor.energy_manager_policy_drift = aligned`, showing all three checksums match and noting the tamper-test that produced a `drifted_static` transition.
- `screenshots/live-dashboard.png` — §9 closing. The deployed live dashboard at a steady-state moment with Franklin in SOLAR_HOLD, EV at target, EcoFlows waiting for a slot.

## Source HTML for generated screenshots

All re-renderable via Playwright from local files (served over `python3 -m http.server` to satisfy Playwright's http-only constraint):

- `screenshots/data-fusion-sankey.html` — custom layout with live values pulled from the HA API at capture time
- `screenshots/churn-reduction-chart.html` — SVG bar chart with hand-computed per-hour data from the recorder
- `screenshots/drift-sentinel-card.html` — card-style layout with checksum + boundary panels
- `screenshots/evidence-dashboard.html` — original May 22 hero template (still in use)

## Reusable from May 22 if needed

- `screenshots/node-red-franklin-dashboard-live.png` — Node-RED Franklin dashboard during EV charging.
- `screenshots/franklin-state-machine.png` — original static state-machine diagram (superseded by `state-machine-policy-engine.png` for the current article).
- `screenshots/node-red-flow-diagram.png` — Node-RED flow structure (observe / normalize / gate / decision / output).

## Not captured

- Home Assistant Lovelace dashboards: behind interactive login. The `live-dashboard.png` capture uses the locally-rendered HTML with a fetched sanitized JSON snapshot, which is the same view the deployed dashboard provides.
- SPAN, Enphase, FranklinWH, Rivian, ChargePoint native apps: not approached for vendor screenshots.

## Suggested manual additions if publishing publicly

- A Home Assistant Energy dashboard screenshot after logging in (the Sankey card on the Energy view, for variety vs. the custom render here).
- A SPAN circuit detail screenshot showing the cluster breaker.
- A redacted utility bill reconciliation screenshot if covering billing accuracy.
