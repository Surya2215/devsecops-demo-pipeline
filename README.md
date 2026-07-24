# DevSecOps Demo Pipeline

A small, working DevSecOps CI/CD pipeline built entirely with open-source
tooling, demonstrating security integrated at four stages: secret scanning,
SAST, SCA, and IaC scanning — plus a local pre-commit gate before code ever
reaches CI.

Built as a hands-on companion to interview prep — the goal is a pipeline you
can actually point to and say "I built this," not just describe conceptually.

---

## Pipeline stages and why each tool was chosen

| Stage | Tool | Why |
|---|---|---|
| Local pre-commit | pre-commit + Gitleaks + Black + Checkov | Catches secrets and obvious issues before code ever leaves the developer's machine — the earliest possible gate |
| Secret scanning (CI) | Gitleaks | Redundant safety net in case `--no-verify` bypassed the local hook |
| SAST | Semgrep (`p/ci` + `p/owasp-top-ten` rulesets) | Fast, low false-positive rate, free/open-source, easy to tune with custom rules |
| SCA | pip-audit | Checks pinned dependencies in `requirements.txt` against known CVEs, no API key required |
| IaC scanning | Checkov | Scans Terraform for misconfigurations before anything is ever provisioned |

All tools are open source — no paid licenses or API keys required to run this
pipeline end-to-end.

## Repository structure

```
devsecops-demo-pipeline/
├── .github/workflows/security-pipeline.yml   # the actual CI/CD pipeline
├── .pre-commit-config.yaml                    # local pre-commit gate
├── app/app.py                                 # small Flask app for scanners to analyze
├── requirements.txt                           # dependencies for the SCA stage
├── terraform/main.tf                          # sample IaC for the Checkov stage
└── README.md
```

## Intentional demo findings

Two files contain deliberately-included, clearly-labeled issues so the
pipeline has something real to catch on the first run (useful for a
before/after screenshot for a portfolio or interview walkthrough):

- `app/app.py` — a fake, non-functional placeholder API key for Gitleaks to catch
- `terraform/main.tf` — an S3 bucket missing encryption/versioning/public-access blocking, for Checkov to catch (a corrected version is commented directly below it)

Remove/fix these once you've captured your evidence, so the repo reflects a
genuinely clean state going forward.

## Gating philosophy (matches the risk-tiered approach discussed in prep)

- **Secret scanning and SAST** — hard fail. No severity threshold; a leaked
  secret or a confirmed high-severity code pattern blocks the pipeline outright.
- **SCA** — hard fail on any known CVE match in a pinned dependency.
- **IaC scanning** — currently set to `soft_fail: true` (reports but doesn't
  block), matching a "warn on findings while the team calibrates the ruleset"
  approach. Flip to `soft_fail: false` once you're ready to make it a hard gate
  — this single-line change is a good thing to demonstrate live in an interview
  if asked "how would you tighten this."

## How to run it

1. **Fork/push this repo to your own GitHub account.**
2. GitHub Actions runs automatically on every push/PR to `main` — no extra
   setup required, since every tool used here is free and open source.
3. To enable the local pre-commit gate:
   ```bash
   pip install pre-commit
   pre-commit install
   ```
   From then on, `git commit` triggers the same checks locally, before CI
   even sees the change.
4. To run any stage manually:
   ```bash
   pip install pip-audit && pip-audit -r requirements.txt
   pip install checkov && checkov -d terraform/
   ```

## What this demonstrates (for interview framing)

- Security-as-code: every gate lives in version-controlled config
  (`.github/workflows/`, `.pre-commit-config.yaml`), not manual UI clicks
- Shift-left in practice: the same checks run locally via pre-commit before
  they run again in CI as a safety net
- A real, risk-tiered gating policy — not "fail on everything," a defensible
  severity-based approach
- Entirely open-source tooling, directly matching "developing a DevSecOps
  CI/CD pipeline completely using open source tools"

## Natural next steps to extend this

- Add a container build + Trivy image scan stage
- Add DAST (OWASP ZAP baseline scan) against a deployed instance of the app
- Add OPA/Conftest for policy-as-code enforcement on the Terraform plan output
- Add a Kubernetes manifest + kube-bench/Checkov Kubernetes-framework scan
