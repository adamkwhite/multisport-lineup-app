# SonarCloud Migration - Implementation Tasks

Generated from: `sonarcloud-migration-prd.md`

## Relevant Files

- `.github/workflows/pr-validation.yml:109-123` - SonarQube scan and quality gate steps (replace with SonarCloud)
- `README.md:3-13` - SonarQube badge URLs (replace with SonarCloud badges)
- `docs/development/ci-cd-pipeline.md` - CI/CD documentation (update SonarQube references)
- `CLAUDE.md` - Project context (update SonarQube references if present)
- `docs/development/sonarcloud-migration.md` - New migration documentation (to be created)

### Notes

- This migration is infrastructure-focused with no application code changes required
- All changes maintain existing quality gate thresholds exactly
- SonarCloud account setup happens externally before code changes
- Testing requires creating a test branch and verifying CI/CD pipeline runs

## Tasks

- [ ] 1.0 Setup SonarCloud account and project configuration
  - [x] 1.1 Visit https://sonarcloud.io and sign in with GitHub account (adamkwhite)
  - [x] 1.2 Authorize SonarCloud to access GitHub repositories
  - [x] 1.3 Select "Analyze new project" and choose `adamkwhite/multisport-lineup-app`
  - [x] 1.4 Configure project key as `adamkwhite_multisport-lineup-app`
  - [x] 1.5 Set project visibility to "Public"
  - [x] 1.6 Navigate to Account > Security > Generate Tokens
  - [x] 1.7 Create token named `multisport-lineup-app-ci` and copy value (using pre-existing token)
  - [x] 1.8 Verify project appears in SonarCloud dashboard
  - [x] 1.9 Confirm project URL: https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app (will be public after first analysis)

- [x] 1.0 Setup SonarCloud account and project configuration
- [x] 2.0 Update CI/CD pipeline to use SonarCloud
  - [x] 2.1 Navigate to GitHub repository Settings > Secrets and variables > Actions
  - [x] 2.2 Add new secret `SONAR_TOKEN` with value from step 1.7
  - [x] 2.3 Remove old secret `SONAR_HOST_URL` if it exists
  - [x] 2.4 Open `.github/workflows/pr-validation.yml` for editing
  - [x] 2.5 Replace SonarQube scan action with sonarqube-scan-action@v6 (official for both SonarQube and SonarCloud)
  - [x] 2.6 Updated sonar-project.properties with organization and projectKey for SonarCloud
  - [x] 2.7 Commit changes to test branch (feat/sonarcloud-migration)
  - [x] 2.8 Push test branch and create draft PR #74
  - [x] 2.9 Monitor workflow run and verify SonarCloud scan completes successfully
  - [x] 2.10 Check SonarCloud dashboard updates with analysis results
  - [x] 2.11 Verify quality gate check passes/fails correctly (✅ PASSED)

- [ ] 3.0 Replace README badges with SonarCloud equivalents
  - [ ] 3.1 Open `README.md` and locate badge section (lines ~3-13)
  - [ ] 3.2 Replace Quality Gate Status badge URL
  - [ ] 3.3 Replace Coverage badge URL
  - [ ] 3.4 Replace Bugs badge URL
  - [ ] 3.5 Replace Vulnerabilities badge URL
  - [ ] 3.6 Replace Code Smells badge URL
  - [ ] 3.7 Replace Security Rating badge URL
  - [ ] 3.8 Replace Maintainability Rating badge URL
  - [ ] 3.9 Replace Reliability Rating badge URL
  - [ ] 3.10 Replace Lines of Code badge URL
  - [ ] 3.11 Replace Duplicated Lines badge URL
  - [ ] 3.12 Replace Technical Debt badge URL
  - [ ] 3.13 Update all badge links to point to: https://sonarcloud.io/summary/new_code?id=adamkwhite_multisport-lineup-app
  - [ ] 3.14 Verify no references to `44.206.255.230` remain in README
  - [ ] 3.15 Commit changes to test branch
  - [ ] 3.16 View README on GitHub to verify badges display correctly (may take 5-10 min after first analysis)

- [ ] 4.0 Configure custom quality gate in SonarCloud
  - [ ] 4.1 Navigate to SonarCloud project > Quality Gates tab
  - [ ] 4.2 Click "Create" to create a new custom quality gate
  - [ ] 4.3 Name quality gate: `multisport-lineup-app-custom`
  - [ ] 4.4 Add condition: "Issues" on "Overall Code" > 0 fails
  - [ ] 4.5 Add condition: "Security Hotspots Reviewed" on "Overall Code" < 100% fails
  - [ ] 4.6 Add condition: "Coverage" on "Overall Code" < 0.0% fails (matches existing threshold)
  - [ ] 4.7 Add condition: "Duplicated Lines (%)" on "Overall Code" > 25.0% fails
  - [ ] 4.8 Save custom quality gate
  - [ ] 4.9 Navigate back to project settings
  - [ ] 4.10 Assign custom quality gate to `adamkwhite_multisport-lineup-app` project
  - [ ] 4.11 Verify quality gate is active on project dashboard

- [ ] 5.0 Update documentation and verify migration success
  - [ ] 5.1 Open `docs/development/ci-cd-pipeline.md` for editing
  - [ ] 5.2 Replace all references to "SonarQube" with "SonarCloud"
  - [ ] 5.3 Update Stage 2 description to mention SonarCloud integration
  - [ ] 5.4 Replace self-hosted SonarQube URLs with SonarCloud dashboard links
  - [ ] 5.5 Open `CLAUDE.md` and search for SonarQube references
  - [ ] 5.6 Update External Services section to list SonarCloud instead of self-hosted instance
  - [ ] 5.7 Update any URLs pointing to `44.206.255.230:9000`
  - [ ] 5.8 Create new file `docs/development/sonarcloud-migration.md`
  - [ ] 5.9 Document the migration process with step-by-step instructions
  - [ ] 5.10 Include lessons learned and gotchas encountered
  - [ ] 5.11 Provide template section for migrating other public repos
  - [ ] 5.12 Reference PRD and GitHub issues #70-73 in migration doc
  - [ ] 5.13 Search entire codebase for `44.206.255.230` to find any remaining references
  - [ ] 5.14 Verify SonarCloud dashboard is publicly accessible (test in incognito/private browsing)
  - [ ] 5.15 Verify README badges display and update automatically
  - [ ] 5.16 Verify CI/CD pipeline runs successfully on test branch
  - [ ] 5.17 Verify quality gate passes on main branch
  - [ ] 5.18 Create a test PR with intentional quality issue to verify gate blocks merge
  - [ ] 5.19 Close test PR and merge actual migration PR to main
  - [ ] 5.20 Update PRD status from PLANNED to COMPLETED
  - [ ] 5.21 Close GitHub issues #70, #71, #72, #73 as completed
