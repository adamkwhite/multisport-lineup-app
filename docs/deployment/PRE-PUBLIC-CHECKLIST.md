# Pre-Public Release Security Checklist

This checklist ensures the repository is safe to make public.

## ✅ Completed (Automated Checks)

- [x] **Git history audit** - No credentials found in commit history
- [x] **SSL certificates removed** - Removed from repository root
- [x] **`.gitignore` verified** - `.env`, `*.pem`, `*.key` properly ignored
- [x] **Code audit** - No hardcoded credentials found
- [x] **Security documentation added** - README.md and SECURITY.md updated

## ⚠️ Manual Actions Required

### Recommended Workflow (No Downtime)

**Order of Operations:**

1. [ ] **Make repository public** (safe - credentials never in git history)
2. [ ] **Generate NEW TeamSnap credentials**
   - Visit: https://www.teamsnap.com/api/v3/me/oauth_applications
   - Create new OAuth application
   - Copy new client_id and client_secret
3. [ ] **Update local `.env` file** with new credentials
4. [ ] **Test authentication** - Verify new credentials work
5. [ ] **Revoke OLD credentials** - Delete old OAuth application from TeamSnap

**Why this order?** You maintain access throughout the process and can rollback if needed.

### Optional Enhancements

- [ ] **Update SonarQube URLs** in README badges
  - Consider: Private SonarQube instance may not be accessible publicly
  - Options:
    - Switch to SonarCloud (public SonarQube service)
    - Remove SonarQube badges from README
    - Keep as-is (badges will just show as broken images)

- [ ] **Review documentation**
  - Update any references to private infrastructure
  - Check for internal URLs or hostnames
  - Verify all examples use public URLs

- [ ] **Enable GitHub security features**
  - Dependabot alerts (automatic)
  - Secret scanning (automatic on public repos)
  - Code scanning (optional - GitHub Advanced Security)

## 📋 Repository Status

### Clean ✅
- No secrets in git history
- No secrets in tracked files
- Proper `.gitignore` configuration
- Security documentation in place

### Sensitive Files (Local Only)
- `.env` - Contains real credentials (gitignored ✅)
- `certs/cert.pem` - Self-signed SSL cert (gitignored ✅)
- `certs/key.pem` - SSL private key (gitignored ✅)
- `lineup.db` - SQLite database (gitignored ✅)

### New Files Added
- `SECURITY.md` - Security policy and best practices
- `docs/deployment/PRE-PUBLIC-CHECKLIST.md` - This checklist

## 🔒 Security Features in Place

- **Environment variables**: All secrets loaded from `.env`
- **Session security**: HTTPS-only, HttpOnly, SameSite cookies
- **CORS**: Restricted origins in production
- **Input validation**: Type checking and sanitization
- **CI/CD security**: SonarQube scanning, code quality checks
- **Pre-commit hooks**: Local security checks

## 📝 Post-Public Actions

Once repository is public:

1. **Monitor GitHub alerts**
   - Watch for Dependabot security alerts
   - Review any secret scanning alerts (false positives expected)

2. **Update documentation**
   - Add contributing guidelines (CONTRIBUTING.md)
   - Add code of conduct (CODE_OF_CONDUCT.md)
   - Add issue templates

3. **Community setup**
   - Enable GitHub Discussions (optional)
   - Add project description and tags
   - Update repository settings (Allow issues, PRs, etc.)

## ⚡ Quick Commands

```bash
# Verify no secrets in tracked files
git ls-files | xargs grep -l "TEAMSNAP_CLIENT\|SECRET_KEY" || echo "Clean"

# Check .gitignore is working
git status --ignored

# Final check before push
git status
git log --oneline -5

# Make repository public (GitHub CLI)
gh repo edit --visibility public

# Or via web: Settings > General > Danger Zone > Change visibility
```

## 🚀 Ready to Go Public?

**Checklist Summary:**
- ✅ Code is clean (verified)
- ✅ Documentation updated
- ⚠️ **Action required**: Revoke old TeamSnap credentials
- ✅ New credentials ready to generate after going public

**Final Steps:**
1. Revoke TeamSnap OAuth credentials (https://auth.teamsnap.com)
2. Commit security documentation changes
3. Push to GitHub
4. Make repository public
5. Generate new TeamSnap credentials
6. Test application with new credentials

---

**Last Updated**: 2025-10-12
**Audit Date**: 2025-10-12
**Status**: ✅ Ready (pending credential revocation)
