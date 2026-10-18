# Data schema — `ai-dashboard/data/latest.json` (schema_version 1)

One JSON file drives both pages. `update/validate.py` enforces everything marked **(checked)**.

| Key | Type | Meaning |
|---|---|---|
| `schema_version` | int | Always `1` for this layout **(checked)** |
| `updated_at` | ISO 8601 with offset | Time of the last daily run, `+10:00` **(checked)** |
| `index` | `{name, version, url}` | The composite capability index used for `aa_index` |
| `fx` | `{aud_per_usd, as_of, source}` | Used for AUD conversions **(checked 0.8–2.5)** |
| `models[]` | object | One row per model (below) |
| `benchmarks[]` | `{name, unit, higher_is_better, what, entries[{model, value, vendor_reported, note?}]}` | Headline benchmark panels **(checked)** |
| `history` | `{metric, closed_frontier[], open_frontier[], local_under_aud50k[]}` | Frontier envelopes; each point `{date, value, model}`; dates ascending; values never fall **(checked)** |
| `forecast` | object | Forecast parameters and headline text (below) |
| `agent_hour_tokens` | `{input_cached_m, input_fresh_m, output_m, cache_read_fallback_fraction_of_input}` | Token profile of one agent-hour, for converting usage to API dollars |
| `plans[]` | object | Subscription plans (below) |
| `hardware[]` | `{name, kind, status, spec, price, note}` | Compute cards |
| `releases[]` | `{date, kind, title, summary, url}` | Newest first; `kind` ∈ model, hardware, pricing, benchmark, policy **(checked)** |
| `sources[]` | `{title, url}` | Footer sources (https) **(checked)** |
| `changelog[]` | `{date, what, why}` | Append-only record of material data changes **(checked)** |

## `models[]`
`id` (unique slug), `name`, `lab`, `released` (YYYY-MM-DD), `weights` (`open`|`closed`), `license` (required for open),
`params_total_b`, `params_active_b`, `aa_index` (0–100), `aa_effort`, `eci`, `cost_per_task_usd`,
`price_in`, `price_out`, `price_cache_read` (US$ per million tokens), `status` (`current`|`superseded`), `note`.
Unknown values are `null`.

## `forecast`
- `closed_growth_pts_per_month` `{low, central, high}` — index points per month for the closed frontier.
- `open_lag_months` `{low, central, high}` — how far the open frontier trails the closed one.
- `local_extra_lag_months` `{low, central, high}` — extra delay before a version runs on a desktop under AUD 50k.
- `horizon` — `measured[{model, date, minutes}]`, `doubling_months {low, high}`, `suite_ceiling_minutes`, `status`.
- `headline[]` — three plain-English sentences.
- `founder` — calculator parameters: `as_of`, `multiplier_growth_monthly {low, central, high}`, `swarm_parallel_fraction`, `swarm_coordination_overhead_per_agent`, `agent_utilisation_during_work`, `task_mix[{task, share, multiplier, kind}]` (shares sum to 1; kind ∈ digital, physical).

## `plans[]`
`id`, `name`, `vendor`, `price_usd_month`, `included_api_credit_usd`, `est_api_value_usd_month [lo, hi]`,
`est_agent_hours_week [lo, hi]`, `default_model` (must exist in `models[]`), `confidence`, `note`.
Prices are published; the `est_*` ranges are estimates and must be labelled as such on the page.
