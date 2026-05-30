# Weak Cryptography SAST

A lightweight, modular Static Application Security Testing (SAST) engine focused on detecting weak and insecure cryptographic implementations across multiple programming languages.

The project parses source code into an intermediate representation (IR), performs static analysis passes such as taint tracking and constant propagation, and applies rule-based security checks to identify cryptographic weaknesses.

---

# Features

- Multi-language parsing using tree-sitter
- Lightweight Intermediate Representation (IR)
- Control Flow Graph (CFG) generation
- Rule-based vulnerability detection
- Taint analysis
- Constant propagation
- SARIF export support
- YAML-based rule definitions
- Extensible analysis pipeline
- Designed specifically for cryptographic security auditing

---

# Targeted Vulnerabilities

The engine is designed to detect vulnerabilities such as:

## Weak Algorithms

- MD5
- SHA1
- DES
- 3DES
- RC4

## Insecure Modes

- AES ECB mode
- Static IV usage
- Predictable nonces

## Hardcoded Secrets

- Hardcoded AES keys
- Hardcoded salts
- Embedded credentials

## Weak Randomness

- `random.random()` for cryptographic purposes
- Predictable seeds
- Non-cryptographic PRNG usage

## TLS Misconfigurations

- TLS 1.0 / 1.1 usage
- Disabled certificate validation
- Insecure SSL contexts

## KDF Weaknesses

- Low PBKDF2 iteration counts
- Weak bcrypt cost factors
- Missing salt usage

---

# High-Level Architecture

```text
                ┌───────────────────┐
                │   Source Code     │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │   Tree-sitter     │
                │      Parser       │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │   AST Builder     │
                └─────────┬─────────┘
                          │
                          ▼
                ┌───────────────────┐
                │ Intermediate IR   │
                └─────────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│     CFG      │  │ Call Graph   │  │ Symbol Table │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ▼
              ┌────────────────────┐
              │ Analysis Engine    │
              │                    │
              │ • Pattern Matching │
              │ • Taint Tracking   │
              │ • Dataflow         │
              │ • Propagation      │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Rule Engine        │
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Findings / SARIF   │
              └────────────────────┘
```

---

# Project Structure

```text
sast/
├── parser/
│   ├── treesitter_query.py
│   ├── ast_builder.py
│   └── language_registry.py
│
├── ir/
│   ├── nodes.py
│   ├── cfg.py
│   ├── callgraph.py
│   ├── symbols.py
│   └── taint.py
│
├── analysis/
│   ├── matcher.py
│   ├── propagation.py
│   ├── dataflow.py
│   ├── engine.py
│   └── context.py
│
├── rules/
│   ├── crypto/
│   │   ├── md5.yml
│   │   ├── sha1.yml
│   │   ├── des.yml
│   │   ├── ecb.yml
│   │   ├── hardcoded_key.yml
│   │   └── weak_rng.yml
│   │
│   ├── loader.py
│   └── schema.py
│
├── reporting/
│   ├── sarif.py
│   ├── json_report.py
│   └── formatter.py
│
├── cli/
│   ├── main.py
│   └── commands.py
│
├── tests/
│   ├── samples/
│   ├── fixtures/
│   └── unit/
│
├── docs/
│   ├── architecture.md
│   ├── ir.md
│   └── rules.md
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Core Components

---

# 1. Parsing Layer

The parsing layer uses tree-sitter grammars to generate syntax trees for multiple programming languages.

Supported / planned languages:

| Language | Status |
|----------|--------|
| Python | Planned |
| JavaScript | Planned |
| TypeScript | Planned |
| Java | Planned |
| Go | Planned |
| Rust | Planned |
| C/C++ | Planned |

Example:

```python
import hashlib

hashlib.md5(data).hexdigest()
```

Tree-sitter generates a concrete syntax tree which is normalized into a language-independent AST.

---

# 2. AST Builder

The AST builder converts tree-sitter nodes into simplified semantic nodes.

Example transformation:

## Input

```python
hashlib.md5(password.encode()).hexdigest()
```

## Internal AST

```text
CallExpression(
    target="hashlib.md5",
    arguments=[
        CallExpression(
            target="password.encode"
        )
    ]
)
```

This abstraction allows rules to work across multiple languages.

---

# 3. Intermediate Representation (IR)

The IR is the central structure used during analysis.

It stores:

- Function calls
- Variable assignments
- Imports
- Constants
- Branches
- Symbol references
- Dataflow edges

Example IR:

```text
AssignNode(
    target="key",
    value="1234567890123456"
)

CallNode(
    function="AES.new",
    arguments=["key"]
)
```

---

# 4. Control Flow Graph (CFG)

The CFG models possible execution paths.

Used for:

- Reachability analysis
- Branch-sensitive checks
- Flow-sensitive analysis
- Taint propagation

Example:

```text
START
  │
  ▼
Read Input
  │
  ▼
If condition
 ├──► Branch A
 └──► Branch B
  │
  ▼
Encrypt Data
  │
  ▼
END
```

---

# 5. Call Graph

Tracks relationships between functions.

Used for:

- Interprocedural analysis
- Cross-function taint tracking
- Sink/source propagation

Example:

```text
main()
 └──► encrypt_password()
         └──► hashlib.md5()
```

---

# 6. Taint Analysis

Tracks sensitive data through the application.

## Example Flow

```python
password = request.POST["password"]
digest = hashlib.md5(password.encode()).hexdigest()
```

Taint path:

```text
User Input
   │
   ▼
password
   │
   ▼
hashlib.md5()
```

This allows the engine to prioritize exploitable findings.

---

# 7. Constant Propagation

Tracks compile-time constants through assignments and expressions.

Useful for detecting:

- Hardcoded encryption keys
- Static salts
- Constant IVs
- Embedded secrets

Example:

```python
KEY = "1234567890123456"

cipher = AES.new(KEY)
```

The analysis engine propagates constant values through the CFG.

---

# 8. Rule Engine

Rules are defined using YAML.

Example rule:

```yaml
id: weak-md5
title: MD5 Usage
severity: HIGH
description: MD5 is cryptographically broken.

match:
  type: call
  pattern: hashlib.md5

message: |
  MD5 should not be used for security-sensitive hashing.

references:
  - https://cwe.mitre.org/data/definitions/327.html
  - https://owasp.org/www-community/vulnerabilities/Weak_hashing_algorithm
```

---

# Rule Format

## Basic Schema

```yaml
id: rule-id
title: Human readable title
severity: LOW | MEDIUM | HIGH | CRITICAL

match:
  type: call | assignment | import
  pattern: some.pattern

message: Human readable explanation
```

---

# Example Rules

## MD5 Detection

```yaml
id: weak-md5
title: MD5 Usage
severity: HIGH

match:
  type: call
  pattern: hashlib.md5

message: MD5 is cryptographically insecure.
```

---

## ECB Detection

```yaml
id: aes-ecb
title: AES ECB Mode
severity: HIGH

match:
  type: call
  pattern: AES.MODE_ECB

message: ECB mode leaks structural information.
```

---

## Hardcoded Key

```yaml
id: hardcoded-key
title: Hardcoded AES Key
severity: CRITICAL

match:
  type: assignment
  pattern: key

constraints:
  entropy: low

message: Hardcoded cryptographic key detected.
```

---

# Example Detection

## Vulnerable Code

```python
import hashlib

password = "admin123"
digest = hashlib.md5(password.encode()).hexdigest()
```

## Output

```text
[HIGH] weak-md5

MD5 is cryptographically insecure.

File: app.py
Line: 4
Column: 10
```

---

# SARIF Output

The engine exports findings in SARIF format for integration with:

- GitHub Code Scanning
- GitLab Security
- Azure DevOps
- CI/CD pipelines

Example:

```bash
python -m cli.main scan ./project --format sarif
```

Generated file:

```text
results.sarif
```

---

# Installation

---

# Requirements

- Python 3.12+
- Git
- GCC / Clang build tools

---

# Clone Repository

```bash
git clone https://github.com/yourusername/weak-crypto-sast.git

cd weak-crypto-sast
```

---

# Create Virtual Environment

## Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Example requirements.txt

```text
tree-sitter
tree-sitter-language-pack
pyyaml
rich
sarif-om
networkx
```

---

# Usage

---

# Scan a Project

```bash
python -m cli.main scan ./example_project
```

---

# Scan Specific File Types

```bash
python -m cli.main scan ./project --lang python
```

---

# Export SARIF

```bash
python -m cli.main scan ./project --format sarif
```

---

# Export JSON

```bash
python -m cli.main scan ./project --format json
```

---

# Run Specific Rules

```bash
python -m cli.main scan ./project --rules weak-md5,aes-ecb
```

---

# Enable Debug Logging

```bash
python -m cli.main scan ./project --debug
```

---

# Example CLI Output

```text
[HIGH] weak-md5
File: app.py
Line: 12

MD5 is cryptographically insecure.
```

---

# Planned Features

## Near-Term

- Python support
- Rule matching engine
- SARIF generation
- CFG generation
- Taint propagation

## Mid-Term

- JavaScript support
- Interprocedural analysis
- Symbol resolution
- Incremental scanning

## Long-Term

- SSA form
- Symbolic execution
- IDE plugins
- Autofix suggestions
- AI-assisted rule generation

---

# Performance Goals

- Fast incremental scans
- Minimal memory overhead
- Parallel analysis pipeline
- Cached parsing
- Lazy CFG construction

---

# Design Principles

- Modular architecture
- Language-agnostic analysis
- Deterministic execution
- Extensible rule system
- Minimal dependencies
- Offline-first scanning

---

# Testing Strategy

The project includes:

- Unit tests
- Parser fixtures
- Vulnerable sample projects
- Rule validation tests
- Regression suites

Example:

```bash
pytest tests/
```

---

# Example Vulnerable Samples

```text
tests/samples/
├── md5_python/
├── ecb_java/
├── weak_rng_js/
└── hardcoded_key_go/
```

---

# Development Workflow

## Run Formatter

```bash
black .
```

## Run Linter

```bash
ruff .
```

## Run Tests

```bash
pytest
```

---

# Contributing

Contributions are welcome.

Areas that need work:

- Additional language support
- Better CFG precision
- More cryptographic rules
- Performance optimization
- Improved taint propagation

---

# Security Disclaimer

This tool is intended for defensive security research and secure software development.

Static analysis cannot guarantee the absence of vulnerabilities and should be combined with:

- Dynamic analysis
- Manual review
- Dependency auditing
- Penetration testing

---

# License

GNU Public License 3.0

---

# Inspiration

Inspired by:

- Semgrep
- CodeQL
- Joern
- Bandit
- SonarQube
- Clang Static Analyzer
```
