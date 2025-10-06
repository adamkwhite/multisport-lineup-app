# SonarQube Integration - Troubleshooting

## Common Issues

### SonarQube Scan Fails

**Check workflow logs:**
```bash
gh pr checks <PR_NUMBER>
gh run view <RUN_ID> --log-failed
```

**Common causes:**
- Missing secrets (SONAR_TOKEN, SONAR_HOST_URL)
- SonarQube instance unavailable
- Invalid coverage files

### Quality Gate Fails

1. View results: <YOUR_SONARQUBE_URL>/dashboard?id=multisport-lineup-app
2. Common failures:
   - Coverage too low - add tests
   - New bugs - fix code issues
   - Code smells - refactor code
   - Duplications - remove duplicate code

### Coverage Not Showing

**Verify coverage files:**
```bash
pytest tests/api/ --cov=app --cov-report=xml
npm test -- --coverage
ls -la coverage.xml test-results/coverage-*/lcov.info
```

### Tests Fail in CI

**Run locally:**
```bash
source lineup-venv/bin/activate
pytest tests/api/ -v
npm test
```

### Badges Not Displaying

**Test badge endpoint:**
```bash
curl -I "<YOUR_SONARQUBE_URL>/api/project_badges/measure?project=multisport-lineup-app&metric=alert_status"
```

Should return 200 OK

### Main Branch Not Analyzed

Trigger analysis by:
- Merge a PR to main
- Push directly to main
- GitHub Actions will run automatically

## Getting Help

- View logs: `gh run view <RUN_ID> --log`
- Check SonarQube: <YOUR_SONARQUBE_URL>
- See usage guide: [sonarqube-usage.md](sonarqube-usage.md)
