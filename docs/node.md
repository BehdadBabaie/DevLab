# Node.js Environment

## Installed Components

| Tool     | Version |
| -------- | ------- |
| Node.js  | 22.x    |
| npm      | 10.x    |
| Corepack | 0.34.x  |

---

## Verify Installation

```bash
node --version
npm --version
corepack --version
```

---

## Create a Project

```bash
npm init
```

---

## Install Packages

```bash
npm install <package-name>
```

---

## Run

```bash
node index.js
```

## Optional Package Managers

Corepack is installed with Node.js.

To enable pnpm:

```bash
corepack enable
corepack prepare pnpm@latest --activate
```
