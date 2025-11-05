# Guide: Pushing to GitHub Repository

This guide walks you through pushing this restructured code to your GitHub repository: `https://github.com/NeuArv/hybrid-bci-wheelchair`

## Prerequisites

- Git installed on your system
- GitHub account with access to the repository
- Code restructuring completed (you're here!)

## Step-by-Step Instructions

### 1. Navigate to the Project Directory

```bash
cd BrainControlledWheelchair-master
```

### 2. Initialize Git Repository (if not already done)

```bash
# Initialize git
git init

# Check current remote (if any)
git remote -v

# If remote exists but points to wrong URL, update it:
git remote set-url origin https://github.com/NeuArv/hybrid-bci-wheelchair.git

# If no remote exists, add it:
git remote add origin https://github.com/NeuArv/hybrid-bci-wheelchair.git
```

### 3. Review Files to be Committed

```bash
# Check status
git status

# Review what files will be added
git add --dry-run .
```

### 4. Stage All New Files

```bash
# Add all files (respects .gitignore)
git add .

# Or add specific directories:
git add src/ scripts/ tests/ docs/ .github/
git add README.md LICENSE requirements.txt setup.py
git add CITATION.* NOTICES.md CONTRIBUTING.md
```

### 5. Verify Staged Files

```bash
# See what's staged
git status

# Make sure these old files are NOT staged (they're replaced by new structure):
# - Old run.py, blink.py, motor.py, ultrasonic.py in root
# - Old NeuroPy/ directory in root
```

### 6. Create Initial Commit

```bash
git commit -m "feat: Restructure project for hybrid-bci-wheelchair repository

- Reorganize code into proper Python package structure (src/hybrid_bci/)
- Move NeuroPy library to package subdirectory
- Create modular components: motor_control, blink_detection, obstacle_detection
- Add comprehensive documentation (API, hardware setup guide)
- Include test suite with pytest
- Add GitHub Actions CI/CD workflow
- Update README with installation and usage instructions
- Add proper Python packaging (setup.py, requirements.txt)
- Include citation files (CITATION.cff, CITATION.bib)
- Add contributing guidelines and notices"
```

### 7. Push to GitHub

```bash
# Push to master branch
git push -u origin master

# If the branch is called 'main' instead:
git push -u origin main

# If you get errors about divergent branches:
git pull --rebase origin master
# Resolve any conflicts, then:
git push origin master
```

### 8. If Repository Already Has Content

If the GitHub repository already has files, you may need to force push (⚠️ **WARNING**: This will overwrite remote content):

```bash
# ONLY if you're sure you want to replace everything on GitHub
git push -f origin master
```

**Alternative (safer)**: Merge with existing content:

```bash
# Pull existing content
git pull origin master --allow-unrelated-histories

# Resolve any conflicts manually
# Then commit the merge:
git commit -m "merge: Combine restructured code with existing repository"

# Push
git push origin master
```

## Post-Push Checklist

After pushing, verify on GitHub:

- [ ] Repository structure matches expected layout
- [ ] README.md displays correctly on GitHub home page
- [ ] GitHub Actions workflow appears in Actions tab
- [ ] All directories are present: src/, scripts/, tests/, docs/
- [ ] LICENSE file is recognized by GitHub
- [ ] CITATION.cff is recognized (check repository sidebar)

## Creating a Release (Optional)

To create an official release:

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial hybrid BCI wheelchair implementation"
git push origin v1.0.0
```

Then on GitHub:
1. Go to "Releases"
2. Click "Draft a new release"
3. Select the tag v1.0.0
4. Add release notes
5. Publish release

## Updating Repository Settings (on GitHub)

After pushing, configure these on GitHub:

1. **Repository Description**: Add description and topics
   - Settings → About → Description: "Hybrid BCI Wheelchair Control System using EEG, blink detection, and obstacle avoidance"
   - Topics: `bci`, `eeg`, `wheelchair`, `neurosky`, `raspberry-pi`, `assistive-technology`

2. **Enable Issues**: Settings → Features → Issues ✓

3. **Enable Discussions**: Settings → Features → Discussions ✓

4. **Branch Protection** (optional): Settings → Branches → Add rule
   - Require pull request reviews
   - Require status checks to pass

5. **GitHub Actions**: Should auto-enable after first push with workflow

## Troubleshooting

### Authentication Issues

If you get authentication errors:

```bash
# Use personal access token (recommended)
# When prompted for password, use your GitHub personal access token

# Or configure SSH:
git remote set-url origin git@github.com:NeuArv/hybrid-bci-wheelchair.git
```

### Large Files

If you get errors about large files (like the PDF):

```bash
# Remove large files from staging
git rm --cached "Mindwave Automation.pdf"

# Add to .gitignore
echo "*.pdf" >> .gitignore
echo "Mindwave Automation.pdf" >> .gitignore

# Commit and push
git add .gitignore
git commit -m "chore: Remove large PDF file, update gitignore"
git push origin master
```

### Cleaning Old Files

If old files from previous structure appear:

```bash
# Remove from git tracking
git rm blink.py motor.py run.py ultrasonic.py
git rm -r NeuroPy/

# Commit removal
git commit -m "chore: Remove old structure files (replaced by src/ package)"

# Push
git push origin master
```

## Verification Commands

After pushing, verify everything worked:

```bash
# Clone fresh copy to test
cd /tmp
git clone https://github.com/NeuArv/hybrid-bci-wheelchair.git test-clone
cd test-clone

# Check structure
ls -la

# Try installation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

## Next Steps

After successfully pushing:

1. **Update Repository README**: Ensure it displays well on GitHub
2. **Add README badges**: Build status, coverage, license
3. **Write release notes**: Document what's included
4. **Share with collaborators**: Invite team members
5. **Set up project board**: Track issues and features
6. **Add wiki pages**: Detailed tutorials and guides

## Need Help?

- GitHub Docs: https://docs.github.com/
- Git Docs: https://git-scm.com/doc
- Project Issues: https://github.com/NeuArv/hybrid-bci-wheelchair/issues

---

**Congratulations!** Your hybrid BCI wheelchair code is now on GitHub! 🎉

