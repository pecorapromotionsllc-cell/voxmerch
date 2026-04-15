# External Skills Index

Third-party Claude skill repos bundled inside this project. Each is dropped under the binder that most matches its focus area. Upstream source URLs are listed so they can be updated or re-installed cleanly on any device.

If one of these is updated upstream, the cleanest refresh is to delete the local copy and replace it with the latest release from the source.

## voxmerch-platform/external-skills/

### agent-skills-main
Coding-focused Claude agent skills: TDD, debugging, CI/CD, security, planning, performance optimization, spec-driven development.
- Upstream: Anthropic `agent-skills` (github.com/anthropics/agent-skills or similar)
- Local path: `voxmerch-platform/external-skills/agent-skills-main/`
- Primary use: developer work on the VoxMerch SaaS platform.

## voxmerch-marketing-site/external-skills/

### claude-seo-main
SEO plugin for Claude covering audits, backlinks, schema, technical SEO, sitemaps, content, programmatic SEO, and local SEO. Includes DataForSEO and Firecrawl extensions.
- Upstream: `claude-seo` plugin
- Local path: `voxmerch-marketing-site/external-skills/claude-seo-main/`
- Primary use: SEO and technical health of voxmerch.com.

## voxmerch-content/external-skills/

### marketingskills-main
Broad marketing skill pack: copywriting, ad creative, email sequences, cold email, content strategy, A/B tests, CRO (page/form/onboarding/paywall), lead magnets, customer research, marketing psychology.
- Upstream: `marketingskills` plugin
- Local path: `voxmerch-content/external-skills/marketingskills-main/`
- Primary use: written marketing execution.

## voxmerch-launch-ops/external-skills/

### business-coach
Business strategy skill powered by a curated canon of business books. Strategy, hiring, pricing, culture, scaling, decisions.
- Upstream: `business-coach` plugin
- Local path: `voxmerch-launch-ops/external-skills/business-coach/`
- Primary use: launch decisions and cross-functional strategy calls during the launch window.

## Notes

- `marketingskills-main (1)` in the Dropbox source was skipped as a duplicate of `marketingskills-main`.
- If any of these should live in a different binder, move the folder and update this index.
- Every external-skills folder includes its own LICENSE. Respect the upstream license when redistributing.
