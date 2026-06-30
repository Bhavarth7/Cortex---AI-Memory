# Branch protection (recommended setup)

Branch protection is configured in GitHub's settings, not in the repository
files. Enable it once for `main` so every change goes through CI and review.

## Via the GitHub UI

**Settings → Branches → Add branch ruleset** (or *Add classic branch protection rule*),
targeting `main`:

- ✅ **Require a pull request before merging**
  - Require at least **1** approval
  - Dismiss stale approvals when new commits are pushed
- ✅ **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Required checks (these are the CI job names from `.github/workflows/ci.yml`):
    - `Backend (pytest)`
    - `Frontend (build)`
- ✅ **Require conversation resolution before merging**
- ✅ **Do not allow bypassing the above settings** (applies to admins too)
- 🚫 Block force pushes and branch deletion on `main`

> The status-check names appear in the dropdown only after the CI workflow has
> run at least once. Push a commit or open a PR first, then add them.

## Via the GitHub CLI

Requires `gh` authenticated with admin rights on the repo:

```bash
gh api -X PUT repos/Bhavarth7/Cortex---AI-Memory/branches/main/protection \
  -H "Accept: application/vnd.github+json" \
  -f "required_status_checks[strict]=true" \
  -f "required_status_checks[contexts][]=Backend (pytest)" \
  -f "required_status_checks[contexts][]=Frontend (build)" \
  -F "enforce_admins=true" \
  -F "required_pull_request_reviews[required_approving_review_count]=1" \
  -F "restrictions=null"
```

## Solo / hackathon mode

If you're working alone and want speed without losing the safety net:

- Keep **Require status checks to pass** enabled (CI still gates merges).
- Set required approvals to **0** so you can self-merge once CI is green.
- Still block force pushes and deletion on `main`.
