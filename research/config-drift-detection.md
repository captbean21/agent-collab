
## Research Cycle — 2026-11-07 21:51 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/Elshayib

## Popular repositories Loading

1. 
                [omarchy-oligarchy-theme](/Elshayib/omarchy-oligarchy-theme)
              omarchy-oligarchy-theme Public A dark medieval-keep theme for Omarchy: iron-grey stone, antique gold windows, moonlight text. Elite capital. Public code.

Something went wrong, please refresh the page to try again.

If the problem persists, check the [GitHub status page](https://www.githubstatus.com/)
          or [contact support](/contact).

---

### Source: https://github.com/Pratik1566/config-drift-detector

An AI-assisted configuration drift detection platform that identifies servers whose configurations differ from an approved fleet baseline, evaluates potential risks, and explains detected changes using a locally running open-weight AI model.

- **Configuration Drift Detection:** Identifies differences between approved baseline configurations and current configurations.
- **Fleet-Based Scanning:** Supports configuration analysis across multiple server profiles.
- **Risk Scoring:** Evaluates detected changes using predefined security rules and risk scores.
- **AI-Powered Explanations:** Uses a local Qwen model through Ollama to explain detected drift and suggest possible fixes.
- **Interactive Dashboard:** Displays configuration findings and scan results through Streamlit.
- **Scan Reports:** Saves scan results for later review and analysis.
- **Automated Testing:** Tests whether deliberately introduced configuration changes are detected correctly.
- **Modular Architecture:** Separates data collection, detection, risk rules, AI explanations, and dashboard components.

- **Programming Language:** Python
- **Dashboard:** Streamlit
- **Local AI Runtime:** Ollama
- **AI Model:** Qwen3 4B (or a supported fallback model)
- **Configuration Data:** JSON and other explicitly supported configuration formats
- **Testing:** Python testing tools

1. Install Python 3.11 or later.
2. Install Git.
3. Install Ollama.
4. Ensure the selected Qwen model is supported by your Ollama installation.

```
git clone <repo-url>
cd config-drift-detector
```
Replace `<repo-url>` with your repository URL.

On Windows PowerShell:

```
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, follow the Python virtual-environment instructions for your operating system.

`python -m pip install -r requirements.txt`
For the primary model:

`ollama pull qwen3:4b`
Optional smaller fallback model:

`ollama pull qwen3:1.7b`
Confirm that the model is available:

`ollama list`
The fallback model must also be configured in the application if the code is expected to use it automatically.

From the project root directory, run:

`streamlit run app/app.py`
Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

1. **Load Configuration Data:** Read the available configuration data and approved baseline.
2. **Parse Settings:** Extract supported settings from the input using the appropriate parser.
3. **Compare Configurations:** Identify changed, missing, and newly added settings.
4. **Evaluate Risks:** Apply predefined rules to assess the potential impact of detected changes.
5. **Generate Explanations:** Use the local AI model to explain findings and suggest possible corrections.
6. **Display Results:** Present findings through the dashboard.
7. **Save Reports:** Store scan results for future review and comparison.

```
config-drift-detector/
├── fleet/
│   ├── generate_fleet.py
│   └── inject_drift.py
├── collector/
│   └── ...
├── engine/
│   └── ...
├── rules/
│   └── risky_settings.json
├── ai/
│   ├── mock.py
│   └── ...
├── app/
│   └── app.py
├── tests/
│   └── ...
├── docs/
│   └── samples/
├── requirements.txt
└── README.md
```
This is the intended project structure. Update the tree to reflect the files actually present in the repository.

- **Model:** Qwen3 4B
- **Runtime:** Ollama
- **Execution:** Locally on the user's machine
- **Parameters:** Approximately 4 billion
- **Fallback:** Qwen3 1.7B, if configured and supported by the application
- **Model License:** Verify the exact model's license on its official model page before redistribution or deployment.

Official references:

- Ollama: [https://ollama.com/](https://ollama.com/)
- Qwen3 4B: [https://ollama.com/library/qwen3:4b](https://ollama.com/library/qwen3:4b)
- Qwen3 1.7B: [https://ollama.com/library/qwen3:1.7b](https://ollama.com/library/qwen3:1.7b)

- Scan only systems and configuration files you are authorized to assess.
- Treat configuration files as potentially sensitive because they may contain internal infrastructure details.
- Avoid exposing credentials, private keys, tokens, or other secrets in scan reports or AI prompts.
- Review AI-generated explanations and recommendations before applying any changes.
- Do not interpret a risk score as a probability that an attack will occur.
- Unsupported directives and parsing limitations should be reported clearly.
- Do not automatically modify production configurations without an authorized, tested change-management process.

- Detection accuracy depends on the quality of the approved baseline, parsing logic, and security rules.
- Different configuration formats require their own parsers and validation rules.
- Some configurations contain defaults, included files, conditional sections, or other behavior that a basic parser may not fully interpret.
- AI-generated explanations may be incomplete or incorrect and should be validated.
- Features such as Docker collection, multi-server scanning, and automated drift injection are available only when their corresponding modules are implemented.

Run the project's tests using the test framework configured in the repository.

If the project uses pytest, install it if necessary and run:

`python -m pytest`
Tests should cover:

- Unchanged configurations.
- Changed settings.
- Missing settings.
- Newly added settings.
- Risk-rule evaluation.
- Invalid or unsupported configuration input.
- AI response validation and fallback behavior.

1. Create a separate feature branch. git checkout -b feature/your-feature-name
2. Make changes within your assigned files or modules.
3. Run the relevant tests.
4. Commit your changes. git add . git commit -m "Add your feature description"
5. Push your branch. git push -u origin feature/your-feature-name
6. Open a pull request for review.

Avoid modifying the same files as another team member without coordinating first.

Contributions are welcome. Please use feature branches, test changes before submitting them, and describe the purpose and behavior of your changes in the pull request.

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Research Cycle — 2026-11-08 00:06 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/Pratik1566/config-drift-detector

An AI-assisted configuration drift detection platform that identifies servers whose configurations differ from an approved fleet baseline, evaluates potential risks, and explains detected changes using a locally running open-weight AI model.

- **Configuration Drift Detection:** Identifies differences between approved baseline configurations and current configurations.
- **Fleet-Based Scanning:** Supports configuration analysis across multiple server profiles.
- **Risk Scoring:** Evaluates detected changes using predefined security rules and risk scores.
- **AI-Powered Explanations:** Uses a local Qwen model through Ollama to explain detected drift and suggest possible fixes.
- **Interactive Dashboard:** Displays configuration findings and scan results through Streamlit.
- **Scan Reports:** Saves scan results for later review and analysis.
- **Automated Testing:** Tests whether deliberately introduced configuration changes are detected correctly.
- **Modular Architecture:** Separates data collection, detection, risk rules, AI explanations, and dashboard components.

- **Programming Language:** Python
- **Dashboard:** Streamlit
- **Local AI Runtime:** Ollama
- **AI Model:** Qwen3 4B (or a supported fallback model)
- **Configuration Data:** JSON and other explicitly supported configuration formats
- **Testing:** Python testing tools

1. Install Python 3.11 or later.
2. Install Git.
3. Install Ollama.
4. Ensure the selected Qwen model is supported by your Ollama installation.

```
git clone <repo-url>
cd config-drift-detector
```
Replace `<repo-url>` with your repository URL.

On Windows PowerShell:

```
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, follow the Python virtual-environment instructions for your operating system.

`python -m pip install -r requirements.txt`
For the primary model:

`ollama pull qwen3:4b`
Optional smaller fallback model:

`ollama pull qwen3:1.7b`
Confirm that the model is available:

`ollama list`
The fallback model must also be configured in the application if the code is expected to use it automatically.

From the project root directory, run:

`streamlit run app/app.py`
Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

1. **Load Configuration Data:** Read the available configuration data and approved baseline.
2. **Parse Settings:** Extract supported settings from the input using the appropriate parser.
3. **Compare Configurations:** Identify changed, missing, and newly added settings.
4. **Evaluate Risks:** Apply predefined rules to assess the potential impact of detected changes.
5. **Generate Explanations:** Use the local AI model to explain findings and suggest possible corrections.
6. **Display Results:** Present findings through the dashboard.
7. **Save Reports:** Store scan results for future review and comparison.

```
config-drift-detector/
├── fleet/
│   ├── generate_fleet.py
│   └── inject_drift.py
├── collector/
│   └── ...
├── engine/
│   └── ...
├── rules/
│   └── risky_settings.json
├── ai/
│   ├── mock.py
│   └── ...
├── app/
│   └── app.py
├── tests/
│   └── ...
├── docs/
│   └── samples/
├── requirements.txt
└── README.md
```
This is the intended project structure. Update the tree to reflect the files actually present in the repository.

- **Model:** Qwen3 4B
- **Runtime:** Ollama
- **Execution:** Locally on the user's machine
- **Parameters:** Approximately 4 billion
- **Fallback:** Qwen3 1.7B, if configured and supported by the application
- **Model License:** Verify the exact model's license on its official model page before redistribution or deployment.

Official references:

- Ollama: [https://ollama.com/](https://ollama.com/)
- Qwen3 4B: [https://ollama.com/library/qwen3:4b](https://ollama.com/library/qwen3:4b)
- Qwen3 1.7B: [https://ollama.com/library/qwen3:1.7b](https://ollama.com/library/qwen3:1.7b)

- Scan only systems and configuration files you are authorized to assess.
- Treat configuration files as potentially sensitive because they may contain internal infrastructure details.
- Avoid exposing credentials, private keys, tokens, or other secrets in scan reports or AI prompts.
- Review AI-generated explanations and recommendations before applying any changes.
- Do not interpret a risk score as a probability that an attack will occur.
- Unsupported directives and parsing limitations should be reported clearly.
- Do not automatically modify production configurations without an authorized, tested change-management process.

- Detection accuracy depends on the quality of the approved baseline, parsing logic, and security rules.
- Different configuration formats require their own parsers and validation rules.
- Some configurations contain defaults, included files, conditional sections, or other behavior that a basic parser may not fully interpret.
- AI-generated explanations may be incomplete or incorrect and should be validated.
- Features such as Docker collection, multi-server scanning, and automated drift injection are available only when their corresponding modules are implemented.

Run the project's tests using the test framework configured in the repository.

If the project uses pytest, install it if necessary and run:

`python -m pytest`
Tests should cover:

- Unchanged configurations.
- Changed settings.
- Missing settings.
- Newly added settings.
- Risk-rule evaluation.
- Invalid or unsupported configuration input.
- AI response validation and fallback behavior.

1. Create a separate feature branch. git checkout -b feature/your-feature-name
2. Make changes within your assigned files or modules.
3. Run the relevant tests.
4. Commit your changes. git add . git commit -m "Add your feature description"
5. Push your branch. git push -u origin feature/your-feature-name
6. Open a pull request for review.

Avoid modifying the same files as another team member without coordinating first.

Contributions are welcome. Please use feature branches, test changes before submitting them, and describe the purpose and behavior of your changes in the pull request.

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Source: https://github.com/Coding-Dev-Tools/configdrift

Keep configurations consistent across all environments, automatically. ConfigDrift compares configs, flags drift, and reports compliance violations before they cause incidents.

⭐ **Star this repo** if you manage multi-environment configs — it helps other devs find ConfigDrift!

Real-world scenarios:

- **Multi-environment compliance**: Ensure staging and prod configs are identical before every deploy
- **Secrets audit**: Detect env vars that exist in one environment but are missing in another
- **CI/CD gating**: Block PRs that introduce config drift across environments
- **Incident prevention**: Catch a changed database endpoint before it causes a production outage

ConfigDrift is **not published to public PyPI**. Install from the self-hosted index, a direct GitHub install, or via Homebrew/Scoop (below).

```
# Install directly from GitHub (recommended)
pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
```
Editable install for development:

`pip install -e ".[dev]"`
Then run: `configdrift --help`

Compare two config files:

`configdrift check dev.yaml prod.yaml`
Scan entire directories as environments:

`configdrift scan ./config/dev ./config/staging ./config/prod`
Use a config file to define environments:

```
configdrift init
configdrift scan --config .configdrift.yaml
```
`configdrift check <file1> <file2> [--output table|json|silent] [--baseline dev] [--target prod]`
Output formats:

- `table` (default): Rich colored table output
- `json`: Machine-readable JSON for CI integration
- `silent`: Exit code only (0 = no breaking drift, 1 = breaking drift found)

`configdrift scan ./dev ./staging ./prod --baseline dev`
Scans all config files in each directory, merges them, and compares against a baseline environment.

`configdrift init .`
Creates `.configdrift.yaml` in the specified directory.

Use `--output silent` for CI gating:

`configdrift check dev.yaml prod.yaml --output silent || echo "Drift detected!"````
- name: Detect config drift
  run: |
    pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
    configdrift check ./config/staging/app.yaml ./config/prod/app.yaml --output silent
```
- **Exit code 1 with no output**: use `--output table` to inspect drift details.
- **TOML parsing errors on Python \< 3.11**: install `tomli` and `tomli-w` or use Python 3.11+.
- **Large config scans are slow**: narrow the scan to changed files or a single directory.
- **Unexpected breaking drift**: review severity rules in the project settings; `database*` and `auth*` keys are flagged as breaking by default.

| Format | Extension | Notes | 
|---|---|---|
| YAML | `.yaml`, `.yml` | Full nested structure support | 
| JSON | `.json` | Nested flattening | 
| TOML | `.toml` | Python 3.11+ native | 
| .env | `.env` | `KEY=VALUE` format | 

- **Info**: Non-critical value changes
- **Warning**: Added or removed optional keys
- **Breaking**: Changes to critical keys (`database*`, `auth*`, `api_key*`, `secret*`, `password*`, `token*`, `endpoint*`)

```
# Install with dev dependencies
pip install -e ".[dev]"
# Run tests
pytest
# Run with coverage
pytest --cov=configdrift
```
ConfigDrift is one of 11 tools in the Revenue Holdings suite. One license covers all CLI tools.

| Plan | Price | Best For | 
|---|---|---|
| **Free** | $0 | Individual devs, OSS — CLI only, 1 env pair | 
| **ConfigDrift Individual** | **$15/mo** ($12 billed annually) | Professional devs — unlimited environments, custom rules | 
| **Suite (all 11 tools)** | **$49/mo** ($39 billed annually) | Full Revenue Holdings toolkit — 40% savings | 
| **Team** | **$79/mo** ($63 billed annually) | Up to 5 devs — drift history, Slack alerts, priority support | 
| **Enterprise** | Custom | SSO, RBAC, compliance reports, dedicated support | 

🔹 **No lock-in**: CLI works fully offline on the free tier — no telemetry, no phone-home.
🔹 **Annual billing**: Save 20%.

| Feature | Free | ConfigDrift | Suite | Team | Enterprise | 
|---|---|---|---|---|---|
| CLI: check, scan | ✓ | ✓ | ✓ | ✓ | ✓ | 
| Unlimited environments | — | ✓ | ✓ | ✓ | ✓ | 
| Custom rules / policies | — | ✓ | ✓ | ✓ | ✓ | 
| Drift history / audit trail | — | — | — | ✓ | ✓ | 
| Slack / webhook alerts | — | — | — | ✓ | ✓ | 
| Compliance reports | — | — | — | — | ✓ | 
| RBAC | — | — | — | — | ✓ | 
| SSO / SAML / OIDC | — | — | — | — | ✓ | 
| Priority support | Community | 24h | 24h | 8h | Dedicated | 

<sub>Part of [Revenue Holdings](https://coding-dev-tools.github.io/devforge/) — CLI tools built by autonomous AI.</sub>

MIT

`npm test  # runs: node --test tests/`

---

## Research Cycle — 2026-11-08 06:08 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/DriftGuard/DriftGuard

### Web Summary: https://github.com/DriftGuard/DriftGuard

# DriftGuard – Configuration Drift Detection Engine

## Core Purpose / Summary
DriftGuard is a Go-based GitOps drift detection platform that continuously compares live Kubernetes cluster state against desired state stored in Git repositories. It classifies drift types, assigns severity levels, tracks resolution status, and persists records in MongoDB. **It does NOT implement alerting or auto-rollback** — it is a detection and reporting layer only.

## Key Takeaways & Facts

- **Detection loop**: Periodic (default 30s) comparison of live cluster vs. Git manifests
- **Drift states**: `active` → `resolved` → `none` (with timestamps)
- **Classification**: 10 drift types (Scaling, VersionChange, ResourceChange, ConfigurationChange, LabelChange, AnnotationChange, PortChange, VolumeChange, SecretChange, ConfigMapChange)
- **Severity levels**: High / Medium / Low (auto-assigned)
- **Storage**: MongoDB 4.4+ for persistent drift records
- **API**: REST endpoints for records, filtering, statistics, manual analysis trigger
- **Monitoring**: Prometheus `/metrics` endpoint + emoji-structured logging
- **Stack**: Go 1.21+, MongoDB, Kubernetes, Git, kubectl
- **Deployment**: Docker container or native `go run`

## Notable Specifics

### Hash Configs
- The page references **"hash-based state tracking"** for Git integration (comparing live state vs. Git-stored manifests), but **no specific hash algorithm, hash config parameters, or hash comparison logic is documented** in this content.
- Config file (`backend/configs/config.yaml`) contains no hash-related fields:

```yaml
git:
  repository_url: "Add your Repo"
  default_branch: main
  clone_timeout: 5m
  pull_timeout: 2m
drift_detection:
  interval: 30s
  enable_periodic: true
```

### Alert
- **No alerting mechanism is present.** There is no integration with PagerDuty, Slack, email, or any notification system.
- The closest equivalents are:
  - Prometheus metrics endpoint (`GET /metrics`) — could feed external alerting (e.g., Alertmanager)
  - Structured logging with emoji markers (⚠️ drift detected, ✅ resolved, 🔄 continued)
- No alert thresholds, escalation policies, or webhook configurations are defined.

### Auto-Rollback
- **No auto-rollback feature exists.** DriftGuard is strictly a **detection and reporting** tool.
- Resolution is manual: the user must `kubectl scale` back or `kubectl apply` the Git manifest, then re-trigger analysis.
- The system detects *when* drift is resolved but does not *cause* the rollback.

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/health` | Health check |
| `GET` | `/ready` | Readiness check |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/v1/drift-records` | List all records |
| `GET` | `/api/v1/drift-records/:resourceId` | Specific record (`kind:namespace:name`) |
| `GET` | `/api/v1/drift-records/active` | Active drift only |
| `GET` | `/api/v1/drift-records/resolved` | Resolved drift only |
| `GET` | `/api/v1/statistics` | Aggregate stats |
| `POST` | `/api/v1/analyze` | Trigger manual analysis |

### Statistics Response Shape
```json
{
  "statistics": {
    "total_records": 25,
    "active_drift": 3,
    "resolved_drift": 15,
    "no_drift": 7,
    "recent_active_drift": 1,
    "recent_resolutions": 2,
    "active_percentage": 12.0,
    "resolved_percentage": 60.0
  }
}
```

### Kubernetes Config Parameters
```yaml
kubernetes:
  config_path: ""          # kubeconfig path (empty = default)
  context: ""
  namespaces: ["driftguard"]
  resources: ["deployments", "services", "configmaps", "secrets"]
  skip_system_namespaces: true
```

## Gap Summary (Requested Focus)

| Focus Area | Present? | Notes |
|---|---|---|
| Hash configs | Partially | "Hash-based state tracking" mentioned; no algorithm/params exposed |
| Alert | ❌ | Only Prometheus metrics + logs; no alerting pipeline |
| Auto-rollback | ❌ | Detection/reporting only; resolution is manual |

---

### Source: https://github.com/Pratik1566/config-drift-detector

An AI-assisted configuration drift detection platform that identifies servers whose configurations differ from an approved fleet baseline, evaluates potential risks, and explains detected changes using a locally running open-weight AI model.

- **Configuration Drift Detection:** Identifies differences between approved baseline configurations and current configurations.
- **Fleet-Based Scanning:** Supports configuration analysis across multiple server profiles.
- **Risk Scoring:** Evaluates detected changes using predefined security rules and risk scores.
- **AI-Powered Explanations:** Uses a local Qwen model through Ollama to explain detected drift and suggest possible fixes.
- **Interactive Dashboard:** Displays configuration findings and scan results through Streamlit.
- **Scan Reports:** Saves scan results for later review and analysis.
- **Automated Testing:** Tests whether deliberately introduced configuration changes are detected correctly.
- **Modular Architecture:** Separates data collection, detection, risk rules, AI explanations, and dashboard components.

- **Programming Language:** Python
- **Dashboard:** Streamlit
- **Local AI Runtime:** Ollama
- **AI Model:** Qwen3 4B (or a supported fallback model)
- **Configuration Data:** JSON and other explicitly supported configuration formats
- **Testing:** Python testing tools

1. Install Python 3.11 or later.
2. Install Git.
3. Install Ollama.
4. Ensure the selected Qwen model is supported by your Ollama installation.

```
git clone <repo-url>
cd config-drift-detector
```
Replace `<repo-url>` with your repository URL.

On Windows PowerShell:

```
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, follow the Python virtual-environment instructions for your operating system.

`python -m pip install -r requirements.txt`
For the primary model:

`ollama pull qwen3:4b`
Optional smaller fallback model:

`ollama pull qwen3:1.7b`
Confirm that the model is available:

`ollama list`
The fallback model must also be configured in the application if the code is expected to use it automatically.

From the project root directory, run:

`streamlit run app/app.py`
Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

1. **Load Configuration Data:** Read the available configuration data and approved baseline.
2. **Parse Settings:** Extract supported settings from the input using the appropriate parser.
3. **Compare Configurations:** Identify changed, missing, and newly added settings.
4. **Evaluate Risks:** Apply predefined rules to assess the potential impact of detected changes.
5. **Generate Explanations:** Use the local AI model to explain findings and suggest possible corrections.
6. **Display Results:** Present findings through the dashboard.
7. **Save Reports:** Store scan results for future review and comparison.

```
config-drift-detector/
├── fleet/
│   ├── generate_fleet.py
│   └── inject_drift.py
├── collector/
│   └── ...
├── engine/
│   └── ...
├── rules/
│   └── risky_settings.json
├── ai/
│   ├── mock.py
│   └── ...
├── app/
│   └── app.py
├── tests/
│   └── ...
├── docs/
│   └── samples/
├── requirements.txt
└── README.md
```
This is the intended project structure. Update the tree to reflect the files actually present in the repository.

- **Model:** Qwen3 4B
- **Runtime:** Ollama
- **Execution:** Locally on the user's machine
- **Parameters:** Approximately 4 billion
- **Fallback:** Qwen3 1.7B, if configured and supported by the application
- **Model License:** Verify the exact model's license on its official model page before redistribution or deployment.

Official references:

- Ollama: [https://ollama.com/](https://ollama.com/)
- Qwen3 4B: [https://ollama.com/library/qwen3:4b](https://ollama.com/library/qwen3:4b)
- Qwen3 1.7B: [https://ollama.com/library/qwen3:1.7b](https://ollama.com/library/qwen3:1.7b)

- Scan only systems and configuration files you are authorized to assess.
- Treat configuration files as potentially sensitive because they may contain internal infrastructure details.
- Avoid exposing credentials, private keys, tokens, or other secrets in scan reports or AI prompts.
- Review AI-generated explanations and recommendations before applying any changes.
- Do not interpret a risk score as a probability that an attack will occur.
- Unsupported directives and parsing limitations should be reported clearly.
- Do not automatically modify production configurations without an authorized, tested change-management process.

- Detection accuracy depends on the quality of the approved baseline, parsing logic, and security rules.
- Different configuration formats require their own parsers and validation rules.
- Some configurations contain defaults, included files, conditional sections, or other behavior that a basic parser may not fully interpret.
- AI-generated explanations may be incomplete or incorrect and should be validated.
- Features such as Docker collection, multi-server scanning, and automated drift injection are available only when their corresponding modules are implemented.

Run the project's tests using the test framework configured in the repository.

If the project uses pytest, install it if necessary and run:

`python -m pytest`
Tests should cover:

- Unchanged configurations.
- Changed settings.
- Missing settings.
- Newly added settings.
- Risk-rule evaluation.
- Invalid or unsupported configuration input.
- AI response validation and fallback behavior.

1. Create a separate feature branch. git checkout -b feature/your-feature-name
2. Make changes within your assigned files or modules.
3. Run the relevant tests.
4. Commit your changes. git add . git commit -m "Add your feature description"
5. Push your branch. git push -u origin feature/your-feature-name
6. Open a pull request for review.

Avoid modifying the same files as another team member without coordinating first.

Contributions are welcome. Please use feature branches, test changes before submitting them, and describe the purpose and behavior of your changes in the pull request.

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Source: https://github.com/oneuptime/blog/tree/master/posts/2026-02-26-configuration-drift-detection-gitops

### Web Summary: https://github.com/oneuptime/blog/tree/master/posts/2026-02-26-configuration-drift-detection-gitops

## Core Purpose / Summary

This article explains how ArgoCD detects configuration drift in GitOps by continuously comparing rendered Git manifests against live Kubernetes cluster state using a semantic diff algorithm. It covers common drift sources (manual edits, webhooks, HPA, controller mutations), remediation via `ignoreDifferences` configs, and automated self-healing (auto-rollback) with alerting.

## Key Takeaways & Facts

- Reconciliation loop runs every **120s + up to 60s jitter** (configurable via `timeout.reconciliation`)
- Diff is **semantic**, not textual: normalizes server-generated fields (`resourceVersion`, `uid`, `creationTimestamp`, `managedFields`), applies K8s defaults, then compares field-by-field
- Four primary drift sources: manual `kubectl` edits, mutating admission webhooks (Istio/Vault), HPA replica changes, controller mutations (ClusterIP assignment, volume reordering)
- Self-heal auto-sync uses a **5-second** timeout (vs. 120s for manual sync)
- Server-side diff (`controller.diff.server.side: "true"`) reduces false positives from defaulting/admission mutations; requires restarting `argocd-application-controller`
- Healthy environment = near-zero OutOfSync apps, decreasing drift duration, low unexpected sync frequency

## Notable Specifics

### Hash / Diff Configs (`ignoreDifferences`)

```yaml
spec:
  ignoreDifferences:
  # Ignore specific containers via jq
  - group: apps
    kind: Deployment
    jqPathExpressions:
    - '.spec.template.spec.containers[] | select(.name == "istio-proxy")'
    # Ignore a single field via JSON pointer
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
  # Ignore all fields managed by a specific controller
  - group: "*"
    kind: "*"
    managedFieldsManagers:
    - kube-controller-manager
```

Server-side diff toggle:

```yaml
# ConfigMap: argocd-cmd-params-cm (namespace: argocd)
data:
  controller.diff.server.side: "true"
```

### Alert (Drift Notifications)

```yaml
# ConfigMap: argocd-notifications-cm (namespace: argocd)
data:
  trigger.on-sync-status-unknown: |
    - when: app.status.sync.status == 'OutOfSync'
      send: [drift-alert]
  template.drift-alert: |
    message: |
      Application {{.app.metadata.name}} has drifted from Git.
      Sync Status: {{.app.status.sync.status}}
      Health: {{.app.status.health.status}}
```

Prometheus queries for drift monitoring:

```promql
count(argocd_app_info{sync_status="OutOfSync"})
sum by (phase) (increase(argocd_app_sync_total[24h]))
sum(increase(argocd_app_sync_total{phase=~"Failed|Error"}[24h]))
```

### Auto-Rollback (Self-Healing)

```yaml
syncPolicy:
  automated:
    selfHeal: true
```

- On drift detection → ArgoCD performs an automatic sync to restore desired state
- Self-heal retry interval: **5s** (controller self-heal timeout)
- **Critical pairing**: always combine `selfHeal: true` with matching `ignoreDifferences` rules; without them, ArgoCD will fight HPA/webhooks in a sync loop
- External Secrets / Sealed Secrets: the generated `Secret` differs from the `ExternalSecret` in Git — this is expected, not drift; ArgoCD manages the operator resource, not the derived Secret

---

## Research Cycle — 2026-11-08 18:05 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/DriftGuard/DriftGuard

### Web Summary: https://github.com/DriftGuard/DriftGuard

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
**Intelligent GitOps Configuration Drift Detection Engine**

DriftGuard is an intelligent GitOps configuration drift detection platform that continuously monitors Kubernetes resources for configuration drift by comparing live cluster states against desired states stored in Git repositories. It features enhanced state tracking, automatic resolution detection, and comprehensive drift analysis.

- **Enhanced Drift Detection**: Continuously monitors Kubernetes resources with intelligent drift classification
- **Drift Resolution Detection**: Automatically detects when drift is resolved and configuration matches Git again
- **State Management**: Tracks drift status (active/resolved/none) with timestamps and resolution messages
- **Git Integration**: Compares live state against Git-stored manifests with hash-based state tracking
- **Intelligent Classification**: Automatically classifies drift types (Scaling, VersionChange, ResourceChange, etc.)
- **Severity Assessment**: Assigns severity levels (low, medium, high) to detected drifts
- **MongoDB Storage**: Persistent storage of drift records with enhanced state tracking
- **REST API**: Comprehensive HTTP endpoints for querying drift records, status filtering, and statistics
- **Metrics & Monitoring**: Prometheus metrics and health checks
- **Enhanced Logging**: Detailed logging with emojis for drift detection and resolution events

Want to dive deeper into the configuration drift crisis and understand how DriftGuard solves real-world infrastructure challenges? Check out our comprehensive guide:

**[Learn More About DriftGuard](/DriftGuard/DriftGuard/blob/main/ABOUT.md)** - Discover the configuration drift crisis, understand GitOps vs InfraOps, explore real-world examples, and learn about DriftGuard's business value and architecture.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Kubernetes    │    │   Git Repo      │    │   DriftGuard    │
│   API Server    │    │   (Desired      │    │   Backend       │
│   (Live State)  │◄──►│   State)        │◄──►│   (Controller)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MongoDB       │    │   REST API      │
                       │   (Enhanced     │    │   (HTTP         │
                       │   Drift Records)│    │   Endpoints)    │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Prometheus    │    │   Health        │
                       │   Metrics       │    │   Checks        │
                       └─────────────────┘    └─────────────────┘
```
- **Go 1.21+**
- **MongoDB 4.4+**
- **Kubernetes cluster** (local or remote)
- **Git repository** with Kubernetes manifests
- **kubectl** configured to access your cluster

```
git clone <repository-url>
cd DriftGuard
```
```
# Create data directory
mkdir -p ~/data/db
# Start MongoDB (macOS/Linux)
sudo mongod --dbpath=~/data/db
# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```
Update the configuration file (`backend/configs/config.yaml`):

```
server:
  port: 8080
  read_timeout: 30s
  write_timeout: 30s
  idle_timeout: 60s
database:
  host: localhost
  port: 27017
  dbname: driftguard
  timeout: 10s
kubernetes:
  config_path: ""  # Leave empty for default kubeconfig
  context: ""
  namespaces: ["driftguard"]
  resources: ["deployments", "services", "configmaps", "secrets"]
  skip_system_namespaces: true
git:
  repository_url: "Add your Repo"
  default_branch: main
  clone_timeout: 5m
  pull_timeout: 2m
drift_detection:
  interval: 30s
  enable_periodic: true
```
```
# Create a dummy Git repository for testing
mkdir -p dummy-k8s-repo
cd dummy-k8s-repo
git init
# Create test Kubernetes manifests
cat > test-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  namespace: driftguard
  labels:
    app: nginx
    environment: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.23
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        env:
        - name: NGINX_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: driftguard
  labels:
    app: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: driftguard
data:
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
  environment: "production"
  version: "1.0.0"
EOF
# Commit the manifests
git add test-deployment.yaml
git commit -m "Initial Kubernetes manifests"
```
`kubectl create namespace driftguard````
cd backend
go run cmd/controller/main.go --config=configs/config.yaml
```
```
# Check if DriftGuard is running
curl http://localhost:8080/health
# Expected response:
# {"status":"healthy","message":"Service is running","time":"2025-01-15T10:30:00Z"}
```
```
# Apply the manifests from Git
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Verify resources are created
kubectl get all -n driftguard
```
```
# Trigger manual drift analysis
curl -X POST http://localhost:8080/api/v1/analyze
# Expected response:
# {"message":"Drift analysis triggered successfully","status":"started"}
```
```
# Wait a few seconds, then check drift records
sleep 5
curl http://localhost:8080/api/v1/drift-records
# You should see records with drift_detected: false initially
```
```
# Scale the deployment to create drift
kubectl scale deployment nginx-app -n driftguard --replicas=3
# Verify the change
kubectl get deployment nginx-app -n driftguard
```
```
# Trigger drift analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for drift detection
sleep 5
curl http://localhost:8080/api/v1/drift-records/active
# You should now see active drift records
```
```
# Scale back to original state
kubectl scale deployment nginx-app -n driftguard --replicas=2
# Or re-apply the Git manifest
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Trigger analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for resolution
sleep 5
curl http://localhost:8080/api/v1/drift-records/resolved
```
```
# Test image change drift
kubectl set image deployment/nginx-app nginx=nginx:1.24 -n driftguard
# Test environment variable drift
kubectl set env deployment/nginx-app NGINX_ENV=staging -n driftguard
# Test resource drift
kubectl patch deployment nginx-app -n driftguard -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"memory":"128Mi"}}}]}}}}'
# Trigger analysis after each change
curl -X POST http://localhost:8080/api/v1/analyze
```
```
# Get comprehensive statistics
curl http://localhost:8080/api/v1/statistics
# Expected response includes:
# - total_records
# - active_drift
# - resolved_drift
# - no_drift
# - active_percentage
# - resolved_percentage
```
```
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
# Get specific resource drift
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/health` | Basic health check | 
| `GET` | `/ready` | Readiness check | 
| `GET` | `/metrics` | Prometheus metrics | 

| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/api/v1/drift-records` | List all drift records | 
| `GET` | `/api/v1/drift-records/:resourceId` | Get specific drift record | 
| `GET` | `/api/v1/drift-records/active` | Get active drift records | 
| `GET` | `/api/v1/drift-records/resolved` | Get resolved drift records | 
| `GET` | `/api/v1/statistics` | Get drift statistics | 
| `POST` | `/api/v1/analyze` | Trigger manual drift analysis | 

**List Drift Records:**

```
# Get all drift records
curl http://localhost:8080/api/v1/drift-records
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
```
**Get Specific Record:**

```
# Get drift record for a specific resource
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
Resources are identified using the format: `kind:namespace:name`

The system tracks drift status with three states:

- **`active`**: Drift is currently detected and active
- **`resolved`**: Drift was previously detected but has been resolved
- **`none`**: No drift detected

The system automatically classifies drifts into categories:

- **Scaling**: Replica count changes
- **VersionChange**: Container image changes
- **ResourceChange**: CPU/memory resource changes
- **ConfigurationChange**: Environment variable changes
- **LabelChange**: Label modifications
- **AnnotationChange**: Annotation modifications
- **PortChange**: Port configuration changes
- **VolumeChange**: Volume mount changes
- **SecretChange**: Secret reference changes
- **ConfigMapChange**: ConfigMap reference changes

- **High**: Image changes, secret changes, significant scaling (>50%)
- **Medium**: Minor scaling, environment variables, ports, volumes
- **Low**: Labels, annotations, other metadata

The system provides comprehensive drift statistics:

```
{
  "statistics": {
    "total_records": 25,
    "active_drift": 3,
    "resolved_drift": 15,
    "no_drift": 7,
    "recent_active_drift": 1,
    "recent_resolutions": 2,
    "active_percentage": 12.0,
    "resolved_percentage": 60.0
  }
}
```
- `config_path`: Path to kubeconfig file
- `context`: Kubernetes context to use
- `namespaces`: List of namespaces to monitor
- `resources`: List of resource types to monitor
- `skip_system_namespaces`: Skip system namespaces

- `repository_url`: Git repository URL
- `default_branch`: Branch to monitor
- `clone_timeout`: Timeout for repository cloning
- `pull_timeout`: Timeout for pulling updates

- `interval`: Periodic analysis interval
- `enable_periodic`: Enable periodic drift detection

1. **MongoDB Connection Failed**
\# Check if MongoDB is running ps aux | grep mongod # Start MongoDB if not running sudo mongod --dbpath=\~/data/db
2. **Kubernetes Connection Failed**
\# Check kubectl configuration kubectl config current-context # Test cluster connection kubectl get nodes
3. **Git Repository Access Failed**
\# Check Git repository URL in config # Ensure repository is accessible git ls-remote \<repository-url>
4. **Port Already in Use**
\# Check if port 8080 is in use lsof -i :8080 # Kill process or change port in config

DriftGuard uses structured logging with emojis:

- 🚀 System startup
- ⚠️ Drift detected
- ✅ Drift resolved
- 🔄 Drift continued
- 📊 Analysis completed

```
# Build the container
docker build -t driftguard:latest backend/
# Run with environment variables
docker run -d \
  -p 8080:8080 \
  -e MONGODB_HOST=your-mongodb-host \
  -e KUBECONFIG=/path/to/kubeconfig \
  driftguard:latest
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: driftguard
  namespace: driftguard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: driftguard
  template:
    metadata:
      labels:
        app: driftguard
    spec:
      containers:
      - name: driftguard
        image: driftguard:latest
        ports:
        - containerPort: 8080
        env:
        - name: MONGODB_HOST
          value: "mongodb-service"
        volumeMounts:
        - name: kubeconfig
          mountPath: /root/.kube
          readOnly: true
      volumes:
      - name: kubeconfig
        secret:
          secretName: driftguard-kubeconfig
```
We welcome contributions! Please see our [Contributing Guidelines](/DriftGuard/DriftGuard/blob/main/CONTRIBUTING.md) for details.

This project is licensed under the MIT License - see the [LICENSE](/DriftGuard/DriftGuard/blob/main/LICENSE.md) file for details.

For questions, feature requests, or contributions, please open an issue in this repository.

---

### Source: https://github.com/Pratik1566/config-drift-detector

An AI-assisted configuration drift detection platform that identifies servers whose configurations differ from an approved fleet baseline, evaluates potential risks, and explains detected changes using a locally running open-weight AI model.

- **Configuration Drift Detection:** Identifies differences between approved baseline configurations and current configurations.
- **Fleet-Based Scanning:** Supports configuration analysis across multiple server profiles.
- **Risk Scoring:** Evaluates detected changes using predefined security rules and risk scores.
- **AI-Powered Explanations:** Uses a local Qwen model through Ollama to explain detected drift and suggest possible fixes.
- **Interactive Dashboard:** Displays configuration findings and scan results through Streamlit.
- **Scan Reports:** Saves scan results for later review and analysis.
- **Automated Testing:** Tests whether deliberately introduced configuration changes are detected correctly.
- **Modular Architecture:** Separates data collection, detection, risk rules, AI explanations, and dashboard components.

- **Programming Language:** Python
- **Dashboard:** Streamlit
- **Local AI Runtime:** Ollama
- **AI Model:** Qwen3 4B (or a supported fallback model)
- **Configuration Data:** JSON and other explicitly supported configuration formats
- **Testing:** Python testing tools

1. Install Python 3.11 or later.
2. Install Git.
3. Install Ollama.
4. Ensure the selected Qwen model is supported by your Ollama installation.

```
git clone <repo-url>
cd config-drift-detector
```
Replace `<repo-url>` with your repository URL.

On Windows PowerShell:

```
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, follow the Python virtual-environment instructions for your operating system.

`python -m pip install -r requirements.txt`
For the primary model:

`ollama pull qwen3:4b`
Optional smaller fallback model:

`ollama pull qwen3:1.7b`
Confirm that the model is available:

`ollama list`
The fallback model must also be configured in the application if the code is expected to use it automatically.

From the project root directory, run:

`streamlit run app/app.py`
Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

1. **Load Configuration Data:** Read the available configuration data and approved baseline.
2. **Parse Settings:** Extract supported settings from the input using the appropriate parser.
3. **Compare Configurations:** Identify changed, missing, and newly added settings.
4. **Evaluate Risks:** Apply predefined rules to assess the potential impact of detected changes.
5. **Generate Explanations:** Use the local AI model to explain findings and suggest possible corrections.
6. **Display Results:** Present findings through the dashboard.
7. **Save Reports:** Store scan results for future review and comparison.

```
config-drift-detector/
├── fleet/
│   ├── generate_fleet.py
│   └── inject_drift.py
├── collector/
│   └── ...
├── engine/
│   └── ...
├── rules/
│   └── risky_settings.json
├── ai/
│   ├── mock.py
│   └── ...
├── app/
│   └── app.py
├── tests/
│   └── ...
├── docs/
│   └── samples/
├── requirements.txt
└── README.md
```
This is the intended project structure. Update the tree to reflect the files actually present in the repository.

- **Model:** Qwen3 4B
- **Runtime:** Ollama
- **Execution:** Locally on the user's machine
- **Parameters:** Approximately 4 billion
- **Fallback:** Qwen3 1.7B, if configured and supported by the application
- **Model License:** Verify the exact model's license on its official model page before redistribution or deployment.

Official references:

- Ollama: [https://ollama.com/](https://ollama.com/)
- Qwen3 4B: [https://ollama.com/library/qwen3:4b](https://ollama.com/library/qwen3:4b)
- Qwen3 1.7B: [https://ollama.com/library/qwen3:1.7b](https://ollama.com/library/qwen3:1.7b)

- Scan only systems and configuration files you are authorized to assess.
- Treat configuration files as potentially sensitive because they may contain internal infrastructure details.
- Avoid exposing credentials, private keys, tokens, or other secrets in scan reports or AI prompts.
- Review AI-generated explanations and recommendations before applying any changes.
- Do not interpret a risk score as a probability that an attack will occur.
- Unsupported directives and parsing limitations should be reported clearly.
- Do not automatically modify production configurations without an authorized, tested change-management process.

- Detection accuracy depends on the quality of the approved baseline, parsing logic, and security rules.
- Different configuration formats require their own parsers and validation rules.
- Some configurations contain defaults, included files, conditional sections, or other behavior that a basic parser may not fully interpret.
- AI-generated explanations may be incomplete or incorrect and should be validated.
- Features such as Docker collection, multi-server scanning, and automated drift injection are available only when their corresponding modules are implemented.

Run the project's tests using the test framework configured in the repository.

If the project uses pytest, install it if necessary and run:

`python -m pytest`
Tests should cover:

- Unchanged configurations.
- Changed settings.
- Missing settings.
- Newly added settings.
- Risk-rule evaluation.
- Invalid or unsupported configuration input.
- AI response validation and fallback behavior.

1. Create a separate feature branch. git checkout -b feature/your-feature-name
2. Make changes within your assigned files or modules.
3. Run the relevant tests.
4. Commit your changes. git add . git commit -m "Add your feature description"
5. Push your branch. git push -u origin feature/your-feature-name
6. Open a pull request for review.

Avoid modifying the same files as another team member without coordinating first.

Contributions are welcome. Please use feature branches, test changes before submitting them, and describe the purpose and behavior of your changes in the pull request.

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Source: https://github.com/oneuptime/blog/tree/master/posts/2026-02-26-configuration-drift-detection-gitops

### Web Summary: https://github.com/oneuptime/blog/tree/master/posts/2026-02-26-configuration-drift-detection-gitops

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
Author: [nawazdhandala](https://github.com/nawazdhandala)

Tags: ArgoCD, GitOps, Kubernetes, Drift Detection, Security

Description: Understand how configuration drift detection works in GitOps with ArgoCD including how differences are calculated, common drift sources, and remediation strategies.

Configuration drift is the silent killer of reliable infrastructure. It happens when the actual state of your Kubernetes cluster diverges from the desired state defined in your Git repository. Without drift detection, you end up in a situation where nobody knows what is actually running in production versus what the manifests say should be running.

GitOps tools like ArgoCD make drift detection a first-class feature. But understanding how it works under the hood - and why it sometimes produces unexpected results - is essential for operating a healthy GitOps environment.

ArgoCD uses a continuous reconciliation loop to detect drift. Every few minutes (configurable, by default 120 seconds plus up to 60 seconds of jitter), the application controller performs the following steps:

```
sequenceDiagram
    participant Git as Git Repository
    participant Repo as Repo Server
    participant Controller as App Controller
    participant Cluster as Kubernetes Cluster
    Controller->>Repo: Generate manifests from Git
    Repo->>Git: Fetch latest revision
    Git-->>Repo: Repository content
    Repo-->>Controller: Desired state (rendered manifests)
    Controller->>Cluster: Get live state
    Cluster-->>Controller: Current resource specs
    Controller->>Controller: Compare desired vs live
    alt No Differences
        Controller->>Controller: Status = Synced
    else Differences Found
        Controller->>Controller: Status = OutOfSync
        Controller->>Controller: Record diff details
    end
```
    The comparison is a structured diff between the rendered manifests from Git and the live resources from the Kubernetes API server.

ArgoCD does not do a simple text comparison. It performs a semantic diff that understands Kubernetes resource structure:

1. **Normalize both sides**: Remove server-generated fields like `resourceVersion`, `uid`, `creationTimestamp`, and `managedFields`.
2. **Apply default values**: Kubernetes adds default values to resources when they are created. ArgoCD accounts for these so that a manifest missing an explicit `strategy` field does not show as drifted when Kubernetes adds the default `RollingUpdate` strategy.
3. **Compare field by field**: Each field in the desired state is compared to the corresponding field in the live state.
4. **Report differences**: Fields that differ are reported with their expected and actual values.

```
# View the diff for an application
argocd app diff my-app
# Example output:
# ===== apps/Deployment my-app/payment-api ======
# --- desired
# +++ live
# @@ -15,7 +15,7 @@
#        containers:
#        - name: payment-api
# -        image: payment-api:v2.0.9
# +        image: payment-api:v2.1.0
#          resources:
# -          limits:
# -            memory: "512Mi"
# +          limits:
# +            memory: "1Gi"
```
The most obvious source of drift. Someone runs `kubectl edit` or `kubectl scale` and changes a resource directly:

```
# This creates drift
kubectl scale deployment payment-api --replicas=5 -n production
# Git says replicas: 3, cluster now has replicas: 5
```
ArgoCD detects this on the next reconciliation cycle and marks the application as OutOfSync.

Mutating admission webhooks modify resources during creation. Common examples:

- **Istio sidecar injection**: Adds an istio-proxy container
- **Vault agent injection**: Adds vault-agent init containers
- **Resource defaulting**: Adds default CPU/memory requests

These mutations exist in the live state but not in Git, causing ArgoCD to report drift on every reconciliation.

**Fix**: Configure ArgoCD to ignore webhook-managed fields:

```
spec:
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jqPathExpressions:
    # Ignore Istio sidecar container
    - '.spec.template.spec.containers[] | select(.name == "istio-proxy")'
    # Ignore Istio init containers
    - '.spec.template.spec.initContainers[] | select(.name == "istio-init")'
```
If you use an HPA, it continuously adjusts the replica count based on metrics. The replica count in Git becomes stale almost immediately:

```
# Git says replicas: 3
# HPA adjusts to replicas: 7 based on CPU
# ArgoCD reports drift on replicas field
```
**Fix**: Ignore the replicas field when using HPA:

```
spec:
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas
```
Some Kubernetes controllers modify resource specifications. For example, the StatefulSet controller may reorder volume claims, or the Service controller may assign a ClusterIP:

```
# You defined:
spec:
  type: ClusterIP
# Kubernetes added:
spec:
  type: ClusterIP
  clusterIP: 10.96.45.123
  clusterIPs:
  - 10.96.45.123
```
**Fix**: Ignore fields owned by the relevant Kubernetes controller, or use server-side diff for defaulting and admission-controller mutations:

```
spec:
  ignoreDifferences:
  - group: "*"
    kind: "*"
    managedFieldsManagers:
    - kube-controller-manager
```
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cmd-params-cm
  namespace: argocd
data:
  controller.diff.server.side: "true"
```
Server-side diff runs a server-side apply dry run and compares the predicted live state with the actual live state, which can reduce false drift reports caused by defaulting and admission-controller mutations. Restart the `argocd-application-controller` after changing this controller-level setting.

If you use External Secrets Operator or Sealed Secrets, the actual Secret resource in the cluster will have different content than what is in Git (because Git contains the ExternalSecret or SealedSecret, not the plain Secret):

```
# Git has this:
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
# Cluster has this (created by External Secrets Operator):
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  ownerReferences:
  - apiVersion: external-secrets.io/v1beta1
    kind: ExternalSecret
    name: db-credentials
```
This is not really drift - it is expected behavior. ArgoCD manages the ExternalSecret resource, and the operator manages the resulting Secret.

ArgoCD can automatically correct detected drift through self-healing:

```
syncPolicy:
  automated:
    selfHeal: true
```
When drift is detected, ArgoCD performs a sync to bring the cluster back to the desired state. The automatic sync interval is controlled by `timeout.reconciliation`, which defaults to 120 seconds plus up to 60 seconds of jitter. With self-heal enabled, repeat sync attempts use the controller self-heal timeout, which defaults to 5 seconds.

Self-healing is powerful but can be disruptive if not configured carefully:

```
# Good: Self-heal with appropriate ignore rules
syncPolicy:
  automated:
    selfHeal: true
ignoreDifferences:
- group: apps
  kind: Deployment
  jsonPointers:
  - /spec/replicas  # Let HPA manage this
# Bad: Self-heal without ignore rules
# Will fight with HPA, mutating webhooks, etc.
syncPolicy:
  automated:
    selfHeal: true
```
Monitor drift patterns to understand your environment's health:

```
# Applications currently out of sync
count(argocd_app_info{sync_status="OutOfSync"})
# Sync operations over time, grouped by result
sum by (phase) (increase(argocd_app_sync_total[24h]))
# Failed or errored syncs over time
sum(increase(argocd_app_sync_total{phase=~"Failed|Error"}[24h]))
```
A healthy GitOps environment shows:

- Zero or near-zero OutOfSync applications (excluding those with manual sync policies)
- Decreasing OutOfSync duration over time as ignore rules are refined
- Low unexpected sync frequency (high frequency indicates something is fighting ArgoCD)

When you find an application in OutOfSync status, investigate the cause:

```
# See what is different
argocd app diff my-app
# Check the application's sync status details
argocd app get my-app --show-operation
# Look at the application's event history
kubectl get events -n argocd --field-selector involvedObject.name=my-app
```
Categorize each drift event:

- **Unauthorized change**: Someone modified a resource directly. Address through training and RBAC.
- **Controller mutation**: A Kubernetes controller modified a field. Add an ignore rule.
- **Webhook injection**: A mutating webhook added content. Add an ignore rule.
- **Legitimate override**: An HPA or operator manages the field. Add an ignore rule.

Configure ArgoCD notifications to alert on drift:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  trigger.on-sync-status-unknown: |
    - when: app.status.sync.status == 'OutOfSync'
      send: [drift-alert]
  template.drift-alert: |
    message: |
      Application {{.app.metadata.name}} has drifted from Git.
      Sync Status: {{.app.status.sync.status}}
      Health: {{.app.status.health.status}}
```
For comprehensive drift monitoring across your entire ArgoCD deployment, integrate with [OneUptime](https://oneuptime.com/blog/post/2026-02-26-argocd-alerts-outofsync-applications/view) to get immediate alerts when applications drift out of sync.

Configuration drift detection is one of the most valuable features of GitOps. ArgoCD detects drift through continuous reconciliation, comparing rendered manifests from Git against live cluster state using a semantic diff algorithm. Common drift sources include manual kubectl changes, mutating webhooks, HPA scaling, and controller mutations. Configure ignore rules for expected mutations, enable self-healing for automatic correction, and monitor drift metrics to track environmental health. The goal is to make all detected drift actionable - either it is a legitimate issue that needs correction, or it is an expected behavior that should be explicitly ignored.

---

## Research Cycle — 2026-11-09 12:05 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/DriftGuard/DriftGuard

### Web Summary: https://github.com/DriftGuard/DriftGuard

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
**Intelligent GitOps Configuration Drift Detection Engine**

DriftGuard is an intelligent GitOps configuration drift detection platform that continuously monitors Kubernetes resources for configuration drift by comparing live cluster states against desired states stored in Git repositories. It features enhanced state tracking, automatic resolution detection, and comprehensive drift analysis.

- **Enhanced Drift Detection**: Continuously monitors Kubernetes resources with intelligent drift classification
- **Drift Resolution Detection**: Automatically detects when drift is resolved and configuration matches Git again
- **State Management**: Tracks drift status (active/resolved/none) with timestamps and resolution messages
- **Git Integration**: Compares live state against Git-stored manifests with hash-based state tracking
- **Intelligent Classification**: Automatically classifies drift types (Scaling, VersionChange, ResourceChange, etc.)
- **Severity Assessment**: Assigns severity levels (low, medium, high) to detected drifts
- **MongoDB Storage**: Persistent storage of drift records with enhanced state tracking
- **REST API**: Comprehensive HTTP endpoints for querying drift records, status filtering, and statistics
- **Metrics & Monitoring**: Prometheus metrics and health checks
- **Enhanced Logging**: Detailed logging with emojis for drift detection and resolution events

Want to dive deeper into the configuration drift crisis and understand how DriftGuard solves real-world infrastructure challenges? Check out our comprehensive guide:

**[Learn More About DriftGuard](/DriftGuard/DriftGuard/blob/main/ABOUT.md)** - Discover the configuration drift crisis, understand GitOps vs InfraOps, explore real-world examples, and learn about DriftGuard's business value and architecture.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Kubernetes    │    │   Git Repo      │    │   DriftGuard    │
│   API Server    │    │   (Desired      │    │   Backend       │
│   (Live State)  │◄──►│   State)        │◄──►│   (Controller)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MongoDB       │    │   REST API      │
                       │   (Enhanced     │    │   (HTTP         │
                       │   Drift Records)│    │   Endpoints)    │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Prometheus    │    │   Health        │
                       │   Metrics       │    │   Checks        │
                       └─────────────────┘    └─────────────────┘
```
- **Go 1.21+**
- **MongoDB 4.4+**
- **Kubernetes cluster** (local or remote)
- **Git repository** with Kubernetes manifests
- **kubectl** configured to access your cluster

```
git clone <repository-url>
cd DriftGuard
```
```
# Create data directory
mkdir -p ~/data/db
# Start MongoDB (macOS/Linux)
sudo mongod --dbpath=~/data/db
# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```
Update the configuration file (`backend/configs/config.yaml`):

```
server:
  port: 8080
  read_timeout: 30s
  write_timeout: 30s
  idle_timeout: 60s
database:
  host: localhost
  port: 27017
  dbname: driftguard
  timeout: 10s
kubernetes:
  config_path: ""  # Leave empty for default kubeconfig
  context: ""
  namespaces: ["driftguard"]
  resources: ["deployments", "services", "configmaps", "secrets"]
  skip_system_namespaces: true
git:
  repository_url: "Add your Repo"
  default_branch: main
  clone_timeout: 5m
  pull_timeout: 2m
drift_detection:
  interval: 30s
  enable_periodic: true
```
```
# Create a dummy Git repository for testing
mkdir -p dummy-k8s-repo
cd dummy-k8s-repo
git init
# Create test Kubernetes manifests
cat > test-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  namespace: driftguard
  labels:
    app: nginx
    environment: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.23
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        env:
        - name: NGINX_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: driftguard
  labels:
    app: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: driftguard
data:
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
  environment: "production"
  version: "1.0.0"
EOF
# Commit the manifests
git add test-deployment.yaml
git commit -m "Initial Kubernetes manifests"
```
`kubectl create namespace driftguard````
cd backend
go run cmd/controller/main.go --config=configs/config.yaml
```
```
# Check if DriftGuard is running
curl http://localhost:8080/health
# Expected response:
# {"status":"healthy","message":"Service is running","time":"2025-01-15T10:30:00Z"}
```
```
# Apply the manifests from Git
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Verify resources are created
kubectl get all -n driftguard
```
```
# Trigger manual drift analysis
curl -X POST http://localhost:8080/api/v1/analyze
# Expected response:
# {"message":"Drift analysis triggered successfully","status":"started"}
```
```
# Wait a few seconds, then check drift records
sleep 5
curl http://localhost:8080/api/v1/drift-records
# You should see records with drift_detected: false initially
```
```
# Scale the deployment to create drift
kubectl scale deployment nginx-app -n driftguard --replicas=3
# Verify the change
kubectl get deployment nginx-app -n driftguard
```
```
# Trigger drift analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for drift detection
sleep 5
curl http://localhost:8080/api/v1/drift-records/active
# You should now see active drift records
```
```
# Scale back to original state
kubectl scale deployment nginx-app -n driftguard --replicas=2
# Or re-apply the Git manifest
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Trigger analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for resolution
sleep 5
curl http://localhost:8080/api/v1/drift-records/resolved
```
```
# Test image change drift
kubectl set image deployment/nginx-app nginx=nginx:1.24 -n driftguard
# Test environment variable drift
kubectl set env deployment/nginx-app NGINX_ENV=staging -n driftguard
# Test resource drift
kubectl patch deployment nginx-app -n driftguard -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"memory":"128Mi"}}}]}}}}'
# Trigger analysis after each change
curl -X POST http://localhost:8080/api/v1/analyze
```
```
# Get comprehensive statistics
curl http://localhost:8080/api/v1/statistics
# Expected response includes:
# - total_records
# - active_drift
# - resolved_drift
# - no_drift
# - active_percentage
# - resolved_percentage
```
```
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
# Get specific resource drift
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/health` | Basic health check | 
| `GET` | `/ready` | Readiness check | 
| `GET` | `/metrics` | Prometheus metrics | 

| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/api/v1/drift-records` | List all drift records | 
| `GET` | `/api/v1/drift-records/:resourceId` | Get specific drift record | 
| `GET` | `/api/v1/drift-records/active` | Get active drift records | 
| `GET` | `/api/v1/drift-records/resolved` | Get resolved drift records | 
| `GET` | `/api/v1/statistics` | Get drift statistics | 
| `POST` | `/api/v1/analyze` | Trigger manual drift analysis | 

**List Drift Records:**

```
# Get all drift records
curl http://localhost:8080/api/v1/drift-records
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
```
**Get Specific Record:**

```
# Get drift record for a specific resource
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
Resources are identified using the format: `kind:namespace:name`

The system tracks drift status with three states:

- **`active`**: Drift is currently detected and active
- **`resolved`**: Drift was previously detected but has been resolved
- **`none`**: No drift detected

The system automatically classifies drifts into categories:

- **Scaling**: Replica count changes
- **VersionChange**: Container image changes
- **ResourceChange**: CPU/memory resource changes
- **ConfigurationChange**: Environment variable changes
- **LabelChange**: Label modifications
- **AnnotationChange**: Annotation modifications
- **PortChange**: Port configuration changes
- **VolumeChange**: Volume mount changes
- **SecretChange**: Secret reference changes
- **ConfigMapChange**: ConfigMap reference changes

- **High**: Image changes, secret changes, significant scaling (>50%)
- **Medium**: Minor scaling, environment variables, ports, volumes
- **Low**: Labels, annotations, other metadata

The system provides comprehensive drift statistics:

```
{
  "statistics": {
    "total_records": 25,
    "active_drift": 3,
    "resolved_drift": 15,
    "no_drift": 7,
    "recent_active_drift": 1,
    "recent_resolutions": 2,
    "active_percentage": 12.0,
    "resolved_percentage": 60.0
  }
}
```
- `config_path`: Path to kubeconfig file
- `context`: Kubernetes context to use
- `namespaces`: List of namespaces to monitor
- `resources`: List of resource types to monitor
- `skip_system_namespaces`: Skip system namespaces

- `repository_url`: Git repository URL
- `default_branch`: Branch to monitor
- `clone_timeout`: Timeout for repository cloning
- `pull_timeout`: Timeout for pulling updates

- `interval`: Periodic analysis interval
- `enable_periodic`: Enable periodic drift detection

1. **MongoDB Connection Failed**
\# Check if MongoDB is running ps aux | grep mongod # Start MongoDB if not running sudo mongod --dbpath=\~/data/db
2. **Kubernetes Connection Failed**
\# Check kubectl configuration kubectl config current-context # Test cluster connection kubectl get nodes
3. **Git Repository Access Failed**
\# Check Git repository URL in config # Ensure repository is accessible git ls-remote \<repository-url>
4. **Port Already in Use**
\# Check if port 8080 is in use lsof -i :8080 # Kill process or change port in config

DriftGuard uses structured logging with emojis:

- 🚀 System startup
- ⚠️ Drift detected
- ✅ Drift resolved
- 🔄 Drift continued
- 📊 Analysis completed

```
# Build the container
docker build -t driftguard:latest backend/
# Run with environment variables
docker run -d \
  -p 8080:8080 \
  -e MONGODB_HOST=your-mongodb-host \
  -e KUBECONFIG=/path/to/kubeconfig \
  driftguard:latest
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: driftguard
  namespace: driftguard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: driftguard
  template:
    metadata:
      labels:
        app: driftguard
    spec:
      containers:
      - name: driftguard
        image: driftguard:latest
        ports:
        - containerPort: 8080
        env:
        - name: MONGODB_HOST
          value: "mongodb-service"
        volumeMounts:
        - name: kubeconfig
          mountPath: /root/.kube
          readOnly: true
      volumes:
      - name: kubeconfig
        secret:
          secretName: driftguard-kubeconfig
```
We welcome contributions! Please see our [Contributing Guidelines](/DriftGuard/DriftGuard/blob/main/CONTRIBUTING.md) for details.

This project is licensed under the MIT License - see the [LICENSE](/DriftGuard/DriftGuard/blob/main/LICENSE.md) file for details.

For questions, feature requests, or contributions, please open an issue in this repository.

---

### Source: https://github.com/Elshayib

## Popular repositories Loading

1. 
                [omarchy-oligarchy-theme](/Elshayib/omarchy-oligarchy-theme)
              omarchy-oligarchy-theme Public A dark medieval-keep theme for Omarchy: iron-grey stone, antique gold windows, moonlight text. Elite capital. Public code.

Something went wrong, please refresh the page to try again.

If the problem persists, check the [GitHub status page](https://www.githubstatus.com/)
          or [contact support](/contact).

---

### Source: https://github.com/Pratik1566/config-drift-detector

An AI-assisted configuration drift detection platform that identifies servers whose configurations differ from an approved fleet baseline, evaluates potential risks, and explains detected changes using a locally running open-weight AI model.

- **Configuration Drift Detection:** Identifies differences between approved baseline configurations and current configurations.
- **Fleet-Based Scanning:** Supports configuration analysis across multiple server profiles.
- **Risk Scoring:** Evaluates detected changes using predefined security rules and risk scores.
- **AI-Powered Explanations:** Uses a local Qwen model through Ollama to explain detected drift and suggest possible fixes.
- **Interactive Dashboard:** Displays configuration findings and scan results through Streamlit.
- **Scan Reports:** Saves scan results for later review and analysis.
- **Automated Testing:** Tests whether deliberately introduced configuration changes are detected correctly.
- **Modular Architecture:** Separates data collection, detection, risk rules, AI explanations, and dashboard components.

- **Programming Language:** Python
- **Dashboard:** Streamlit
- **Local AI Runtime:** Ollama
- **AI Model:** Qwen3 4B (or a supported fallback model)
- **Configuration Data:** JSON and other explicitly supported configuration formats
- **Testing:** Python testing tools

1. Install Python 3.11 or later.
2. Install Git.
3. Install Ollama.
4. Ensure the selected Qwen model is supported by your Ollama installation.

```
git clone <repo-url>
cd config-drift-detector
```
Replace `<repo-url>` with your repository URL.

On Windows PowerShell:

```
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, follow the Python virtual-environment instructions for your operating system.

`python -m pip install -r requirements.txt`
For the primary model:

`ollama pull qwen3:4b`
Optional smaller fallback model:

`ollama pull qwen3:1.7b`
Confirm that the model is available:

`ollama list`
The fallback model must also be configured in the application if the code is expected to use it automatically.

From the project root directory, run:

`streamlit run app/app.py`
Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

1. **Load Configuration Data:** Read the available configuration data and approved baseline.
2. **Parse Settings:** Extract supported settings from the input using the appropriate parser.
3. **Compare Configurations:** Identify changed, missing, and newly added settings.
4. **Evaluate Risks:** Apply predefined rules to assess the potential impact of detected changes.
5. **Generate Explanations:** Use the local AI model to explain findings and suggest possible corrections.
6. **Display Results:** Present findings through the dashboard.
7. **Save Reports:** Store scan results for future review and comparison.

```
config-drift-detector/
├── fleet/
│   ├── generate_fleet.py
│   └── inject_drift.py
├── collector/
│   └── ...
├── engine/
│   └── ...
├── rules/
│   └── risky_settings.json
├── ai/
│   ├── mock.py
│   └── ...
├── app/
│   └── app.py
├── tests/
│   └── ...
├── docs/
│   └── samples/
├── requirements.txt
└── README.md
```
This is the intended project structure. Update the tree to reflect the files actually present in the repository.

- **Model:** Qwen3 4B
- **Runtime:** Ollama
- **Execution:** Locally on the user's machine
- **Parameters:** Approximately 4 billion
- **Fallback:** Qwen3 1.7B, if configured and supported by the application
- **Model License:** Verify the exact model's license on its official model page before redistribution or deployment.

Official references:

- Ollama: [https://ollama.com/](https://ollama.com/)
- Qwen3 4B: [https://ollama.com/library/qwen3:4b](https://ollama.com/library/qwen3:4b)
- Qwen3 1.7B: [https://ollama.com/library/qwen3:1.7b](https://ollama.com/library/qwen3:1.7b)

- Scan only systems and configuration files you are authorized to assess.
- Treat configuration files as potentially sensitive because they may contain internal infrastructure details.
- Avoid exposing credentials, private keys, tokens, or other secrets in scan reports or AI prompts.
- Review AI-generated explanations and recommendations before applying any changes.
- Do not interpret a risk score as a probability that an attack will occur.
- Unsupported directives and parsing limitations should be reported clearly.
- Do not automatically modify production configurations without an authorized, tested change-management process.

- Detection accuracy depends on the quality of the approved baseline, parsing logic, and security rules.
- Different configuration formats require their own parsers and validation rules.
- Some configurations contain defaults, included files, conditional sections, or other behavior that a basic parser may not fully interpret.
- AI-generated explanations may be incomplete or incorrect and should be validated.
- Features such as Docker collection, multi-server scanning, and automated drift injection are available only when their corresponding modules are implemented.

Run the project's tests using the test framework configured in the repository.

If the project uses pytest, install it if necessary and run:

`python -m pytest`
Tests should cover:

- Unchanged configurations.
- Changed settings.
- Missing settings.
- Newly added settings.
- Risk-rule evaluation.
- Invalid or unsupported configuration input.
- AI response validation and fallback behavior.

1. Create a separate feature branch. git checkout -b feature/your-feature-name
2. Make changes within your assigned files or modules.
3. Run the relevant tests.
4. Commit your changes. git add . git commit -m "Add your feature description"
5. Push your branch. git push -u origin feature/your-feature-name
6. Open a pull request for review.

Avoid modifying the same files as another team member without coordinating first.

Contributions are welcome. Please use feature branches, test changes before submitting them, and describe the purpose and behavior of your changes in the pull request.

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Research Cycle — 2026-11-09 18:05 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/Coding-Dev-Tools/configdrift

Keep configurations consistent across all environments, automatically. ConfigDrift compares configs, flags drift, and reports compliance violations before they cause incidents.

⭐ **Star this repo** if you manage multi-environment configs — it helps other devs find ConfigDrift!

Real-world scenarios:

- **Multi-environment compliance**: Ensure staging and prod configs are identical before every deploy
- **Secrets audit**: Detect env vars that exist in one environment but are missing in another
- **CI/CD gating**: Block PRs that introduce config drift across environments
- **Incident prevention**: Catch a changed database endpoint before it causes a production outage

ConfigDrift is **not published to public PyPI**. Install from the self-hosted index, a direct GitHub install, or via Homebrew/Scoop (below).

```
# Install directly from GitHub (recommended)
pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
```
Editable install for development:

`pip install -e ".[dev]"`
Then run: `configdrift --help`

Compare two config files:

`configdrift check dev.yaml prod.yaml`
Scan entire directories as environments:

`configdrift scan ./config/dev ./config/staging ./config/prod`
Use a config file to define environments:

```
configdrift init
configdrift scan --config .configdrift.yaml
```
`configdrift check <file1> <file2> [--output table|json|silent] [--baseline dev] [--target prod]`
Output formats:

- `table` (default): Rich colored table output
- `json`: Machine-readable JSON for CI integration
- `silent`: Exit code only (0 = no breaking drift, 1 = breaking drift found)

`configdrift scan ./dev ./staging ./prod --baseline dev`
Scans all config files in each directory, merges them, and compares against a baseline environment.

`configdrift init .`
Creates `.configdrift.yaml` in the specified directory.

Use `--output silent` for CI gating:

`configdrift check dev.yaml prod.yaml --output silent || echo "Drift detected!"````
- name: Detect config drift
  run: |
    pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
    configdrift check ./config/staging/app.yaml ./config/prod/app.yaml --output silent
```
- **Exit code 1 with no output**: use `--output table` to inspect drift details.
- **TOML parsing errors on Python \< 3.11**: install `tomli` and `tomli-w` or use Python 3.11+.
- **Large config scans are slow**: narrow the scan to changed files or a single directory.
- **Unexpected breaking drift**: review severity rules in the project settings; `database*` and `auth*` keys are flagged as breaking by default.

| Format | Extension | Notes | 
|---|---|---|
| YAML | `.yaml`, `.yml` | Full nested structure support | 
| JSON | `.json` | Nested flattening | 
| TOML | `.toml` | Python 3.11+ native | 
| .env | `.env` | `KEY=VALUE` format | 

- **Info**: Non-critical value changes
- **Warning**: Added or removed optional keys
- **Breaking**: Changes to critical keys (`database*`, `auth*`, `api_key*`, `secret*`, `password*`, `token*`, `endpoint*`)

```
# Install with dev dependencies
pip install -e ".[dev]"
# Run tests
pytest
# Run with coverage
pytest --cov=configdrift
```
ConfigDrift is one of 11 tools in the Revenue Holdings suite. One license covers all CLI tools.

| Plan | Price | Best For | 
|---|---|---|
| **Free** | $0 | Individual devs, OSS — CLI only, 1 env pair | 
| **ConfigDrift Individual** | **$15/mo** ($12 billed annually) | Professional devs — unlimited environments, custom rules | 
| **Suite (all 11 tools)** | **$49/mo** ($39 billed annually) | Full Revenue Holdings toolkit — 40% savings | 
| **Team** | **$79/mo** ($63 billed annually) | Up to 5 devs — drift history, Slack alerts, priority support | 
| **Enterprise** | Custom | SSO, RBAC, compliance reports, dedicated support | 

🔹 **No lock-in**: CLI works fully offline on the free tier — no telemetry, no phone-home.
🔹 **Annual billing**: Save 20%.

| Feature | Free | ConfigDrift | Suite | Team | Enterprise | 
|---|---|---|---|---|---|
| CLI: check, scan | ✓ | ✓ | ✓ | ✓ | ✓ | 
| Unlimited environments | — | ✓ | ✓ | ✓ | ✓ | 
| Custom rules / policies | — | ✓ | ✓ | ✓ | ✓ | 
| Drift history / audit trail | — | — | — | ✓ | ✓ | 
| Slack / webhook alerts | — | — | — | ✓ | ✓ | 
| Compliance reports | — | — | — | — | ✓ | 
| RBAC | — | — | — | — | ✓ | 
| SSO / SAML / OIDC | — | — | — | — | ✓ | 
| Priority support | Community | 24h | 24h | 8h | Dedicated | 

<sub>Part of [Revenue Holdings](https://coding-dev-tools.github.io/devforge/) — CLI tools built by autonomous AI.</sub>

MIT

`npm test  # runs: node --test tests/`

---

### Source: https://github.com/DriftGuard/DriftGuard

### Web Summary: https://github.com/DriftGuard/DriftGuard

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
**Intelligent GitOps Configuration Drift Detection Engine**

DriftGuard is an intelligent GitOps configuration drift detection platform that continuously monitors Kubernetes resources for configuration drift by comparing live cluster states against desired states stored in Git repositories. It features enhanced state tracking, automatic resolution detection, and comprehensive drift analysis.

- **Enhanced Drift Detection**: Continuously monitors Kubernetes resources with intelligent drift classification
- **Drift Resolution Detection**: Automatically detects when drift is resolved and configuration matches Git again
- **State Management**: Tracks drift status (active/resolved/none) with timestamps and resolution messages
- **Git Integration**: Compares live state against Git-stored manifests with hash-based state tracking
- **Intelligent Classification**: Automatically classifies drift types (Scaling, VersionChange, ResourceChange, etc.)
- **Severity Assessment**: Assigns severity levels (low, medium, high) to detected drifts
- **MongoDB Storage**: Persistent storage of drift records with enhanced state tracking
- **REST API**: Comprehensive HTTP endpoints for querying drift records, status filtering, and statistics
- **Metrics & Monitoring**: Prometheus metrics and health checks
- **Enhanced Logging**: Detailed logging with emojis for drift detection and resolution events

Want to dive deeper into the configuration drift crisis and understand how DriftGuard solves real-world infrastructure challenges? Check out our comprehensive guide:

**[Learn More About DriftGuard](/DriftGuard/DriftGuard/blob/main/ABOUT.md)** - Discover the configuration drift crisis, understand GitOps vs InfraOps, explore real-world examples, and learn about DriftGuard's business value and architecture.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Kubernetes    │    │   Git Repo      │    │   DriftGuard    │
│   API Server    │    │   (Desired      │    │   Backend       │
│   (Live State)  │◄──►│   State)        │◄──►│   (Controller)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MongoDB       │    │   REST API      │
                       │   (Enhanced     │    │   (HTTP         │
                       │   Drift Records)│    │   Endpoints)    │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Prometheus    │    │   Health        │
                       │   Metrics       │    │   Checks        │
                       └─────────────────┘    └─────────────────┘
```
- **Go 1.21+**
- **MongoDB 4.4+**
- **Kubernetes cluster** (local or remote)
- **Git repository** with Kubernetes manifests
- **kubectl** configured to access your cluster

```
git clone <repository-url>
cd DriftGuard
```
```
# Create data directory
mkdir -p ~/data/db
# Start MongoDB (macOS/Linux)
sudo mongod --dbpath=~/data/db
# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```
Update the configuration file (`backend/configs/config.yaml`):

```
server:
  port: 8080
  read_timeout: 30s
  write_timeout: 30s
  idle_timeout: 60s
database:
  host: localhost
  port: 27017
  dbname: driftguard
  timeout: 10s
kubernetes:
  config_path: ""  # Leave empty for default kubeconfig
  context: ""
  namespaces: ["driftguard"]
  resources: ["deployments", "services", "configmaps", "secrets"]
  skip_system_namespaces: true
git:
  repository_url: "Add your Repo"
  default_branch: main
  clone_timeout: 5m
  pull_timeout: 2m
drift_detection:
  interval: 30s
  enable_periodic: true
```
```
# Create a dummy Git repository for testing
mkdir -p dummy-k8s-repo
cd dummy-k8s-repo
git init
# Create test Kubernetes manifests
cat > test-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  namespace: driftguard
  labels:
    app: nginx
    environment: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.23
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        env:
        - name: NGINX_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: driftguard
  labels:
    app: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: driftguard
data:
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
  environment: "production"
  version: "1.0.0"
EOF
# Commit the manifests
git add test-deployment.yaml
git commit -m "Initial Kubernetes manifests"
```
`kubectl create namespace driftguard````
cd backend
go run cmd/controller/main.go --config=configs/config.yaml
```
```
# Check if DriftGuard is running
curl http://localhost:8080/health
# Expected response:
# {"status":"healthy","message":"Service is running","time":"2025-01-15T10:30:00Z"}
```
```
# Apply the manifests from Git
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Verify resources are created
kubectl get all -n driftguard
```
```
# Trigger manual drift analysis
curl -X POST http://localhost:8080/api/v1/analyze
# Expected response:
# {"message":"Drift analysis triggered successfully","status":"started"}
```
```
# Wait a few seconds, then check drift records
sleep 5
curl http://localhost:8080/api/v1/drift-records
# You should see records with drift_detected: false initially
```
```
# Scale the deployment to create drift
kubectl scale deployment nginx-app -n driftguard --replicas=3
# Verify the change
kubectl get deployment nginx-app -n driftguard
```
```
# Trigger drift analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for drift detection
sleep 5
curl http://localhost:8080/api/v1/drift-records/active
# You should now see active drift records
```
```
# Scale back to original state
kubectl scale deployment nginx-app -n driftguard --replicas=2
# Or re-apply the Git manifest
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Trigger analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for resolution
sleep 5
curl http://localhost:8080/api/v1/drift-records/resolved
```
```
# Test image change drift
kubectl set image deployment/nginx-app nginx=nginx:1.24 -n driftguard
# Test environment variable drift
kubectl set env deployment/nginx-app NGINX_ENV=staging -n driftguard
# Test resource drift
kubectl patch deployment nginx-app -n driftguard -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"memory":"128Mi"}}}]}}}}'
# Trigger analysis after each change
curl -X POST http://localhost:8080/api/v1/analyze
```
```
# Get comprehensive statistics
curl http://localhost:8080/api/v1/statistics
# Expected response includes:
# - total_records
# - active_drift
# - resolved_drift
# - no_drift
# - active_percentage
# - resolved_percentage
```
```
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
# Get specific resource drift
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/health` | Basic health check | 
| `GET` | `/ready` | Readiness check | 
| `GET` | `/metrics` | Prometheus metrics | 

| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/api/v1/drift-records` | List all drift records | 
| `GET` | `/api/v1/drift-records/:resourceId` | Get specific drift record | 
| `GET` | `/api/v1/drift-records/active` | Get active drift records | 
| `GET` | `/api/v1/drift-records/resolved` | Get resolved drift records | 
| `GET` | `/api/v1/statistics` | Get drift statistics | 
| `POST` | `/api/v1/analyze` | Trigger manual drift analysis | 

**List Drift Records:**

```
# Get all drift records
curl http://localhost:8080/api/v1/drift-records
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
```
**Get Specific Record:**

```
# Get drift record for a specific resource
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
Resources are identified using the format: `kind:namespace:name`

The system tracks drift status with three states:

- **`active`**: Drift is currently detected and active
- **`resolved`**: Drift was previously detected but has been resolved
- **`none`**: No drift detected

The system automatically classifies drifts into categories:

- **Scaling**: Replica count changes
- **VersionChange**: Container image changes
- **ResourceChange**: CPU/memory resource changes
- **ConfigurationChange**: Environment variable changes
- **LabelChange**: Label modifications
- **AnnotationChange**: Annotation modifications
- **PortChange**: Port configuration changes
- **VolumeChange**: Volume mount changes
- **SecretChange**: Secret reference changes
- **ConfigMapChange**: ConfigMap reference changes

- **High**: Image changes, secret changes, significant scaling (>50%)
- **Medium**: Minor scaling, environment variables, ports, volumes
- **Low**: Labels, annotations, other metadata

The system provides comprehensive drift statistics:

```
{
  "statistics": {
    "total_records": 25,
    "active_drift": 3,
    "resolved_drift": 15,
    "no_drift": 7,
    "recent_active_drift": 1,
    "recent_resolutions": 2,
    "active_percentage": 12.0,
    "resolved_percentage": 60.0
  }
}
```
- `config_path`: Path to kubeconfig file
- `context`: Kubernetes context to use
- `namespaces`: List of namespaces to monitor
- `resources`: List of resource types to monitor
- `skip_system_namespaces`: Skip system namespaces

- `repository_url`: Git repository URL
- `default_branch`: Branch to monitor
- `clone_timeout`: Timeout for repository cloning
- `pull_timeout`: Timeout for pulling updates

- `interval`: Periodic analysis interval
- `enable_periodic`: Enable periodic drift detection

1. **MongoDB Connection Failed**
\# Check if MongoDB is running ps aux | grep mongod # Start MongoDB if not running sudo mongod --dbpath=\~/data/db
2. **Kubernetes Connection Failed**
\# Check kubectl configuration kubectl config current-context # Test cluster connection kubectl get nodes
3. **Git Repository Access Failed**
\# Check Git repository URL in config # Ensure repository is accessible git ls-remote \<repository-url>
4. **Port Already in Use**
\# Check if port 8080 is in use lsof -i :8080 # Kill process or change port in config

DriftGuard uses structured logging with emojis:

- 🚀 System startup
- ⚠️ Drift detected
- ✅ Drift resolved
- 🔄 Drift continued
- 📊 Analysis completed

```
# Build the container
docker build -t driftguard:latest backend/
# Run with environment variables
docker run -d \
  -p 8080:8080 \
  -e MONGODB_HOST=your-mongodb-host \
  -e KUBECONFIG=/path/to/kubeconfig \
  driftguard:latest
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: driftguard
  namespace: driftguard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: driftguard
  template:
    metadata:
      labels:
        app: driftguard
    spec:
      containers:
      - name: driftguard
        image: driftguard:latest
        ports:
        - containerPort: 8080
        env:
        - name: MONGODB_HOST
          value: "mongodb-service"
        volumeMounts:
        - name: kubeconfig
          mountPath: /root/.kube
          readOnly: true
      volumes:
      - name: kubeconfig
        secret:
          secretName: driftguard-kubeconfig
```
We welcome contributions! Please see our [Contributing Guidelines](/DriftGuard/DriftGuard/blob/main/CONTRIBUTING.md) for details.

This project is licensed under the MIT License - see the [LICENSE](/DriftGuard/DriftGuard/blob/main/LICENSE.md) file for details.

For questions, feature requests, or contributions, please open an issue in this repository.

---

### Source: https://github.com/Pratik1566/config-drift-detector

An AI-assisted configuration drift detection platform that identifies servers whose configurations differ from an approved fleet baseline, evaluates potential risks, and explains detected changes using a locally running open-weight AI model.

- **Configuration Drift Detection:** Identifies differences between approved baseline configurations and current configurations.
- **Fleet-Based Scanning:** Supports configuration analysis across multiple server profiles.
- **Risk Scoring:** Evaluates detected changes using predefined security rules and risk scores.
- **AI-Powered Explanations:** Uses a local Qwen model through Ollama to explain detected drift and suggest possible fixes.
- **Interactive Dashboard:** Displays configuration findings and scan results through Streamlit.
- **Scan Reports:** Saves scan results for later review and analysis.
- **Automated Testing:** Tests whether deliberately introduced configuration changes are detected correctly.
- **Modular Architecture:** Separates data collection, detection, risk rules, AI explanations, and dashboard components.

- **Programming Language:** Python
- **Dashboard:** Streamlit
- **Local AI Runtime:** Ollama
- **AI Model:** Qwen3 4B (or a supported fallback model)
- **Configuration Data:** JSON and other explicitly supported configuration formats
- **Testing:** Python testing tools

1. Install Python 3.11 or later.
2. Install Git.
3. Install Ollama.
4. Ensure the selected Qwen model is supported by your Ollama installation.

```
git clone <repo-url>
cd config-drift-detector
```
Replace `<repo-url>` with your repository URL.

On Windows PowerShell:

```
python -m venv venv
venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, follow the Python virtual-environment instructions for your operating system.

`python -m pip install -r requirements.txt`
For the primary model:

`ollama pull qwen3:4b`
Optional smaller fallback model:

`ollama pull qwen3:1.7b`
Confirm that the model is available:

`ollama list`
The fallback model must also be configured in the application if the code is expected to use it automatically.

From the project root directory, run:

`streamlit run app/app.py`
Streamlit will display a local URL in the terminal. Open that URL in your browser to access the dashboard.

1. **Load Configuration Data:** Read the available configuration data and approved baseline.
2. **Parse Settings:** Extract supported settings from the input using the appropriate parser.
3. **Compare Configurations:** Identify changed, missing, and newly added settings.
4. **Evaluate Risks:** Apply predefined rules to assess the potential impact of detected changes.
5. **Generate Explanations:** Use the local AI model to explain findings and suggest possible corrections.
6. **Display Results:** Present findings through the dashboard.
7. **Save Reports:** Store scan results for future review and comparison.

```
config-drift-detector/
├── fleet/
│   ├── generate_fleet.py
│   └── inject_drift.py
├── collector/
│   └── ...
├── engine/
│   └── ...
├── rules/
│   └── risky_settings.json
├── ai/
│   ├── mock.py
│   └── ...
├── app/
│   └── app.py
├── tests/
│   └── ...
├── docs/
│   └── samples/
├── requirements.txt
└── README.md
```
This is the intended project structure. Update the tree to reflect the files actually present in the repository.

- **Model:** Qwen3 4B
- **Runtime:** Ollama
- **Execution:** Locally on the user's machine
- **Parameters:** Approximately 4 billion
- **Fallback:** Qwen3 1.7B, if configured and supported by the application
- **Model License:** Verify the exact model's license on its official model page before redistribution or deployment.

Official references:

- Ollama: [https://ollama.com/](https://ollama.com/)
- Qwen3 4B: [https://ollama.com/library/qwen3:4b](https://ollama.com/library/qwen3:4b)
- Qwen3 1.7B: [https://ollama.com/library/qwen3:1.7b](https://ollama.com/library/qwen3:1.7b)

- Scan only systems and configuration files you are authorized to assess.
- Treat configuration files as potentially sensitive because they may contain internal infrastructure details.
- Avoid exposing credentials, private keys, tokens, or other secrets in scan reports or AI prompts.
- Review AI-generated explanations and recommendations before applying any changes.
- Do not interpret a risk score as a probability that an attack will occur.
- Unsupported directives and parsing limitations should be reported clearly.
- Do not automatically modify production configurations without an authorized, tested change-management process.

- Detection accuracy depends on the quality of the approved baseline, parsing logic, and security rules.
- Different configuration formats require their own parsers and validation rules.
- Some configurations contain defaults, included files, conditional sections, or other behavior that a basic parser may not fully interpret.
- AI-generated explanations may be incomplete or incorrect and should be validated.
- Features such as Docker collection, multi-server scanning, and automated drift injection are available only when their corresponding modules are implemented.

Run the project's tests using the test framework configured in the repository.

If the project uses pytest, install it if necessary and run:

`python -m pytest`
Tests should cover:

- Unchanged configurations.
- Changed settings.
- Missing settings.
- Newly added settings.
- Risk-rule evaluation.
- Invalid or unsupported configuration input.
- AI response validation and fallback behavior.

1. Create a separate feature branch. git checkout -b feature/your-feature-name
2. Make changes within your assigned files or modules.
3. Run the relevant tests.
4. Commit your changes. git add . git commit -m "Add your feature description"
5. Push your branch. git push -u origin feature/your-feature-name
6. Open a pull request for review.

Avoid modifying the same files as another team member without coordinating first.

Contributions are welcome. Please use feature branches, test changes before submitting them, and describe the purpose and behavior of your changes in the pull request.

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Research Cycle — 2026-11-10 06:05 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/Elshayib

## Popular repositories Loading

1. 
                [omarchy-oligarchy-theme](/Elshayib/omarchy-oligarchy-theme)
              omarchy-oligarchy-theme Public A dark medieval-keep theme for Omarchy: iron-grey stone, antique gold windows, moonlight text. Elite capital. Public code.

Something went wrong, please refresh the page to try again.

If the problem persists, check the [GitHub status page](https://www.githubstatus.com/)
          or [contact support](/contact).

---

### Source: https://github.com/janinelurenana

**Security Detection · Network Engineering · Automation**

Polytechnic University of the Philippines

I build **detection systems and network infrastructure that hold under real conditions**, not just controlled labs.

My work focuses on:

- Translating ambiguous security problems into **repeatable detection logic**
- Designing networks with **enforced boundaries and validated failover**
- Automating infrastructure with **state verification, not just deployment**

Most student projects stop at *“it works.”*
Mine are built to answer:

*Does it still work under failure, scale, and misconfiguration?*

- Build **SIEM-style detection logic** from raw logs (not dashboards on clean data)
- Design **segmented enterprise networks** with measurable resilience
- Implement **network-as-code pipelines** with drift detection
- Develop **risk-based anomaly detection systems** using SQL correlation logic

**Repo:** [https://github.com/janinelurenana/cloud-security-analyzer](https://github.com/janinelurenana/cloud-security-analyzer)

Built a modular detection pipeline that processes CloudTrail-style logs and produces **severity-ranked, MITRE ATT&CK–mapped findings**.

- 8 detection rules across 26 simulated cloud resources
- 43 validated findings surfaced via Streamlit
- Config-driven thresholds (no hardcoded detection logic)

**What matters:**

- Detection logic is **decoupled from thresholds** → mirrors real SIEM rule design
- Outputs are **explicitly mapped to attacker behavior**, not generic alerts

**Mapped Techniques:**

- T1078 — Valid Accounts / Privilege Abuse
- T1098 — Account Manipulation
- T1110 — Brute Force

**Repo:** [https://github.com/janinelurenana/Enterprise-Campus-Network-Architecture](https://github.com/janinelurenana/Enterprise-Campus-Network-Architecture)

Designed and validated a segmented campus network with **enforced least privilege and high availability**.

- VLAN segmentation: IT, HR, Guest, DMZ
- ACL-enforced zone isolation (not theoretical)
- FortiGate Active–Passive HA

**Validation, not assumption:**

- \~1 second failover convergence
- Session persistence during link failure

**Additional work:**

- Documented HSRP convergence behavior (5–10s)
- Extending to multi-site OSPF + IPsec VPN

**Repo:** [https://github.com/janinelurenana/declarative-network-provisioning](https://github.com/janinelurenana/declarative-network-provisioning)

Built a **multi-vendor network-as-code pipeline**:

YAML → Jinja2 → Netmiko → Device Configuration → State Verification

**Key capability:**

- Drift detection is **bidirectional**
  - Detects missing intended config
  - Detects unauthorized changes

**Why this matters:**
Most automation scripts push configs.
This enforces **state integrity**, which is what production environments actually need.

**Repo:** [https://github.com/janinelurenana/banking-fraud-detection-analytics](https://github.com/janinelurenana/banking-fraud-detection-analytics)

Built a transaction analysis system using **weighted anomaly scoring**, not simple thresholds.

- 5,500 transactions across 200 accounts
- Multi-table joins with CASE-based scoring

**Detection includes:**

- Velocity anomalies
- Geographic inconsistencies
- High-value outliers

**Key insight:**
Single signals don’t trigger alerts—**combined risk does**
→ aligns with real SIEM correlation logic

**Output:**

- Star schema → Power BI dashboards
- Geographic threat clustering for interpretability

**Security**

- Log Analysis · MITRE ATT&CK
- IAM Auditing · CSPM
- Burp Suite (SQLi) · Nmap

**Networking**

- GNS3 · FortiGate HA
- OSPF · VLANs · ACLs
- IPsec VPN · HSRP / VRRP
- NAT · STP

**Programming / Automation**

- Python · SQL
- Jinja2 · YAML
- Pandas · Streamlit · Netmiko

**Tooling**

- Power BI · MySQL
- AWS CloudTrail
- Kali Linux
- Git / GitHub

- Multi-site network simulation (OSPF + IPsec WAN)
- Detection engineering aligned with SOC workflows via TryHackMe
- CompTIA Security+ (target: Q3 2026)

Open to **junior-level roles**, not just internships:

- Security Analyst
- Network Engineer
- Detection Engineer (entry/junior)

---

### Source: https://github.com/SiteQ8/ConduitShield

### Web Summary: https://github.com/SiteQ8/ConduitShield

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
**One platform. Three modes. Full OT lifecycle security.**

[Live Dashboard](https://siteq8.github.io/ConduitShield) · [Features](#features) · [Architecture](#architecture) · [Standards](#standards-alignment) · [Quick Start](#quick-start)

APIs are the #1 attack vector in IT. In OT, the attack surface is the **protocol layer** — Modbus writes, S7comm uploads, DNP3 commands — where a single unauthorized change can halt a plant or endanger safety.

Most cybersecurity tools are built for IT and retrofitted for OT. They actively scan, ignore zones and conduits, treat the plant like a flat LAN, and have no awareness of operational safety.

ConduitShield is **built for OT from the ground up**:

- **Passive-first** — SPAN/TAP visibility, no active scanning unless explicitly approved during a maintenance window
- **Zones & conduits native** — ISA/IEC 62443 segmentation is a first-class concept, not a report add-on
- **Safety-aware** — response automation never disrupts operations without explicit policy gates
- **OT protocol parsing** — Modbus, DNP3, S7comm, EtherNet/IP, OPC UA, BACnet, IEC 104, MQTT, CoAP
- **Three operational modes** — Discover, Defend, Respond — matching how OT security programs mature

| Credential | Username | Password | 
|---|---|---|
| **Admin** | `admin` | `OT@Secure2025` | 

**Live:** [https://siteq8.github.io/ConduitShield](https://siteq8.github.io/ConduitShield)

Demo credentials with click-to-fill. Certificate-backed device trust. Three operational modes: Discover, Defend, Respond.

Real-time security posture across 7 Purdue zones (L0-L5 + DMZ). Communication baselines detect unauthorized protocols, rogue devices, and polling anomalies. 2,461 monitored assets with 12 zones and 34 conduits.

Safety-aware 6-step playbook for unauthorized PLC writes with explicit safety gates. Evidence locker with chain of custody (PCAPs, logs, PLC state, timelines). Contact tree with SLA times for operations, CISO, vendors, integrators, legal, and external IR.

| Mode | Purpose | 
|---|---|
| **Discover** | Asset inventory, topology mapping, zone/conduit definition, protocol baselining | 
| **Defend** | Access control, segmentation enforcement, vulnerability management, IoT lifecycle | 
| **Respond** | Detection engineering, incident cases, OT playbooks, evidence preservation | 

| Module | Key Capabilities | 
|---|---|
| **Overview** | Security posture: 2,461 assets, Purdue L0-L5 zone health with conduit counts, real-time alerts, communication baselines (normal protocol detection, rogue device, unauthorized protocol, polling anomaly) | 
| **Asset Intelligence** | Passive discovery (SPAN/TAP): vendor, model, serial, firmware, OS, protocol, zone, IP/MAC, owner, criticality. Auto-built topology with protocol map (Modbus, S7comm, OPC UA, EtherNet/IP, DNP3, MQTT). End-of-life tracking with compensating controls | 
| **Access & Identity** | JIT remote access with MFA, approval chains, session recording, one-click disconnect. Certificate-backed device trust. RBAC/ABAC role matrix (Operator, Engineer, Vendor, SOC, Admin). SSO/federation (SAML, OAuth2, AD). Default credential detection and forced replacement | 
| **Vulnerability & Patch** | ICS-CERT advisory correlation (6 real CVEs). OT patch workflow (assess → test offline → schedule outage → deploy → verify → rollback). SBOM ingest with component-to-asset mapping. Config drift detection with golden image comparison. Compensating control tracking | 
| **IoT Lifecycle** | Secure onboarding (4-gate: credentials, certificate, config, access controls). Firmware update validation (signature + SHA-256 checksum + rollback). Device state awareness (healthy/degraded/compromised). Key and certificate lifecycle. Logical access controls on interfaces, ports, APIs | 
| **Detection & Analytics** | 47 MITRE ATT&CK for ICS techniques. Process-aware anomaly detection: unexpected writes, unauthorized mode changes, unusual polling, scan storms, engineering uploads, abnormal inter-zone traffic. 14 event sources connected. Threat hunting queries | 
| **Incident Response** | P1-P4 cases with zone/conduit impact. OT playbooks with safety gates (never auto-disrupt without policy). Evidence locker (PCAPs, logs, PLC state, timelines) with chain of custody. Contact trees (operations, CISO, vendors, integrators, legal, external IR) | 
| **Segmentation Policy** | Zone/conduit policy with allowed protocols, ports, time windows. Change simulation with blast radius preview. DMZ architecture recommendations. Unidirectional gateway placement. Continuous traffic-vs-policy validation | 
| **Compliance & Audit** | 6 frameworks: IEC 62443, NIST 800-82, NERC CIP, ATT&CK ICS, CIS v8.1, CISA. 1,247 controls tracked. Audit-ready reports (assets, access, patches, EOL, incidents, exceptions). Platform deployment: on-prem first, lightweight collectors, store-and-forward, HA, API-first, multi-site | 

```
ConduitShield Platform
│
├── DISCOVER MODE
│   ├── Passive Network Discovery (SPAN/TAP)
│   ├── Full Asset Inventory (vendor, model, firmware, protocol, zone)
│   ├── Auto-built Topology with Purdue Levels
│   ├── Protocol-aware Parsing (Modbus, DNP3, S7comm, CIP, OPC UA)
│   └── Communication Baselines + Rogue Device Detection
│
├── DEFEND MODE
│   ├── Identity & Access Management (RBAC/ABAC, MFA, JIT)
│   ├── Privileged Access Workflow (session recording, command logging)
│   ├── Default Credential Detection & Forced Replacement
│   ├── Vulnerability Correlation (ICS-CERT, vendor advisories)
│   ├── Patch Workflow (assess → test → schedule → deploy → verify → rollback)
│   ├── Compensating Control Tracking
│   ├── Config Drift Detection & Golden Image Comparison
│   ├── SBOM Ingest & Supply Chain Mapping
│   ├── IoT Onboarding & Secure Configuration
│   ├── Certificate & Key Lifecycle Management
│   ├── Firmware Update Validation (signature, checksum, rollback)
│   ├── Zone/Conduit Policy Builder
│   ├── Segmentation Continuous Validation
│   └── Change Simulation (blast radius preview)
│
├── RESPOND MODE
│   ├── Event Collection (OT sensors, HMIs, SCADA, historians, firewalls)
│   ├── Process-aware Anomaly Detection
│   ├── MITRE ATT&CK for ICS Mapping (47 techniques)
│   ├── Audit Log Storage with Integrity Protection
│   ├── Incident Cases (severity, zones, impact, containment)
│   ├── OT-specific Playbooks
│   ├── Evidence Locker (logs, PCAPs, timelines, chain of custody)
│   ├── Safety-aware Response Gates
│   └── Contact Trees (vendors, operations, legal, responders)
│
└── PLATFORM
    ├── On-premises First (optional hybrid analytics)
    ├── Lightweight Collectors for Plants/Substations
    ├── Store-and-forward for Low-bandwidth Sites
    ├── API-first Integration (SIEM, SOAR, CMDB, IAM)
    └── Multi-site Tenancy (enterprise, MSSP)
```
| Standard | Version | Coverage | 
|---|---|---|
| **ISA/IEC 62443** | 2018 | Zones/conduits, security levels, system requirements, component requirements | 
| **NIST SP 800-82** | Rev 3 | OT security guide — network architecture, access control, monitoring | 
| **NERC CIP** | v7 | Critical infrastructure protection for bulk electric systems | 
| **MITRE ATT&CK for ICS** | v14 | 47 techniques mapped with detection rules and hunting queries | 
| **CIS Controls** | v8.1 | Implementation groups 1-3 mapped to OT context | 
| **CISA ICS Guidelines** | 2024 | Secure-by-design, default credential elimination, SBOM | 
| **NIST IoT Cybersecurity** | NIST IR 8259 | Device identity, logical access, software update, telemetry | 

| Protocol | Port | Standard | Use Case | 
|---|---|---|---|
| Modbus/TCP | 502 | IEC 61158 | PLCs, RTUs, sensors | 
| DNP3 | 20000 | IEEE 1815 | Substations, water/wastewater | 
| S7comm/S7comm+ | 102 | Siemens | S7-300/400/1200/1500 PLCs | 
| EtherNet/IP (CIP) | 44818 | IEC 61158 | Rockwell/Allen-Bradley | 
| OPC UA | 4840 | IEC 62541 | HMIs, SCADA, historians | 
| BACnet/IP | 47808 | ISO 16484-5 | Building management | 
| IEC 60870-5-104 | 2404 | IEC 60870 | Power grid SCADA | 
| MQTT | 1883 | ISO/IEC 20922 | IoT sensors, telemetry | 
| CoAP | 5683 | RFC 7252 | Constrained IoT devices | 
| TriStation | 1502 | Schneider | Safety instrumented systems | 
| PROFINET | — | IEC 61158 | Siemens automation | 
| Foundation Fieldbus | — | IEC 61158 | Process instrumentation | 

ConduitShield includes OT-specific playbooks designed around safety and operational continuity:

| Playbook | Key Principle | 
|---|---|
| **Unauthorized PLC Write** | Isolate source, verify process state BEFORE any PLC action, compare against golden backup | 
| **Ransomware on OT-adjacent** | Sever IT-OT conduit, verify DMZ integrity, check for lateral movement to L2/L1 | 
| **Unauthorized Logic Change** | Freeze engineering access, diff current vs golden program, engage vendor if needed | 
| **Unsafe Cross-zone Traffic** | Block at conduit firewall, investigate source, verify no process impact before enforcement | 
| **Vendor Session Compromise** | Terminate session immediately, audit all changes made, rotate credentials, review logs | 
| **Rogue Device Detection** | Port-disable at switch, capture traffic, identify device, assess blast radius | 

[https://siteq8.github.io/ConduitShield](https://siteq8.github.io/ConduitShield)

Login: `admin` / `OT@Secure2025`

```
git clone https://github.com/SiteQ8/ConduitShield.git
cd ConduitShield
open docs/index.html
```
For v1, the feature set prioritizes **safe, passive capabilities** that deliver value without taking operational risks:

| Feature | Status | 
|---|---|
| Passive asset discovery & inventory | Demo | 
| Topology with Purdue zone mapping | Demo | 
| Zone/conduit policy builder | Demo | 
| Firmware vulnerability correlation (ICS-CERT) | Demo | 
| Secure remote access monitoring | Demo | 
| MITRE ATT&CK for ICS detections | Demo | 
| Incident cases with OT playbooks | Demo | 
| IoT device lifecycle controls | Demo | 
| Multi-standard compliance dashboard | Demo | 

Based on NIST, CISA, and ISA/IEC 62443 guidance, ConduitShield is designed to avoid common OT security tool pitfalls:

| Red Flag | ConduitShield Approach | 
|---|---|
| Active-scan only | Passive-first from SPAN/TAP | 
| Relies on default credentials | Detects and forces replacement | 
| Weak logging | Full audit trail with integrity protection | 
| No patch visibility | Firmware/software version tracking + ICS-CERT correlation | 
| Ignores OT safety | Safety-aware response gates, no auto-disruption | 
| Flat network assumption | ISA/IEC 62443 zones & conduits as first-class concept | 
| Vendor lock-in | API-first, open integration with SIEM/SOAR/CMDB | 

MIT — see [LICENSE](/SiteQ8/ConduitShield/blob/main/LICENSE).

<sub>ConduitShield — Passive-first cybersecurity for OT, ICS, and IIoT</sub>

<sub>ISA/IEC 62443 · NIST SP 800-82 · NERC CIP · MITRE ATT&CK for ICS · CISA</sub>

<sub>[@SiteQ8](https://github.com/SiteQ8) — Ali AlEnezi</sub>

---

## Research Cycle — 2026-11-10 18:06 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/DriftGuard/DriftGuard

### Web Summary: https://github.com/DriftGuard/DriftGuard

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
**Intelligent GitOps Configuration Drift Detection Engine**

DriftGuard is an intelligent GitOps configuration drift detection platform that continuously monitors Kubernetes resources for configuration drift by comparing live cluster states against desired states stored in Git repositories. It features enhanced state tracking, automatic resolution detection, and comprehensive drift analysis.

- **Enhanced Drift Detection**: Continuously monitors Kubernetes resources with intelligent drift classification
- **Drift Resolution Detection**: Automatically detects when drift is resolved and configuration matches Git again
- **State Management**: Tracks drift status (active/resolved/none) with timestamps and resolution messages
- **Git Integration**: Compares live state against Git-stored manifests with hash-based state tracking
- **Intelligent Classification**: Automatically classifies drift types (Scaling, VersionChange, ResourceChange, etc.)
- **Severity Assessment**: Assigns severity levels (low, medium, high) to detected drifts
- **MongoDB Storage**: Persistent storage of drift records with enhanced state tracking
- **REST API**: Comprehensive HTTP endpoints for querying drift records, status filtering, and statistics
- **Metrics & Monitoring**: Prometheus metrics and health checks
- **Enhanced Logging**: Detailed logging with emojis for drift detection and resolution events

Want to dive deeper into the configuration drift crisis and understand how DriftGuard solves real-world infrastructure challenges? Check out our comprehensive guide:

**[Learn More About DriftGuard](/DriftGuard/DriftGuard/blob/main/ABOUT.md)** - Discover the configuration drift crisis, understand GitOps vs InfraOps, explore real-world examples, and learn about DriftGuard's business value and architecture.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Kubernetes    │    │   Git Repo      │    │   DriftGuard    │
│   API Server    │    │   (Desired      │    │   Backend       │
│   (Live State)  │◄──►│   State)        │◄──►│   (Controller)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MongoDB       │    │   REST API      │
                       │   (Enhanced     │    │   (HTTP         │
                       │   Drift Records)│    │   Endpoints)    │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Prometheus    │    │   Health        │
                       │   Metrics       │    │   Checks        │
                       └─────────────────┘    └─────────────────┘
```
- **Go 1.21+**
- **MongoDB 4.4+**
- **Kubernetes cluster** (local or remote)
- **Git repository** with Kubernetes manifests
- **kubectl** configured to access your cluster

```
git clone <repository-url>
cd DriftGuard
```
```
# Create data directory
mkdir -p ~/data/db
# Start MongoDB (macOS/Linux)
sudo mongod --dbpath=~/data/db
# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```
Update the configuration file (`backend/configs/config.yaml`):

```
server:
  port: 8080
  read_timeout: 30s
  write_timeout: 30s
  idle_timeout: 60s
database:
  host: localhost
  port: 27017
  dbname: driftguard
  timeout: 10s
kubernetes:
  config_path: ""  # Leave empty for default kubeconfig
  context: ""
  namespaces: ["driftguard"]
  resources: ["deployments", "services", "configmaps", "secrets"]
  skip_system_namespaces: true
git:
  repository_url: "Add your Repo"
  default_branch: main
  clone_timeout: 5m
  pull_timeout: 2m
drift_detection:
  interval: 30s
  enable_periodic: true
```
```
# Create a dummy Git repository for testing
mkdir -p dummy-k8s-repo
cd dummy-k8s-repo
git init
# Create test Kubernetes manifests
cat > test-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-app
  namespace: driftguard
  labels:
    app: nginx
    environment: test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.23
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        env:
        - name: NGINX_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: driftguard
  labels:
    app: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: driftguard
data:
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
        
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    }
  environment: "production"
  version: "1.0.0"
EOF
# Commit the manifests
git add test-deployment.yaml
git commit -m "Initial Kubernetes manifests"
```
`kubectl create namespace driftguard````
cd backend
go run cmd/controller/main.go --config=configs/config.yaml
```
```
# Check if DriftGuard is running
curl http://localhost:8080/health
# Expected response:
# {"status":"healthy","message":"Service is running","time":"2025-01-15T10:30:00Z"}
```
```
# Apply the manifests from Git
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Verify resources are created
kubectl get all -n driftguard
```
```
# Trigger manual drift analysis
curl -X POST http://localhost:8080/api/v1/analyze
# Expected response:
# {"message":"Drift analysis triggered successfully","status":"started"}
```
```
# Wait a few seconds, then check drift records
sleep 5
curl http://localhost:8080/api/v1/drift-records
# You should see records with drift_detected: false initially
```
```
# Scale the deployment to create drift
kubectl scale deployment nginx-app -n driftguard --replicas=3
# Verify the change
kubectl get deployment nginx-app -n driftguard
```
```
# Trigger drift analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for drift detection
sleep 5
curl http://localhost:8080/api/v1/drift-records/active
# You should now see active drift records
```
```
# Scale back to original state
kubectl scale deployment nginx-app -n driftguard --replicas=2
# Or re-apply the Git manifest
kubectl apply -f ../dummy-k8s-repo/test-deployment.yaml
# Trigger analysis again
curl -X POST http://localhost:8080/api/v1/analyze
# Wait and check for resolution
sleep 5
curl http://localhost:8080/api/v1/drift-records/resolved
```
```
# Test image change drift
kubectl set image deployment/nginx-app nginx=nginx:1.24 -n driftguard
# Test environment variable drift
kubectl set env deployment/nginx-app NGINX_ENV=staging -n driftguard
# Test resource drift
kubectl patch deployment nginx-app -n driftguard -p '{"spec":{"template":{"spec":{"containers":[{"name":"nginx","resources":{"requests":{"memory":"128Mi"}}}]}}}}'
# Trigger analysis after each change
curl -X POST http://localhost:8080/api/v1/analyze
```
```
# Get comprehensive statistics
curl http://localhost:8080/api/v1/statistics
# Expected response includes:
# - total_records
# - active_drift
# - resolved_drift
# - no_drift
# - active_percentage
# - resolved_percentage
```
```
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
# Get specific resource drift
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/health` | Basic health check | 
| `GET` | `/ready` | Readiness check | 
| `GET` | `/metrics` | Prometheus metrics | 

| Method | Endpoint | Description | 
|---|---|---|
| `GET` | `/api/v1/drift-records` | List all drift records | 
| `GET` | `/api/v1/drift-records/:resourceId` | Get specific drift record | 
| `GET` | `/api/v1/drift-records/active` | Get active drift records | 
| `GET` | `/api/v1/drift-records/resolved` | Get resolved drift records | 
| `GET` | `/api/v1/statistics` | Get drift statistics | 
| `POST` | `/api/v1/analyze` | Trigger manual drift analysis | 

**List Drift Records:**

```
# Get all drift records
curl http://localhost:8080/api/v1/drift-records
# Filter by namespace
curl "http://localhost:8080/api/v1/drift-records?namespace=driftguard"
# Filter by drift status
curl "http://localhost:8080/api/v1/drift-records?drift_detected=true"
```
**Get Specific Record:**

```
# Get drift record for a specific resource
curl http://localhost:8080/api/v1/drift-records/Deployment:driftguard:nginx-app
```
Resources are identified using the format: `kind:namespace:name`

The system tracks drift status with three states:

- **`active`**: Drift is currently detected and active
- **`resolved`**: Drift was previously detected but has been resolved
- **`none`**: No drift detected

The system automatically classifies drifts into categories:

- **Scaling**: Replica count changes
- **VersionChange**: Container image changes
- **ResourceChange**: CPU/memory resource changes
- **ConfigurationChange**: Environment variable changes
- **LabelChange**: Label modifications
- **AnnotationChange**: Annotation modifications
- **PortChange**: Port configuration changes
- **VolumeChange**: Volume mount changes
- **SecretChange**: Secret reference changes
- **ConfigMapChange**: ConfigMap reference changes

- **High**: Image changes, secret changes, significant scaling (>50%)
- **Medium**: Minor scaling, environment variables, ports, volumes
- **Low**: Labels, annotations, other metadata

The system provides comprehensive drift statistics:

```
{
  "statistics": {
    "total_records": 25,
    "active_drift": 3,
    "resolved_drift": 15,
    "no_drift": 7,
    "recent_active_drift": 1,
    "recent_resolutions": 2,
    "active_percentage": 12.0,
    "resolved_percentage": 60.0
  }
}
```
- `config_path`: Path to kubeconfig file
- `context`: Kubernetes context to use
- `namespaces`: List of namespaces to monitor
- `resources`: List of resource types to monitor
- `skip_system_namespaces`: Skip system namespaces

- `repository_url`: Git repository URL
- `default_branch`: Branch to monitor
- `clone_timeout`: Timeout for repository cloning
- `pull_timeout`: Timeout for pulling updates

- `interval`: Periodic analysis interval
- `enable_periodic`: Enable periodic drift detection

1. **MongoDB Connection Failed**
\# Check if MongoDB is running ps aux | grep mongod # Start MongoDB if not running sudo mongod --dbpath=\~/data/db
2. **Kubernetes Connection Failed**
\# Check kubectl configuration kubectl config current-context # Test cluster connection kubectl get nodes
3. **Git Repository Access Failed**
\# Check Git repository URL in config # Ensure repository is accessible git ls-remote \<repository-url>
4. **Port Already in Use**
\# Check if port 8080 is in use lsof -i :8080 # Kill process or change port in config

DriftGuard uses structured logging with emojis:

- 🚀 System startup
- ⚠️ Drift detected
- ✅ Drift resolved
- 🔄 Drift continued
- 📊 Analysis completed

```
# Build the container
docker build -t driftguard:latest backend/
# Run with environment variables
docker run -d \
  -p 8080:8080 \
  -e MONGODB_HOST=your-mongodb-host \
  -e KUBECONFIG=/path/to/kubeconfig \
  driftguard:latest
```
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: driftguard
  namespace: driftguard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: driftguard
  template:
    metadata:
      labels:
        app: driftguard
    spec:
      containers:
      - name: driftguard
        image: driftguard:latest
        ports:
        - containerPort: 8080
        env:
        - name: MONGODB_HOST
          value: "mongodb-service"
        volumeMounts:
        - name: kubeconfig
          mountPath: /root/.kube
          readOnly: true
      volumes:
      - name: kubeconfig
        secret:
          secretName: driftguard-kubeconfig
```
We welcome contributions! Please see our [Contributing Guidelines](/DriftGuard/DriftGuard/blob/main/CONTRIBUTING.md) for details.

This project is licensed under the MIT License - see the [LICENSE](/DriftGuard/DriftGuard/blob/main/LICENSE.md) file for details.

For questions, feature requests, or contributions, please open an issue in this repository.

---

### Source: https://github.com/Coding-Dev-Tools/configdrift

Keep configurations consistent across all environments, automatically. ConfigDrift compares configs, flags drift, and reports compliance violations before they cause incidents.

⭐ **Star this repo** if you manage multi-environment configs — it helps other devs find ConfigDrift!

Real-world scenarios:

- **Multi-environment compliance**: Ensure staging and prod configs are identical before every deploy
- **Secrets audit**: Detect env vars that exist in one environment but are missing in another
- **CI/CD gating**: Block PRs that introduce config drift across environments
- **Incident prevention**: Catch a changed database endpoint before it causes a production outage

ConfigDrift is **not published to public PyPI**. Install from the self-hosted index, a direct GitHub install, or via Homebrew/Scoop (below).

```
# Install directly from GitHub (recommended)
pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
```
Editable install for development:

`pip install -e ".[dev]"`
Then run: `configdrift --help`

Compare two config files:

`configdrift check dev.yaml prod.yaml`
Scan entire directories as environments:

`configdrift scan ./config/dev ./config/staging ./config/prod`
Use a config file to define environments:

```
configdrift init
configdrift scan --config .configdrift.yaml
```
`configdrift check <file1> <file2> [--output table|json|silent] [--baseline dev] [--target prod]`
Output formats:

- `table` (default): Rich colored table output
- `json`: Machine-readable JSON for CI integration
- `silent`: Exit code only (0 = no breaking drift, 1 = breaking drift found)

`configdrift scan ./dev ./staging ./prod --baseline dev`
Scans all config files in each directory, merges them, and compares against a baseline environment.

`configdrift init .`
Creates `.configdrift.yaml` in the specified directory.

Use `--output silent` for CI gating:

`configdrift check dev.yaml prod.yaml --output silent || echo "Drift detected!"````
- name: Detect config drift
  run: |
    pip install git+https://github.com/Coding-Dev-Tools/configdrift.git
    configdrift check ./config/staging/app.yaml ./config/prod/app.yaml --output silent
```
- **Exit code 1 with no output**: use `--output table` to inspect drift details.
- **TOML parsing errors on Python \< 3.11**: install `tomli` and `tomli-w` or use Python 3.11+.
- **Large config scans are slow**: narrow the scan to changed files or a single directory.
- **Unexpected breaking drift**: review severity rules in the project settings; `database*` and `auth*` keys are flagged as breaking by default.

| Format | Extension | Notes | 
|---|---|---|
| YAML | `.yaml`, `.yml` | Full nested structure support | 
| JSON | `.json` | Nested flattening | 
| TOML | `.toml` | Python 3.11+ native | 
| .env | `.env` | `KEY=VALUE` format | 

- **Info**: Non-critical value changes
- **Warning**: Added or removed optional keys
- **Breaking**: Changes to critical keys (`database*`, `auth*`, `api_key*`, `secret*`, `password*`, `token*`, `endpoint*`)

```
# Install with dev dependencies
pip install -e ".[dev]"
# Run tests
pytest
# Run with coverage
pytest --cov=configdrift
```
ConfigDrift is one of 11 tools in the Revenue Holdings suite. One license covers all CLI tools.

| Plan | Price | Best For | 
|---|---|---|
| **Free** | $0 | Individual devs, OSS — CLI only, 1 env pair | 
| **ConfigDrift Individual** | **$15/mo** ($12 billed annually) | Professional devs — unlimited environments, custom rules | 
| **Suite (all 11 tools)** | **$49/mo** ($39 billed annually) | Full Revenue Holdings toolkit — 40% savings | 
| **Team** | **$79/mo** ($63 billed annually) | Up to 5 devs — drift history, Slack alerts, priority support | 
| **Enterprise** | Custom | SSO, RBAC, compliance reports, dedicated support | 

🔹 **No lock-in**: CLI works fully offline on the free tier — no telemetry, no phone-home.
🔹 **Annual billing**: Save 20%.

| Feature | Free | ConfigDrift | Suite | Team | Enterprise | 
|---|---|---|---|---|---|
| CLI: check, scan | ✓ | ✓ | ✓ | ✓ | ✓ | 
| Unlimited environments | — | ✓ | ✓ | ✓ | ✓ | 
| Custom rules / policies | — | ✓ | ✓ | ✓ | ✓ | 
| Drift history / audit trail | — | — | — | ✓ | ✓ | 
| Slack / webhook alerts | — | — | — | ✓ | ✓ | 
| Compliance reports | — | — | — | — | ✓ | 
| RBAC | — | — | — | — | ✓ | 
| SSO / SAML / OIDC | — | — | — | — | ✓ | 
| Priority support | Community | 24h | 24h | 8h | Dedicated | 

<sub>Part of [Revenue Holdings](https://coding-dev-tools.github.io/devforge/) — CLI tools built by autonomous AI.</sub>

MIT

`npm test  # runs: node --test tests/`

---

### Source: https://github.com/ryjen/config-drift-guard/releases/tag/demo-video-2026-10-18

## Repository navigation

# Config Drift Guard — Drift Detection & Approval-Gated Reconciliation Demo

Pre-release
## Config Drift Guard — Demonstration Video

An 87-second demonstration of deterministic configuration drift detection, approval-gated reconciliation, and safe failure handling.

Config Drift Guard is a lightweight control plane that compares desired configuration against observed state, identifies drift, generates remediation plans, and requires explicit operator approval before changes are applied.

### What the demo shows

**1. Detect configuration drift**

A synthetic API service starts with:

- Image: `api:v1`
- Replicas: `1`
- Log level: `debug`

The desired configuration specifies:

- Image: `api:v2`
- Replicas: `3`
- Log level: `info`

The system detects all three differences and generates an immutable remediation plan.

**2. Approve and verify reconciliation**

The operator approves the plan. The system validates the observed state, applies the changes atomically, and verifies convergence.

**Result: No drift remains.**

**3. Reject stale remediation plans**

A second scenario changes the observed image to `api:v3` after the plan is generated.

Preflight detects that the plan is stale and refuses reconciliation. The modified configuration is preserved, and apply and verification steps are skipped.

**4. Explicit operator rejection**

The operator can reject a remediation plan without modifying the observed configuration.

### Technical highlights

- Deterministic drift detection
- Immutable remediation plans and evidence digests
- Human approval before mutation
- Stale-plan protection
- Atomic configuration updates
- Post-reconciliation verification
- Persistent workflow state and auditability

### Video details

- Duration: 87 seconds
- Format: MP4, H.264, 720p
- Narration: ElevenLabs
- English captions: Separate WebVTT file

The video uses edited footage from real automated Chromium/Playwright tests against local synthetic fixtures. It does not represent production infrastructure, a continuous manual recording, or independent security certification.

**Source code and reproducible walkthrough:**

[https://github.com/ryjen/config-drift-guard](https://github.com/ryjen/config-drift-guard)

**License and distribution provenance:**

[#34](https://github.com/ryjen/config-drift-guard/issues/34)

---

## Research Cycle — 2026-11-11 00:06 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### Source: https://github.com/Elshayib

## Popular repositories Loading

1. 
                [omarchy-oligarchy-theme](/Elshayib/omarchy-oligarchy-theme)
              omarchy-oligarchy-theme Public A dark medieval-keep theme for Omarchy: iron-grey stone, antique gold windows, moonlight text. Elite capital. Public code.

Something went wrong, please refresh the page to try again.

If the problem persists, check the [GitHub status page](https://www.githubstatus.com/)
          or [contact support](/contact).

---

### Source: https://github.com/janinelurenana

**Security Detection · Network Engineering · Automation**

Polytechnic University of the Philippines

I build **detection systems and network infrastructure that hold under real conditions**, not just controlled labs.

My work focuses on:

- Translating ambiguous security problems into **repeatable detection logic**
- Designing networks with **enforced boundaries and validated failover**
- Automating infrastructure with **state verification, not just deployment**

Most student projects stop at *“it works.”*
Mine are built to answer:

*Does it still work under failure, scale, and misconfiguration?*

- Build **SIEM-style detection logic** from raw logs (not dashboards on clean data)
- Design **segmented enterprise networks** with measurable resilience
- Implement **network-as-code pipelines** with drift detection
- Develop **risk-based anomaly detection systems** using SQL correlation logic

**Repo:** [https://github.com/janinelurenana/cloud-security-analyzer](https://github.com/janinelurenana/cloud-security-analyzer)

Built a modular detection pipeline that processes CloudTrail-style logs and produces **severity-ranked, MITRE ATT&CK–mapped findings**.

- 8 detection rules across 26 simulated cloud resources
- 43 validated findings surfaced via Streamlit
- Config-driven thresholds (no hardcoded detection logic)

**What matters:**

- Detection logic is **decoupled from thresholds** → mirrors real SIEM rule design
- Outputs are **explicitly mapped to attacker behavior**, not generic alerts

**Mapped Techniques:**

- T1078 — Valid Accounts / Privilege Abuse
- T1098 — Account Manipulation
- T1110 — Brute Force

**Repo:** [https://github.com/janinelurenana/Enterprise-Campus-Network-Architecture](https://github.com/janinelurenana/Enterprise-Campus-Network-Architecture)

Designed and validated a segmented campus network with **enforced least privilege and high availability**.

- VLAN segmentation: IT, HR, Guest, DMZ
- ACL-enforced zone isolation (not theoretical)
- FortiGate Active–Passive HA

**Validation, not assumption:**

- \~1 second failover convergence
- Session persistence during link failure

**Additional work:**

- Documented HSRP convergence behavior (5–10s)
- Extending to multi-site OSPF + IPsec VPN

**Repo:** [https://github.com/janinelurenana/declarative-network-provisioning](https://github.com/janinelurenana/declarative-network-provisioning)

Built a **multi-vendor network-as-code pipeline**:

YAML → Jinja2 → Netmiko → Device Configuration → State Verification

**Key capability:**

- Drift detection is **bidirectional**
  - Detects missing intended config
  - Detects unauthorized changes

**Why this matters:**
Most automation scripts push configs.
This enforces **state integrity**, which is what production environments actually need.

**Repo:** [https://github.com/janinelurenana/banking-fraud-detection-analytics](https://github.com/janinelurenana/banking-fraud-detection-analytics)

Built a transaction analysis system using **weighted anomaly scoring**, not simple thresholds.

- 5,500 transactions across 200 accounts
- Multi-table joins with CASE-based scoring

**Detection includes:**

- Velocity anomalies
- Geographic inconsistencies
- High-value outliers

**Key insight:**
Single signals don’t trigger alerts—**combined risk does**
→ aligns with real SIEM correlation logic

**Output:**

- Star schema → Power BI dashboards
- Geographic threat clustering for interpretability

**Security**

- Log Analysis · MITRE ATT&CK
- IAM Auditing · CSPM
- Burp Suite (SQLi) · Nmap

**Networking**

- GNS3 · FortiGate HA
- OSPF · VLANs · ACLs
- IPsec VPN · HSRP / VRRP
- NAT · STP

**Programming / Automation**

- Python · SQL
- Jinja2 · YAML
- Pandas · Streamlit · Netmiko

**Tooling**

- Power BI · MySQL
- AWS CloudTrail
- Kali Linux
- Git / GitHub

- Multi-site network simulation (OSPF + IPsec WAN)
- Detection engineering aligned with SOC workflows via TryHackMe
- CompTIA Security+ (target: Q3 2026)

Open to **junior-level roles**, not just internships:

- Security Analyst
- Network Engineer
- Detection Engineer (entry/junior)

---

### Source: https://github.com/SiteQ8/ConduitShield

### Web Summary: https://github.com/SiteQ8/ConduitShield

[Local Qwen Summarizer Error: <urlopen error [Errno 113] No route to host>]

Fallback Raw Content:
**One platform. Three modes. Full OT lifecycle security.**

[Live Dashboard](https://siteq8.github.io/ConduitShield) · [Features](#features) · [Architecture](#architecture) · [Standards](#standards-alignment) · [Quick Start](#quick-start)

APIs are the #1 attack vector in IT. In OT, the attack surface is the **protocol layer** — Modbus writes, S7comm uploads, DNP3 commands — where a single unauthorized change can halt a plant or endanger safety.

Most cybersecurity tools are built for IT and retrofitted for OT. They actively scan, ignore zones and conduits, treat the plant like a flat LAN, and have no awareness of operational safety.

ConduitShield is **built for OT from the ground up**:

- **Passive-first** — SPAN/TAP visibility, no active scanning unless explicitly approved during a maintenance window
- **Zones & conduits native** — ISA/IEC 62443 segmentation is a first-class concept, not a report add-on
- **Safety-aware** — response automation never disrupts operations without explicit policy gates
- **OT protocol parsing** — Modbus, DNP3, S7comm, EtherNet/IP, OPC UA, BACnet, IEC 104, MQTT, CoAP
- **Three operational modes** — Discover, Defend, Respond — matching how OT security programs mature

| Credential | Username | Password | 
|---|---|---|
| **Admin** | `admin` | `OT@Secure2025` | 

**Live:** [https://siteq8.github.io/ConduitShield](https://siteq8.github.io/ConduitShield)

Demo credentials with click-to-fill. Certificate-backed device trust. Three operational modes: Discover, Defend, Respond.

Real-time security posture across 7 Purdue zones (L0-L5 + DMZ). Communication baselines detect unauthorized protocols, rogue devices, and polling anomalies. 2,461 monitored assets with 12 zones and 34 conduits.

Safety-aware 6-step playbook for unauthorized PLC writes with explicit safety gates. Evidence locker with chain of custody (PCAPs, logs, PLC state, timelines). Contact tree with SLA times for operations, CISO, vendors, integrators, legal, and external IR.

| Mode | Purpose | 
|---|---|
| **Discover** | Asset inventory, topology mapping, zone/conduit definition, protocol baselining | 
| **Defend** | Access control, segmentation enforcement, vulnerability management, IoT lifecycle | 
| **Respond** | Detection engineering, incident cases, OT playbooks, evidence preservation | 

| Module | Key Capabilities | 
|---|---|
| **Overview** | Security posture: 2,461 assets, Purdue L0-L5 zone health with conduit counts, real-time alerts, communication baselines (normal protocol detection, rogue device, unauthorized protocol, polling anomaly) | 
| **Asset Intelligence** | Passive discovery (SPAN/TAP): vendor, model, serial, firmware, OS, protocol, zone, IP/MAC, owner, criticality. Auto-built topology with protocol map (Modbus, S7comm, OPC UA, EtherNet/IP, DNP3, MQTT). End-of-life tracking with compensating controls | 
| **Access & Identity** | JIT remote access with MFA, approval chains, session recording, one-click disconnect. Certificate-backed device trust. RBAC/ABAC role matrix (Operator, Engineer, Vendor, SOC, Admin). SSO/federation (SAML, OAuth2, AD). Default credential detection and forced replacement | 
| **Vulnerability & Patch** | ICS-CERT advisory correlation (6 real CVEs). OT patch workflow (assess → test offline → schedule outage → deploy → verify → rollback). SBOM ingest with component-to-asset mapping. Config drift detection with golden image comparison. Compensating control tracking | 
| **IoT Lifecycle** | Secure onboarding (4-gate: credentials, certificate, config, access controls). Firmware update validation (signature + SHA-256 checksum + rollback). Device state awareness (healthy/degraded/compromised). Key and certificate lifecycle. Logical access controls on interfaces, ports, APIs | 
| **Detection & Analytics** | 47 MITRE ATT&CK for ICS techniques. Process-aware anomaly detection: unexpected writes, unauthorized mode changes, unusual polling, scan storms, engineering uploads, abnormal inter-zone traffic. 14 event sources connected. Threat hunting queries | 
| **Incident Response** | P1-P4 cases with zone/conduit impact. OT playbooks with safety gates (never auto-disrupt without policy). Evidence locker (PCAPs, logs, PLC state, timelines) with chain of custody. Contact trees (operations, CISO, vendors, integrators, legal, external IR) | 
| **Segmentation Policy** | Zone/conduit policy with allowed protocols, ports, time windows. Change simulation with blast radius preview. DMZ architecture recommendations. Unidirectional gateway placement. Continuous traffic-vs-policy validation | 
| **Compliance & Audit** | 6 frameworks: IEC 62443, NIST 800-82, NERC CIP, ATT&CK ICS, CIS v8.1, CISA. 1,247 controls tracked. Audit-ready reports (assets, access, patches, EOL, incidents, exceptions). Platform deployment: on-prem first, lightweight collectors, store-and-forward, HA, API-first, multi-site | 

```
ConduitShield Platform
│
├── DISCOVER MODE
│   ├── Passive Network Discovery (SPAN/TAP)
│   ├── Full Asset Inventory (vendor, model, firmware, protocol, zone)
│   ├── Auto-built Topology with Purdue Levels
│   ├── Protocol-aware Parsing (Modbus, DNP3, S7comm, CIP, OPC UA)
│   └── Communication Baselines + Rogue Device Detection
│
├── DEFEND MODE
│   ├── Identity & Access Management (RBAC/ABAC, MFA, JIT)
│   ├── Privileged Access Workflow (session recording, command logging)
│   ├── Default Credential Detection & Forced Replacement
│   ├── Vulnerability Correlation (ICS-CERT, vendor advisories)
│   ├── Patch Workflow (assess → test → schedule → deploy → verify → rollback)
│   ├── Compensating Control Tracking
│   ├── Config Drift Detection & Golden Image Comparison
│   ├── SBOM Ingest & Supply Chain Mapping
│   ├── IoT Onboarding & Secure Configuration
│   ├── Certificate & Key Lifecycle Management
│   ├── Firmware Update Validation (signature, checksum, rollback)
│   ├── Zone/Conduit Policy Builder
│   ├── Segmentation Continuous Validation
│   └── Change Simulation (blast radius preview)
│
├── RESPOND MODE
│   ├── Event Collection (OT sensors, HMIs, SCADA, historians, firewalls)
│   ├── Process-aware Anomaly Detection
│   ├── MITRE ATT&CK for ICS Mapping (47 techniques)
│   ├── Audit Log Storage with Integrity Protection
│   ├── Incident Cases (severity, zones, impact, containment)
│   ├── OT-specific Playbooks
│   ├── Evidence Locker (logs, PCAPs, timelines, chain of custody)
│   ├── Safety-aware Response Gates
│   └── Contact Trees (vendors, operations, legal, responders)
│
└── PLATFORM
    ├── On-premises First (optional hybrid analytics)
    ├── Lightweight Collectors for Plants/Substations
    ├── Store-and-forward for Low-bandwidth Sites
    ├── API-first Integration (SIEM, SOAR, CMDB, IAM)
    └── Multi-site Tenancy (enterprise, MSSP)
```
| Standard | Version | Coverage | 
|---|---|---|
| **ISA/IEC 62443** | 2018 | Zones/conduits, security levels, system requirements, component requirements | 
| **NIST SP 800-82** | Rev 3 | OT security guide — network architecture, access control, monitoring | 
| **NERC CIP** | v7 | Critical infrastructure protection for bulk electric systems | 
| **MITRE ATT&CK for ICS** | v14 | 47 techniques mapped with detection rules and hunting queries | 
| **CIS Controls** | v8.1 | Implementation groups 1-3 mapped to OT context | 
| **CISA ICS Guidelines** | 2024 | Secure-by-design, default credential elimination, SBOM | 
| **NIST IoT Cybersecurity** | NIST IR 8259 | Device identity, logical access, software update, telemetry | 

| Protocol | Port | Standard | Use Case | 
|---|---|---|---|
| Modbus/TCP | 502 | IEC 61158 | PLCs, RTUs, sensors | 
| DNP3 | 20000 | IEEE 1815 | Substations, water/wastewater | 
| S7comm/S7comm+ | 102 | Siemens | S7-300/400/1200/1500 PLCs | 
| EtherNet/IP (CIP) | 44818 | IEC 61158 | Rockwell/Allen-Bradley | 
| OPC UA | 4840 | IEC 62541 | HMIs, SCADA, historians | 
| BACnet/IP | 47808 | ISO 16484-5 | Building management | 
| IEC 60870-5-104 | 2404 | IEC 60870 | Power grid SCADA | 
| MQTT | 1883 | ISO/IEC 20922 | IoT sensors, telemetry | 
| CoAP | 5683 | RFC 7252 | Constrained IoT devices | 
| TriStation | 1502 | Schneider | Safety instrumented systems | 
| PROFINET | — | IEC 61158 | Siemens automation | 
| Foundation Fieldbus | — | IEC 61158 | Process instrumentation | 

ConduitShield includes OT-specific playbooks designed around safety and operational continuity:

| Playbook | Key Principle | 
|---|---|
| **Unauthorized PLC Write** | Isolate source, verify process state BEFORE any PLC action, compare against golden backup | 
| **Ransomware on OT-adjacent** | Sever IT-OT conduit, verify DMZ integrity, check for lateral movement to L2/L1 | 
| **Unauthorized Logic Change** | Freeze engineering access, diff current vs golden program, engage vendor if needed | 
| **Unsafe Cross-zone Traffic** | Block at conduit firewall, investigate source, verify no process impact before enforcement | 
| **Vendor Session Compromise** | Terminate session immediately, audit all changes made, rotate credentials, review logs | 
| **Rogue Device Detection** | Port-disable at switch, capture traffic, identify device, assess blast radius | 

[https://siteq8.github.io/ConduitShield](https://siteq8.github.io/ConduitShield)

Login: `admin` / `OT@Secure2025`

```
git clone https://github.com/SiteQ8/ConduitShield.git
cd ConduitShield
open docs/index.html
```
For v1, the feature set prioritizes **safe, passive capabilities** that deliver value without taking operational risks:

| Feature | Status | 
|---|---|
| Passive asset discovery & inventory | Demo | 
| Topology with Purdue zone mapping | Demo | 
| Zone/conduit policy builder | Demo | 
| Firmware vulnerability correlation (ICS-CERT) | Demo | 
| Secure remote access monitoring | Demo | 
| MITRE ATT&CK for ICS detections | Demo | 
| Incident cases with OT playbooks | Demo | 
| IoT device lifecycle controls | Demo | 
| Multi-standard compliance dashboard | Demo | 

Based on NIST, CISA, and ISA/IEC 62443 guidance, ConduitShield is designed to avoid common OT security tool pitfalls:

| Red Flag | ConduitShield Approach | 
|---|---|
| Active-scan only | Passive-first from SPAN/TAP | 
| Relies on default credentials | Detects and forces replacement | 
| Weak logging | Full audit trail with integrity protection | 
| No patch visibility | Firmware/software version tracking + ICS-CERT correlation | 
| Ignores OT safety | Safety-aware response gates, no auto-disruption | 
| Flat network assumption | ISA/IEC 62443 zones & conduits as first-class concept | 
| Vendor lock-in | API-first, open integration with SIEM/SOAR/CMDB | 

MIT — see [LICENSE](/SiteQ8/ConduitShield/blob/main/LICENSE).

<sub>ConduitShield — Passive-first cybersecurity for OT, ICS, and IIoT</sub>

<sub>ISA/IEC 62443 · NIST SP 800-82 · NERC CIP · MITRE ATT&CK for ICS · CISA</sub>

<sub>[@SiteQ8](https://github.com/SiteQ8) — Ali AlEnezi</sub>

---

## 2026-11-12 00:08 UTC

**Topic:** hash configs, alert, auto-rollback

**arXiv Sources:**

### arXiv:2603.04657

# Computer Science > Computation and Language

\[Submitted on 4 Mar 2026\]

# Title:Stan: An LLM-based thermodynamics course assistant

[View PDF](/pdf/2603.04657)

[HTML (experimental)](https://arxiv.org/html/2603.04657v1)

Abstract:Discussions of AI in education focus predominantly on student-facing tools -- chatbots, tutors, and problem generators -- while the potential for the same infrastructure to support instructors remains largely unexplored. We describe Stan, a suite of tools for an undergraduate chemical engineering thermodynamics course built on a data pipeline that we develop and deploy in dual roles: serving students and supporting instructors from a shared foundation of lecture transcripts and a structured textbook index. On the student side, a retrieval-augmented generation (RAG) pipeline answers natural-language queries by extracting technical terms, matching them against the textbook index, and synthesizing grounded responses with specific chapter and page references. On the instructor side, the same transcript corpus is processed through structured analysis pipelines that produce per-lecture summaries, identify student questions and moments of confusion, and catalog the anecdotes and analogies used to motivate difficult material -- providing a searchable, semester-scale record of teaching that supports course reflection, reminders, and improvement. All components, including speech-to-text transcription, structured content extraction, and interactive query answering, run entirely on locally controlled hardware using open-weight models (Whisper large-v3, Llama\~3.1 8B) with no dependence on cloud APIs, ensuring predictable costs, full data privacy, and reproducibility independent of third-party services. We describe the design, implementation, and practical failure modes encountered when deploying 7--8 billion parameter models for structured extraction over long lecture transcripts, including context truncation, bimodal output distributions, and schema drift, along with the mitigations that resolved them.

### Additional Features

### Current browse context:

cs.CL

Change to browse by:

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

### arXiv:2610.38234

# Computer Science > Robotics

\[Submitted on 28 Oct 2026 ([v1](https://arxiv.org/abs/2610.38234v1)), last revised 30 Oct 2026 (this version, v2)\]

# Title:SimRetract: Zero-Shot Sim-to-Real Robotic Assistance for Retractor Take-Over in Open Surgery

[View PDF](/pdf/2610.38234)

[HTML (experimental)](https://arxiv.org/html/2610.38234v2)

Abstract:We demonstrate the first zero-shot sim-to-real transfer for a surgeon-robot collaboration task in open surgery: retractor take-over. A robot arm takes a retractor from the surgeon's hand and preserves retraction at handoff, using a policy trained only on simulated demonstrations, without human demonstrations or real-world fine-tuning. Imitation learning from real demonstrations is limited by collection and labeling costs, and by performance degradation when the environment changes. Our framework, SimRetract, generates simulated demonstrations designed for transfer: the policy observes masked instrument images and grasp geometry, learns to recover from off-nominal states, and acts with margin for execution drift. Deployed zero-shot, it grasps the retractor in 90% of 50 surgeon-defined phantom presentations and preserves retraction at handoff in 78%. Results on unseen retractors suggest potential for generalization to instruments with similar grasp geometry. Across ten policy configurations and 1,200 simulated and real trials, we localize the sim-to-real gap to components: in simulation, grasp rates across ablations span 80-96%, while on the real robot removing the instrument mask alone drops performance to 22% grasped and 12% held. Transfer-oriented design thus makes zero-shot sim-to-real transfer feasible for a surgical assistance task without human demonstrations. Code is available here: [this https URL](https://anonymous.4open.science/r/simretract-58D2).

## Submission history

From: Xucheng Wang \[
[view email](/show-email/b20d6be2/2610.38234)\]

**[\[v1\]](/abs/2610.38234v1)**Wed, 28 Oct 2026 03:36:24 UTC (41,076 KB)

**\[v2\]**Fri, 30 Oct 2026 04:34:21 UTC (41,076 KB)

### Additional Features

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

### arXiv:2611.03737

# Computer Science > Machine Learning

\[Submitted on 1 Nov 2026\]

# Title:SSPE: Robust Sequential Staypoint Extraction in Degraded Trajectory Data

[View PDF](/pdf/2611.03737)

[HTML (experimental)](https://arxiv.org/html/2611.03737v1)

Abstract:Extracting semantically meaningful staypoints from raw trajectory streams is a foundational prerequisite for mobility analytics. However, real-world trajectory data is frequently degraded by severe spatial noise and protracted temporal dropouts. Classic threshold-based extraction methods, such as the widely adopted sliding-window algorithm, are highly sensitive to these anomalies, routinely fracturing continuous stationary episodes into disjointed fragments. To overcome this limitation, we propose the Sequential Staypoint Extraction (SSPE) algorithm. SSPE employs a resilient, state-driven architecture that replaces static spatial anchors with a dynamic centroid and introduces an $n$-step lookahead heuristic to structurally tolerate transient coordinate drift. Concurrently, it utilizes temporal bridging mechanisms to prevent artificial fragmentation during prolonged signal loss. Since optimal extraction parameters vary significantly across datasets, we further introduce a fully unsupervised, consensus-based parameter estimation framework. This framework derives baseline statistical scales directly from the raw trajectory data and identifies the optimal parameter configuration by maximizing structural agreement, thereby eliminating the reliance on annotated ground truth. We evaluate SSPE on the ExtraSensory dataset, a real-world mobility corpus with manually verified ground-truth staypoints, against the sliding-window implementation of Trackintel, one of the most widely adopted extraction baselines in the field. Empirical results demonstrate that SSPE achieves superior accuracy, yielding higher F1-scores while simultaneously improving computational efficiency over this standard.

### Additional Features

### References & Citations

Loading...

# Bibliographic and Citation Tools

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

# Code, Data and Media Associated with this Article

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub *([What is DagsHub?](https://dagshub.com/))*

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

# Demos

# Recommenders and Search Tools

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

IArxiv Recommender
              *([What is IArxiv?](https://iarxiv.org/about))*

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).
## Research Cycle — 2026-11-12 12:07 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection
**arXiv:** [2603.02345](https://arxiv.org/abs/2603.02345)  
**Authors:** Sami Abuzakuk, Lucas Crijns, Anne-Marie Kermarrec, Rafael Pires, Martijn de Vos  
**Published:** 2026-03-02  
**Categories:** cs.SE, cs.AI, cs.MA  

**Abstract:**
Infrastructure as code (IaC) tools automate cloud provisioning but verifying that deployed systems remain consistent with the IaC specifications remains challenging. Such configuration drift occurs because of bugs in the IaC specification, manual changes, or system updates. Large language model (LLM)-based agentic AI systems can automate the analysis of large volumes of telemetry data, making them suitable for the detection of configuration drift. However, existing agentic systems implicitly assume that the tools they invoke always return correct outputs, making them vulnerable to erroneous tool responses. Since agents cannot distinguish whether an anomalous tool output reflects a real infrastructure problem or a broken tool, such errors may cause missed drift or false alarms, reducing reliability precisely when it is most needed. We introduce RIVA (Robust Infrastructure by Verification Agents), a novel multi-agent system that performs robust IaC verification even when tools produce incorrect or misleading outputs. RIVA employs two specialized agents, a verifier agent and a tool generation agent, that collaborate through iterative cross-validation, multi-perspective verification, and tool call history tracking. Evaluation on the AIOpsLab benchmark demonstrates that RIVA, in the presence of erroneous tool responses, recovers task accuracy from 27.3% when using a baseline ReAct agent to 50.0% on average. RIVA also improves task accuracy 28% to 43.8% without erroneous tool responses. Our results show that cross-validation of diverse tool calls enables more reliable autonomous infrastructure verification in production cloud environments.

---

---

## Research Cycle — 2026-11-12 13:50 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection
**arXiv:** [2603.02345](https://arxiv.org/abs/2603.02345)  
**Authors:** Sami Abuzakuk, Lucas Crijns, Anne-Marie Kermarrec, Rafael Pires, Martijn de Vos  
**Published:** 2026-03-02  
**Categories:** cs.SE, cs.AI, cs.MA  

**Abstract:**
Infrastructure as code (IaC) tools automate cloud provisioning but verifying that deployed systems remain consistent with the IaC specifications remains challenging. Such configuration drift occurs because of bugs in the IaC specification, manual changes, or system updates. Large language model (LLM)-based agentic AI systems can automate the analysis of large volumes of telemetry data, making them suitable for the detection of configuration drift. However, existing agentic systems implicitly assume that the tools they invoke always return correct outputs, making them vulnerable to erroneous tool responses. Since agents cannot distinguish whether an anomalous tool output reflects a real infrastructure problem or a broken tool, such errors may cause missed drift or false alarms, reducing reliability precisely when it is most needed. We introduce RIVA (Robust Infrastructure by Verification Agents), a novel multi-agent system that performs robust IaC verification even when tools produce incorrect or misleading outputs. RIVA employs two specialized agents, a verifier agent and a tool generation agent, that collaborate through iterative cross-validation, multi-perspective verification, and tool call history tracking. Evaluation on the AIOpsLab benchmark demonstrates that RIVA, in the presence of erroneous tool responses, recovers task accuracy from 27.3% when using a baseline ReAct agent to 50.0% on average. RIVA also improves task accuracy 28% to 43.8% without erroneous tool responses. Our results show that cross-validation of diverse tool calls enables more reliable autonomous infrastructure verification in production cloud environments.

---

### RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection
**arXiv:** [2603.02345v1](https://arxiv.org/abs/2603.02345v1)  
**Authors:** Sami Abuzakuk, Lucas Crijns, Anne-Marie Kermarrec, Rafael Pires, Martijn de Vos  
**Published:** 2026-03-02  
**Categories:** cs.SE, cs.AI, cs.MA  

**Abstract:**
Infrastructure as code (IaC) tools automate cloud provisioning but verifying that deployed systems remain consistent with the IaC specifications remains challenging. Such configuration drift occurs because of bugs in the IaC specification, manual changes, or system updates. Large language model (LLM)-based agentic AI systems can automate the analysis of large volumes of telemetry data, making them suitable for the detection of configuration drift. However, existing agentic systems implicitly assume that the tools they invoke always return correct outputs, making them vulnerable to erroneous tool responses. Since agents cannot distinguish whether an anomalous tool output reflects a real infrastructure problem or a broken tool, such errors may cause missed drift or false alarms, reducing reliability precisely when it is most needed. We introduce RIVA (Robust Infrastructure by Verification Agents), a novel multi-agent system that performs robust IaC verification even when tools produce incorrect or misleading outputs. RIVA employs two specialized agents, a verifier agent and a tool generation agent, that collaborate through iterative cross-validation, multi-perspective verification, and tool call history tracking. Evaluation on the AIOpsLab benchmark demonstrates that RIVA, in the presence of erroneous tool responses, recovers task accuracy from 27.3% when using a baseline ReAct agent to 50.0% on average. RIVA also improves task accuracy 28% to 43.8% without erroneous tool responses. Our results show that cross-validation of diverse tool calls enables more reliable autonomous infrastructure verification in production cloud environments.

---

### Source: https://www.youtube.com/

About
Press
Copyright
Contact us
Creators
Advertise
Developers
Terms
Privacy
Policy & Safety
How YouTube works
Test new features
© 2026 Google LLC

---

## Research Cycle — 2026-11-12 18:04 UTC

**Topic:** config-drift-detection  
**Focus:** hash configs, alert, auto-rollback

### RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection
**arXiv:** [2603.02345](https://arxiv.org/abs/2603.02345)  
**Authors:** Sami Abuzakuk, Lucas Crijns, Anne-Marie Kermarrec, Rafael Pires, Martijn de Vos  
**Published:** 2026-03-02  
**Categories:** cs.SE, cs.AI, cs.MA  

**Abstract:**
Infrastructure as code (IaC) tools automate cloud provisioning but verifying that deployed systems remain consistent with the IaC specifications remains challenging. Such configuration drift occurs because of bugs in the IaC specification, manual changes, or system updates. Large language model (LLM)-based agentic AI systems can automate the analysis of large volumes of telemetry data, making them suitable for the detection of configuration drift. However, existing agentic systems implicitly assume that the tools they invoke always return correct outputs, making them vulnerable to erroneous tool responses. Since agents cannot distinguish whether an anomalous tool output reflects a real infrastructure problem or a broken tool, such errors may cause missed drift or false alarms, reducing reliability precisely when it is most needed. We introduce RIVA (Robust Infrastructure by Verification Agents), a novel multi-agent system that performs robust IaC verification even when tools produce incorrect or misleading outputs. RIVA employs two specialized agents, a verifier agent and a tool generation agent, that collaborate through iterative cross-validation, multi-perspective verification, and tool call history tracking. Evaluation on the AIOpsLab benchmark demonstrates that RIVA, in the presence of erroneous tool responses, recovers task accuracy from 27.3% when using a baseline ReAct agent to 50.0% on average. RIVA also improves task accuracy 28% to 43.8% without erroneous tool responses. Our results show that cross-validation of diverse tool calls enables more reliable autonomous infrastructure verification in production cloud environments.

---


