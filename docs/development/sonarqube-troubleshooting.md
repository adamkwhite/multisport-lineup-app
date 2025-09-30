# SonarQube Integration - Troubleshooting Guide

## Common Issues and Solutions

### Issue: SonarQube Scan Fails in GitHub Actions

**Symptoms:**
- GitHub Actions workflow shows "SonarQube Scan" as failed
- PR is blocked from merging

**Solutions:**

1. **Check workflow logs:**
   ```bash
   gh pr checks <PR_NUMBER>
   gh run view <RUN_ID> --log-failed
   ```

2. **Common causes:**
   - **Missing secrets:** Verify `SONAR_TOKEN` and `SONAR_HOST_URL` exist in repository settings
   - **Network issues:** SonarQube instance may be temporarily unavailable
   - **Invalid coverage files:** Tests may have failed to generate coverage.xml or lcov.info

3. **Quick fixes:**
   - Re-run the workflow: `gh run rerun <RUN_ID>`
   - Check SonarQube instance is accessible: `curl http://44.206.255.230:9000`

---

### Issue: Quality Gate Fails

**Symptoms:**
- SonarQube scan completes but quality gate status is "FAILED"
- PR cannot be merged

**Solutions:**

1. **View detailed results:**
   - Go to http://44.206.255.230:9000/dashboard?id=baseball-lineup-app
   - Click on "Failed" conditions to see why

2. **Common failures:**
   - **Coverage too low:** Add tests to increase coverage above thresholds (80% Python, 85% JavaScript)
   - **New bugs/vulnerabilities:** Fix code issues identified by SonarQube
   - **Code smells:** Refactor code to reduce maintainability issues
   - **Duplications:** Remove duplicate code blocks

3. **Temporary workaround (not recommended):**
   - Lower quality gate thresholds in SonarQube settings
   - Only use for urgent fixes; restore thresholds afterward

---

### Issue: Coverage Not Showing in SonarQube

**Symptoms:**
- SonarQube dashboard shows 0% coverage or "No coverage data"
- Tests ran successfully in GitHub Actions

**Solutions:**

1. **Verify coverage files are generated:**
   ```bash
   # Check if coverage.xml exists after pytest
   pytest tests/api/ --cov=app --cov-report=xml:coverage.xml

   # Check if lcov.info exists after Jest
   npm test -- --coverage
   ls -la test-results/coverage-*/lcov.info
   ```

2. **Check coverage file paths in sonar-project.properties:**
   ```properties
   sonar.python.coverage.reportPaths=coverage.xml
   sonar.javascript.lcov.reportPaths=lcov.info
   ```

3. **Verify files are copied to project root:**
   - GitHub Actions workflow should copy coverage files to root
   - Check workflow logs for coverage file copy step

4. **Run locally to debug:**
   ```bash
   python scripts/run-tests.py
   # This generates coverage files and copies them for SonarQube
   ```

---

### Issue: Tests Fail in GitHub Actions

**Symptoms:**
- "Run Python tests with coverage" or "Run JavaScript tests with coverage" steps fail
- Workflow continues due to `continue-on-error: true`

**Solutions:**

1. **Python test failures:**
   ```bash
   # Run tests locally
   source baseball-venv/bin/activate
   pytest tests/api/ -v

   # Check for missing dependencies
   pip install -r requirements.txt
   ```

2. **JavaScript test failures:**
   ```bash
   # Run tests locally
   npm install
   npm test

   # Check Jest configuration
   cat jest.config.js
   ```

3. **Tests pass locally but fail in CI:**
   - Check Python version (should be 3.12)
   - Check Node.js version (should be 18)
   - Verify all test dependencies are in requirements.txt / package.json

---

### Issue: Badges Not Displaying in README

**Symptoms:**
- README shows broken image icons instead of SonarQube badges
- Badges show "unknown" or error

**Solutions:**

1. **Verify badge URLs:**
   ```bash
   # Test badge endpoint
   curl -I "http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=alert_status"
   # Should return 200 OK
   ```

2. **Common causes:**
   - **Project not analyzed yet:** Wait for first SonarQube scan to complete
   - **Wrong project key:** Verify `baseball-lineup-app` matches sonar-project.properties
   - **SonarQube instance down:** Check if http://44.206.255.230:9000 is accessible

3. **Badge URL format:**
   ```markdown
   ![Badge](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=METRIC_NAME)
   ```

---

### Issue: "Main Branch Not Analyzed" in SonarQube

**Symptoms:**
- SonarQube dashboard shows "Project's Main Branch is not analyzed yet"
- No metrics displayed

**Solutions:**

1. **Trigger first analysis:**
   - Create and merge a PR to main branch
   - OR push directly to main branch
   - GitHub Actions workflow will trigger SonarQube scan

2. **Verify workflow triggers:**
   ```yaml
   on:
     push:
       branches: [ main ]
     pull_request:
       branches: [ main ]
   ```

3. **Manual scan (if needed):**
   ```bash
   # Install sonar-scanner CLI
   # Run from project root
   sonar-scanner \
     -Dsonar.token=$SONAR_TOKEN \
     -Dsonar.host.url=http://44.206.255.230:9000
   ```

---

### Issue: Workflow Takes Too Long

**Symptoms:**
- SonarQube scan step takes >5 minutes
- Timeout errors in quality gate check

**Solutions:**

1. **Check exclusions in sonar-project.properties:**
   - Ensure large directories are excluded (node_modules, venv, test-results)

2. **Increase timeout in workflow:**
   ```yaml
   - name: SonarQube Quality Gate Check
     timeout-minutes: 10  # Increase from 5 if needed
   ```

3. **Optimize test execution:**
   - Tests run before scan; slow tests delay the scan
   - Consider splitting tests or running in parallel

---

### Issue: Permission Denied or Authentication Errors

**Symptoms:**
- "Authentication required" or "403 Forbidden" errors
- SonarQube scan fails with authentication error

**Solutions:**

1. **Verify SONAR_TOKEN secret:**
   ```bash
   # Check secret exists (doesn't show value)
   gh secret list
   ```

2. **Regenerate token if needed:**
   - Log into SonarQube: http://44.206.255.230:9000
   - Go to Account > Security > Generate Tokens
   - Update GitHub secret with new token

3. **Check token permissions:**
   - Token must have "Execute Analysis" permission
   - Verify in SonarQube token settings

---

## Getting Help

If issues persist:

1. **Check SonarQube logs:**
   - View full analysis logs in SonarQube UI
   - Download task report for detailed debugging

2. **Review GitHub Actions logs:**
   ```bash
   gh run view <RUN_ID> --log
   ```

3. **Consult documentation:**
   - [SonarQube Usage Guide](sonarqube-usage.md)
   - [Official SonarQube Docs](https://docs.sonarqube.org/)
   - [GitHub Actions Docs](https://docs.github.com/en/actions)

4. **Check SonarQube Community:**
   - https://community.sonarsource.com/