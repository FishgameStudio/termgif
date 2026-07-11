# Security Policy

## Supported Versions
Only the latest major/minor release receives security patches. Older versions will not be updated with security fixes.

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅Yes              |
| Older   | ❌No               |

## Reporting a Vulnerability
Do **not** create public GitHub Issues to report security vulnerabilities. Public disclosures put all users at risk.

1. Submit security reports via private channel (e.g. maintainer private email / GitHub security advisory form).
2. Include detailed information:
   - Affected component, commit hash or release version
   - Step-by-step reproduction instructions
   - Potential exploit impact (information leak, RCE, crash, bypass, etc.)
   - Suggested fix or proof-of-concept (if available)

### Response Process
- You will receive an acknowledgment **as soon as possible**.
- Maintainers will investigate, validate the vulnerability, and coordinate a fix timeline.
- A patch will be prepared and released before public disclosure.
- You may be credited in the security advisory if you wish.

## Security Best Practices for Users
1. Always use the latest stable release of this project.
2. Avoid running untrusted input without validation/sanitization.
3. Do not expose internal APIs, debug endpoints or sensitive identifiers to public networks.
4. Review third-party dependencies regularly for known CVEs.
5. Remove debug print statements, hardcoded secrets and local test credentials before deployment.

## Dependency Security
- Dependencies are periodically scanned for vulnerabilities.
- Pull Requests that upgrade vulnerable packages are highly encouraged.
- If you identify an insecure dependency, submit a private security report rather than a public PR.

## Scope of This Policy
This security policy covers code, build scripts, CI workflows, example code and documentation hosted within this repository.
It does not cover:
- Misconfiguration on user-owned operating systems, networks or hosting environments
- Third-party external services unrelated to this project
- Vulnerabilities present in upstream unrelated libraries (report to the respective upstream maintainers)

## Disclosure Timeline
1. Report received & acknowledged (0-7 days)
2. Vulnerability validation & fix development (7–30 days)
3. Patch release + private advisory notification
4. Full public security advisory published after patch availabilities
