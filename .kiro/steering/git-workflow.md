# Git & Contribution Standards

## Branch Strategy

- `master` — stable, merged PRs only
- `feat/web-ui` — main development branch for the app
- Feature branches off `feat/web-ui` for individual modules/features

## Commit Messages

Format: `<type>: <short description>`

Types:
- `feat` — new feature or module
- `fix` — bug fix
- `refactor` — code restructure without behavior change
- `docs` — documentation only
- `style` — formatting, no code logic change
- `test` — adding or updating tests
- `chore` — build, config, tooling changes

Examples:
- `feat: add library module with post listing and filters`
- `fix: handle missing cadence field in niche.yaml gracefully`
- `refactor: extract fetch utility from app.js`

Keep subject under 72 characters. No period at end.

## Code Quality

- No commented-out code committed. Delete it — git has history.
- No `TODO` or `FIXME` without a linked issue or clear explanation.
- No debug prints/console.logs in committed code (use proper logging).
- Every file must have a purpose. No empty files, no placeholder files beyond `__init__.py`.

## PR Standards

- One concern per PR. Don't mix refactoring with feature work.
- PR description: what changed, why, how to test.
- All steering rules must pass before merge.
