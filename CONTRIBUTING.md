# Contributing to ENCODEfetch

🎉 First of all, thank you for your interest in contributing to **ENCODEfetch**!  
Contributions from the community are what make open-source tools like this thrive.

This document provides guidelines for contributing code, documentation, or ideas.

---

## 📌 Ways to contribute

- **Report bugs** by opening [GitHub issues](https://github.com/khan-lab/ENCODEfetch/issues).
- **Suggest features** or improvements through an issue or a discussion.
- **Improve documentation** (README, docs/, examples, API references).
- **Submit code** via pull requests (PRs).

---

## 🛠️ Development setup

1. **Fork & clone** the repository:

   ```bash
   git clone https://github.com/YOUR-USERNAME/ENCODEfetch.git
   cd ENCODEfetch
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -e .[dev]
   ```

4. **Install docs dependencies** (optional):
   ```bash
   pip install -r docs/requirements.txt
   ```

---

## 🧪 Testing

We use **pytest** for testing.

```bash
pytest -v
```

Before submitting a PR, ensure:

- All tests pass (`pytest`).
- Code coverage is not reduced.
- New features have corresponding tests.

---

## 🎨 Code style

- Follow [PEP8](https://peps.python.org/pep-0008/) for formatting.
- Use [black](https://github.com/psf/black) for auto-formatting:
  ```bash
  black encodefetch tests
  ```
- Use [isort](https://pycqa.github.io/isort/) for imports:
  ```bash
  isort encodefetch tests
  ```
- Use [flake8](https://flake8.pycqa.org/) for linting:
  ```bash
  flake8 encodefetch tests
  ```

---

## 📚 Documentation

- Documentation lives in [`docs/`](docs/).
- Built with **Sphinx + MyST Markdown** and hosted on GitHub Pages.
- To build docs locally:
  ```bash
  cd docs
  make html
  open _build/html/index.html
  ```

---

## 🔀 Pull requests

1. Create a new branch:

   ```bash
   git checkout -b feature/my-feature
   ```

2. Commit changes with a clear message:

   ```bash
   git commit -m "Add feature: my-feature"
   ```

3. Push to your fork and open a PR:

   ```bash
   git push origin feature/my-feature
   ```

4. In your PR description, reference related issues (e.g., `Fixes #42`).

---

## ✅ PR checklist

- [ ] Tests added/updated and all passing
- [ ] Lint/formatting checks passing
- [ ] Documentation updated (README and/or docs/)
- [ ] PR description clearly explains changes
- [ ] Linked to relevant issue(s)

---

## 🤝 Code of conduct

Please note that this project follows the [Contributor Covenant](https://www.contributor-covenant.org/).  
By participating, you agree to uphold our community standards of respect, inclusivity, and collaboration.

---

## 📧 Questions?

- GitHub Issues: <https://github.com/khan-lab/ENCODEfetch/issues>
- Maintainer: [Aziz Khan](https://github.com/aziz-khan)

---

💡 Tip: even small improvements (fixing typos, adding examples, clarifying docs) are valuable contributions!
