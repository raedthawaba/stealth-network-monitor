#!/bin/bash

# 🚀 شل سكريبت لنقل جميع ملفات مستودع Stealth Network Monitor
# إلى مجلد جديد للمراجعة

echo "📦 إنشاء مجلد المستودع..."

# إنشاء مجلد المستودع
mkdir -p "stealth-network-monitor"
cd "stealth-network-monitor"

# إنشاء بنية المجلدات
mkdir -p .github/workflows
mkdir -p docs

echo "📁 نسخ الملفات الأساسية..."

# 1. الملفات الأساسية للتطبيق
cp ../stealth_network_spy_fixed.py .
cp ../main.py .
cp ../buildozer.spec .
cp ../STEALTH_README.md .
cp ../apk_creation_guide.md .
cp ../config.yaml .

# 2. ملفات GitHub
cp ../github_readme.md ./README.md
cp ../github_requirements.txt ./requirements.txt
cp ../github_gitignore.txt ./.gitignore
cp ../github_setup.sh ./setup.sh
cp ../github_license.txt ./LICENSE

# 3. ملفات CI/CD
cp ../github_workflow.yml ./.github/workflows/ci-cd.yml

# 4. ملفات Docker
cp ../docker-compose.yml .
cp ../Dockerfile .
cp ../.dockerignore .

# 5. ملفات إضافية
cp ../github_config.yml ./docs/repository-config.yml
cp ../mobile_config_ready.json ./

echo "🔧 إنشاء الملفات المفقودة..."

# إنشاء ملف CHANGELOG.md
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-08

### Added
- ✨ Initial release of Stealth Network Monitor
- 🕵️ Real-time network monitoring system
- 📱 Android APK support with buildozer
- 🎨 Beautiful Kivy-based GUI interface
- 🔒 Encrypted database storage
- 📊 Comprehensive behavioral analysis
- 🌐 Application signature detection
- 🛡️ Risk assessment and scoring
- 📚 Complete documentation and setup guides

### Features
- Network connection monitoring without root access
- Browser history analysis
- Process monitoring on Android/Termux
- Social media and streaming app detection
- Real-time dashboard with statistics
- Export capabilities (JSON, CSV, HTML)
- Docker containerization support
- CI/CD pipeline with GitHub Actions

### Technical Details
- Python 3.8+ compatible
- Kivy framework for mobile GUI
- SQLite database with custom encryption
- Termux environment optimized
- Cross-platform support (Android, Linux)

## Development
- Comprehensive unit tests
- Automated APK building
- Security scanning with Trivy
- Docker containerization
- GitHub Actions CI/CD pipeline

EOF

# إنشاء ملف CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# Contributing to Stealth Network Monitor

Thank you for your interest in contributing to Stealth Network Monitor! This project aims to provide a comprehensive, ethical network monitoring solution for Android devices.

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Provide detailed reproduction steps
4. Include environment information

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Describe the problem and solution
4. Consider implementation feasibility

### Code Contributions

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stealth-network-monitor.git
cd stealth-network-monitor

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Run the application
python main.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where possible
- Write tests for new features

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting
- Test on both Android and Linux environments
- Consider edge cases and error conditions

## Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Update changelog for new features
- Include examples in documentation

## Security

- Follow secure coding practices
- Never store sensitive data in plain text
- Report security vulnerabilities privately
- Follow the project's security policy

## Pull Request Process

1. Update the version number if applicable
2. Update the changelog
3. Ensure all tests pass
4. Request review from maintainers
5. Address any feedback

## Legal Considerations

- Ensure all contributions comply with the license
- Respect user privacy and consent requirements
- Do not add features for unauthorized monitoring
- Follow ethical guidelines for parental control tools

## Questions?

Feel free to open an issue or contact the maintainers if you have questions about contributing.

Thank you for helping make Stealth Network Monitor better! 🎉

EOF

# إنشاء ملف CODE_OF_CONDUCT.md
cat > CODE_OF_CONDUCT.md << 'EOF'
# Contributor Covenant Code of Conduct

## Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behavior that contributes to creating a positive environment include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

## Scope

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at conduct@stealth-monitor.com. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4, available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/

EOF

# إنشاء ملف SECURITY.md
cat > SECURITY.md << 'EOF'
# Security Policy

## Supported Versions

We currently support the following versions of Stealth Network Monitor with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Security is our top priority. We appreciate your efforts to responsibly disclose security vulnerabilities.

### How to Report

**Do not create public issues for security vulnerabilities.**

Instead, please report security vulnerabilities to **security@stealth-monitor.com**.

### What to Include

Please include the following information in your report:

- Type of vulnerability (e.g., buffer overflow, SQL injection, etc.)
- Full paths of source file(s) related to the manifestation of the vulnerability
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue
- Corrected version (if available)

### What to Expect

- **Initial Response**: You will receive an acknowledgment within 48 hours
- **Investigation**: We will investigate and confirm the vulnerability
- **Fix Development**: We will develop and test a fix
- **Disclosure**: We will coordinate disclosure with you
- **Release**: A patched version will be released as soon as possible

### Our Commitment

- We will make every effort to acknowledge your report within 48 hours
- We will provide regular updates on our progress
- We will credit you for your discovery (unless you prefer to remain anonymous)
- We will keep you informed throughout the resolution process

### Scope

This policy covers:
- The Stealth Network Monitor application
- Related documentation
- The project repository
- Associated infrastructure

### Out of Scope

The following are not covered by this policy:
- Third-party libraries and dependencies
- User-generated content
- Issues in older versions (see "Supported Versions" table above)

### Security Best Practices

We encourage the following security practices:

1. **Regular Updates**: Always use the latest version
2. **Secure Configuration**: Review security settings
3. **Access Control**: Limit system access
4. **Data Protection**: Encrypt sensitive information
5. **Audit Logs**: Monitor system activity
6. **Backup Strategy**: Implement regular backups

### Legal Notice

We appreciate your efforts to help keep our community safe. Any research conducted should be in line with applicable laws and regulations.

Thank you for helping keep Stealth Network Monitor secure! 🔒

EOF

# إنشاء ملف .dockerignore (إذا لم يكن موجوداً)
cat > .dockerignore << 'EOF'
# Git
.git
.gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Documentation
README.md
docs/
*.md

# Docker
Dockerfile*
docker-compose.yml
.dockerignore

# CI/CD
.github/
.gitlab-ci.yml
.travis.yml
.circleci/

# Testing
.coverage
.pytest_cache/
.tox/
htmlcov/

# Logs and data
logs/
data/
exports/
backups/
*.log
*.db
*.sqlite
*.sqlite3

# Temporary files
*.tmp
*.temp
tmp/

# Build artifacts
build/
bin/
*.apk
*.aab

# Environment files
.env
.env.local
.env.production

# Cache
.cache/
.npm/
.yarn/

# Node modules
node_modules/
package-lock.json
yarn.lock

# Android
android-*/
.gradle/
gradle/
local.properties

# User data
user_input_files/
monitoring_data/
activity_logs/
EOF

# جعل الملفات قابلة للتنفيذ
chmod +x setup.sh

echo "✅ تم إنشاء مجلد المستودع: stealth-network-monitor"
echo ""
echo "📋 الملفات المنشأة:"
echo "├── stealth_network_spy_fixed.py"
echo "├── main.py"
echo "├── buildozer.spec"
echo "├── config.yaml"
echo "├── README.md"
echo "├── requirements.txt"
echo "├── .gitignore"
echo "├── LICENSE"
echo "├── setup.sh"
echo "├── docker-compose.yml"
echo "├── Dockerfile"
echo "├── .dockerignore"
echo "├── CHANGELOG.md"
echo "├── CONTRIBUTING.md"
echo "├── CODE_OF_CONDUCT.md"
echo "├── SECURITY.md"
echo "├── mobile_config_ready.json"
echo "└── .github/workflows/ci-cd.yml"
echo ""
echo "🎉 جميع الملفات جاهزة للرفع على GitHub!"
echo ""
echo "الخطوات التالية:"
echo "1. cd stealth-network-monitor"
echo "2. git init"
echo "3. git add ."
echo "4. git commit -m 'Initial commit: Stealth Network Monitor'"
echo "5. git branch -M main"
echo "6. git remote add origin https://github.com/YOUR_USERNAME/stealth-network-monitor.git"
echo "7. git push -u origin main"
