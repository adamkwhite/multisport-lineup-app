# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it by:

1. **DO NOT** open a public GitHub issue
2. Email the maintainer with details of the vulnerability
3. Include steps to reproduce the issue if possible

## Secure Configuration

### API Credentials

This application uses the TeamSnap API and requires OAuth credentials. **Never commit these credentials to version control.**

**Best Practices:**
- ✅ Store credentials in `.env` file (gitignored)
- ✅ Use `.env.example` as a template with placeholder values
- ✅ Rotate credentials periodically
- ✅ Use different credentials for development/staging/production
- ❌ Never hardcode credentials in source code
- ❌ Never commit `.env` files to git
- ❌ Never share credentials in public forums or documentation

### Environment Variables

Required sensitive environment variables:
- `TEAMSNAP_CLIENT_ID` - OAuth client ID from TeamSnap Developer Portal
- `TEAMSNAP_CLIENT_SECRET` - OAuth client secret (keep private!)
- `SECRET_KEY` - Flask session secret (generate a random string)

### SSL/TLS Certificates

The application supports HTTPS for local development using self-signed certificates:
- Certificates are stored in `certs/` directory (gitignored)
- Generate new certificates: `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
- **Production**: Use proper certificates from a trusted CA (Let's Encrypt, etc.)

### Session Security

The application implements secure session handling:
- HTTP-only cookies (prevents XSS attacks)
- Secure cookies in production (HTTPS-only)
- SameSite cookie policy (CSRF protection)
- 24-hour session timeout

## Security Features

### Code Quality & Scanning

- **SonarQube**: Automated security vulnerability scanning in CI/CD
- **Pre-commit hooks**: Local code quality checks
- **GitHub Actions**: 3-stage validation pipeline
- **Dependency scanning**: Automated via GitHub Dependabot

### Input Validation

- Player data validated before processing
- API responses sanitized
- Type checking with mypy
- Linting with flake8 and bandit

### Dependencies

Keep dependencies up to date:
```bash
pip list --outdated
pip install --upgrade -r requirements.txt
```

## Known Security Considerations

### TeamSnap API Rate Limiting

Currently not implemented. In production, consider:
- Rate limiting per user/IP
- Caching TeamSnap API responses
- Implementing retry logic with exponential backoff

### Multi-User Authentication

Current version uses single OAuth flow. For production with multiple users:
- Implement proper user authentication
- Store OAuth tokens securely (encrypted database)
- Use refresh tokens to minimize credential exposure

### Database Security

- Development uses SQLite (single-user)
- Production should use PostgreSQL with:
  - Encrypted connections (SSL/TLS)
  - Limited database user permissions
  - Regular backups
  - No sensitive data in logs

## Compliance

This project handles youth sports data. Be aware of:
- **COPPA** (Children's Online Privacy Protection Act) - if collecting data from users under 13
- **FERPA** (Family Educational Rights and Privacy Act) - if used in educational settings
- **GDPR** - if serving users in the EU

Consult with legal counsel if deploying for production use with minors' data.

## Security Updates

Subscribe to security advisories for dependencies:
- GitHub Security Advisories
- Python security mailing list
- Flask security announcements

## Contact

For security concerns, please contact the repository maintainer.
