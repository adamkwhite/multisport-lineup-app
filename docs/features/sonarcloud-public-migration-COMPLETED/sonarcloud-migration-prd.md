# Product Requirements Document: SonarCloud Migration

## Introduction/Overview

Migrate this project from self-hosted SonarQube (Community Edition at `44.206.255.230:9000`) to SonarCloud's cloud-hosted platform. This migration enables public dashboard visibility for recruiters and peers while reducing infrastructure maintenance for this public repository.

**Problem Statement**: The current self-hosted SonarQube instance is not publicly accessible, preventing recruiters and peers from viewing code quality metrics. For public repositories, SonarCloud provides public dashboard visibility, automatic PR decoration, and professional portfolio presentation.

## Goals

**Primary Goal:**
1. Enable public access to quality metrics dashboard for portfolio/recruitment visibility

**Secondary Goals:**
1. Maintain continuous code quality analysis with existing quality gate thresholds
2. Improve GitHub integration with automatic badges and PR decoration
3. Establish reusable migration pattern for other public repositories

## User Stories

**As a recruiter/hiring manager**, I want to:
- View live code quality metrics on the repository README
- Access the public SonarCloud dashboard to assess code quality
- See quality gate status on pull requests

**As a developer/peer**, I want to:
- Quickly verify code quality standards are maintained
- See quality metrics without requiring access credentials
- Trust that CI/CD blocks merges on quality gate failures

**As a repository maintainer**, I want to:
- Provide public visibility into code quality for this repository
- Automatically display quality badges in README
- Maintain existing quality standards and thresholds (match current settings exactly)
- Keep self-hosted instance available for private projects

## Functional Requirements

### FR1: SonarCloud Account Setup
- Create/configure SonarCloud account linked to GitHub
- Import project to SonarCloud
- Configure project key and organization settings
- Generate SonarCloud authentication token for GitHub Actions

### FR2: Quality Gate Configuration
- Configure custom quality gate to match existing self-hosted thresholds exactly:
  - New Code: 0 issues
  - Security Hotspots: 100% reviewed
  - Coverage: ≥0% (current threshold)
  - Duplicated Lines: ≤25%
- Ensure quality gate passes with current codebase
- Do NOT use SonarCloud default if it differs from current settings

### FR3: CI/CD Pipeline Update
- Replace self-hosted SonarQube action with SonarCloud action in `.github/workflows/build.yml`
- Update secrets in GitHub repository (`SONAR_TOKEN`, remove old credentials)
- Maintain existing 3-stage pipeline structure (quick-checks → tests+sonarcloud → review)
- Ensure quality gate failures block PR merges

### FR4: Public Visibility Features
- Add SonarCloud quality gate badge to `README.md`
- Add direct link to SonarCloud dashboard in `README.md`
- Verify badge updates automatically on quality changes

### FR5: Documentation Updates
- Update `docs/development/ci-cd-pipeline.md` to reference SonarCloud
- Update `README.md` to remove self-hosted SonarQube badge references
- Document migration steps for future public repository migrations

## Non-Goals (Out of Scope)

1. **Self-Hosted Decommission**: Keep self-hosted SonarQube running for private projects
2. **Quality Standards Changes**: Maintain existing quality gate thresholds (no relaxation)
3. **Code Changes**: No application code modifications required
4. **Private Repository Migration**: Only migrate this repo (establish pattern for later)
5. **SonarCloud Premium Features**: Use free tier for public repositories only

## Technical Considerations

### GitHub Actions Workflow Update
Current workflow uses `SonarSource/sonarqube-scan-action@v5` (or v6) pointing to self-hosted instance. Update to:

```yaml
- name: SonarCloud Scan
  uses: SonarSource/sonarcloud-github-action@master
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Required Secrets
- **New**: `SONAR_TOKEN` - SonarCloud authentication token (GitHub repository secret)
- **Remove**: Self-hosted SonarQube credentials (if stored as secrets)

### Quality Gate Compatibility
Current custom quality gate:
- Issues > 0 (new code)
- Security Hotspots Reviewed < 100%
- Coverage < 0.0%
- Duplicated Lines > 25.0%

**Decision**: Configure custom quality gate to match existing thresholds exactly. Do not use SonarCloud defaults.

### Project Key
Use consistent project key format: `adamkwhite_<project>` (GitHub organization + repo name)

## Success Metrics

1. **Migration Success**:
   - [ ] SonarCloud project created and linked to GitHub
   - [ ] CI/CD pipeline runs successfully with SonarCloud
   - [ ] Quality gate passes on main branch

2. **Visibility Success**:
   - [ ] Quality gate badge visible in README
   - [ ] Public dashboard accessible without authentication
   - [ ] Badge updates automatically on code changes

3. **Maintenance Reduction**:
   - [ ] No self-hosted instance configuration required for this repo
   - [ ] CI/CD pipeline runs without manual intervention
   - [ ] Quality gate failures block merges as expected

## Timeline

**Priority**: Immediate (complete ASAP after repository is made public)
**Blocking**: No - does not block making repository public
**Estimated Duration**: 1-2 hours

## Open Questions

1. **Badge Placement**: Where in README should the SonarCloud badge appear? (Recommend: Replace existing SonarQube badges in header section)

## Related Work

- **Issue #70**: Setup SonarCloud account and import project
- **Issue #71**: Update CI/CD pipeline to use SonarCloud
- **Issue #72**: Add README badges and public visibility features
- **Issue #73**: Documentation updates and verification

## GitHub Issues

- [#70 - Setup SonarCloud account](https://github.com/adamkwhite/multisport-lineup-app/issues/70)
- [#71 - Update CI/CD pipeline](https://github.com/adamkwhite/multisport-lineup-app/issues/71)
- [#72 - Add README badges](https://github.com/adamkwhite/multisport-lineup-app/issues/72)
- [#73 - Documentation and verification](https://github.com/adamkwhite/multisport-lineup-app/issues/73)

## References

- SonarCloud: https://sonarcloud.io
- SonarCloud GitHub Action: https://github.com/SonarSource/sonarcloud-github-action
- Current self-hosted SonarQube: http://44.206.255.230:9000/dashboard (private)
- GitHub Repository: https://github.com/adamkwhite/multisport-lineup-app

---

**Status**: PLANNED
**Last Updated**: 2025-10-12
**Implementation Approach**: Traditional (Option 1: Standard PRD Structure)
