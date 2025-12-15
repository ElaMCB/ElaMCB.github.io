# UAA (Unified Autonomous Agent)

A modular, unified agent architecture that consolidates multiple autonomous agent capabilities into a single, maintainable system.

## Architecture

```
agents/
├── router.sh                 # Main orchestrator script
├── shared/                    # Shared utilities
│   ├── utils.sh              # Logging, GitHub API helpers
│   └── config.sh             # Configuration settings
└── capabilities/             # Individual agent capabilities
    ├── ci-fix/               # CI/CD failure detection and auto-fix
    │   └── ci-fix.sh
    ├── link-health/          # Broken link scanning
    │   └── link-health.sh
    └── security/             # Security vulnerability scanning
        └── security.sh
```

## Features

### Modular Design
- Each capability is self-contained in its own folder
- Shared utilities prevent code duplication
- Easy to add new capabilities

### Unified Workflow
- Single GitHub Actions workflow file
- Intelligent routing based on event type
- Centralized configuration

### Capabilities

#### 1. CI-Fix
- Monitors CI/CD pipeline failures
- Auto-fixes common issues (npm lock sync, missing dependencies)
- Creates GitHub issues for complex errors

#### 2. Link-Health
- Scans for broken links in HTML/Markdown files
- Creates PRs with fix reports
- Creates critical issues for internal broken links

#### 3. Security
- Runs npm audit for vulnerabilities
- Scans for exposed secrets
- Auto-fixes moderate/low severity issues
- Creates critical issues for urgent problems

## Usage

### Manual Execution

Run a specific capability:
```bash
bash agents/router.sh ci-fix
bash agents/router.sh link-health
bash agents/router.sh security
```

Run all capabilities:
```bash
bash agents/router.sh all
```

### GitHub Actions

The unified agent automatically runs based on workflow events:

- **workflow_run** (failure) → CI-Fix capability
- **schedule** (weekly) → All capabilities
- **push** (file changes) → Link-Health or Security based on file types
- **workflow_dispatch** → Run any capability manually

## Configuration

Edit `agents/shared/config.sh` to:
- Enable/disable specific capabilities
- Configure capability-specific settings
- Adjust schedules and thresholds

## Benefits

1. **Single Point of Maintenance**: One workflow file instead of three
2. **Shared Code**: Common utilities reduce duplication
3. **Easier Testing**: Test capabilities independently
4. **Scalability**: Add new capabilities easily
5. **Consistency**: Unified logging and error handling

## Migration from Separate Agents

The old separate workflows can be disabled once the unified agent is tested and verified. The unified agent provides the same functionality with better organization.

## Adding New Capabilities

1. Create a new folder in `agents/capabilities/`
2. Create your capability script (e.g., `my-capability.sh`)
3. Add capability function to `agents/router.sh`
4. Update `agents/shared/config.sh` with capability settings
5. Add capability option to unified workflow

## Troubleshooting

- Check capability logs in GitHub Actions output
- Verify scripts are executable: `chmod +x agents/**/*.sh`
- Ensure GitHub token has required permissions
- Review `agents/shared/config.sh` for capability enablement

