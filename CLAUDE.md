# CLAUDE.md - AI Assistant Guide

This document provides comprehensive guidance for AI assistants (like Claude) working with this codebase. It covers repository structure, development workflows, coding conventions, and best practices.

## Table of Contents

- [Repository Overview](#repository-overview)
- [Codebase Structure](#codebase-structure)
- [Development Workflow](#development-workflow)
- [Coding Conventions](#coding-conventions)
- [Testing Strategy](#testing-strategy)
- [Common Tasks](#common-tasks)
- [AI Assistant Guidelines](#ai-assistant-guidelines)

---

## Repository Overview

### Purpose
**TODO: Describe the main purpose and goals of this repository**

### Tech Stack
**TODO: List the primary technologies, frameworks, and languages used**

Example:
- Language: TypeScript/JavaScript/Python/etc.
- Runtime: Node.js/Deno/Python/etc.
- Framework: React/Express/FastAPI/etc.
- Build Tool: Vite/Webpack/tsc/etc.
- Package Manager: npm/yarn/pnpm/pip/etc.

### Key Dependencies
**TODO: List critical dependencies and their purposes**

---

## Codebase Structure

### Directory Layout

```
TODO: Provide the actual directory structure
Example:
/
├── src/              # Source code
│   ├── components/   # Reusable components
│   ├── services/     # Business logic and services
│   ├── utils/        # Utility functions
│   └── types/        # TypeScript type definitions
├── tests/            # Test files
├── docs/             # Documentation
├── scripts/          # Build and utility scripts
└── config/           # Configuration files
```

### Critical Files

**TODO: Document important configuration and entry point files**

- `package.json` / `pyproject.toml` - Project metadata and dependencies
- `tsconfig.json` / `.eslintrc` - Language and linting configuration
- Entry points, configuration files, etc.

### Module Organization

**TODO: Explain how code is organized into modules/packages**

---

## Development Workflow

### Initial Setup

**TODO: Provide setup instructions**

```bash
# Example:
# 1. Install dependencies
npm install

# 2. Set up environment variables
cp .env.example .env

# 3. Run initial build
npm run build
```

### Common Commands

**TODO: Document frequently used commands**

```bash
# Development
npm run dev          # Start development server
npm run build        # Production build
npm run test         # Run tests
npm run lint         # Lint code
npm run format       # Format code
npm run typecheck    # Type checking
```

### Git Workflow

**TODO: Describe branching strategy and commit conventions**

#### Branch Naming
- Feature branches: `feature/description` or `claude/description-XXXXX`
- Bug fixes: `fix/description`
- Refactoring: `refactor/description`

#### Commit Messages
Follow conventional commits format:
```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
```

### Build Process

**TODO: Explain the build pipeline**

1. Type checking
2. Linting
3. Testing
4. Compilation/bundling
5. Asset optimization

---

## Coding Conventions

### Style Guide

**TODO: Document code style preferences**

#### General Principles
- Write clear, self-documenting code
- Prefer simple solutions over clever ones
- Follow DRY (Don't Repeat Yourself) when it makes sense
- Comment only when the "why" isn't obvious from the code

#### Naming Conventions

**TODO: Specify naming patterns**

```typescript
// Example:
// Variables and functions: camelCase
const userName = 'example';
function getUserData() {}

// Classes and Types: PascalCase
class UserService {}
type UserData = {};

// Constants: UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;

// Files: kebab-case or camelCase
// user-service.ts or userService.ts
```

#### Code Organization

**TODO: Describe how to organize code within files**

- Import ordering (external, internal, types, etc.)
- Function ordering
- File size limits
- When to split files

### TypeScript/Type Patterns

**TODO: Document type-related conventions**

- When to use interfaces vs types
- How to handle null/undefined
- Generic usage patterns
- Type inference guidelines

### Error Handling

**TODO: Document error handling patterns**

```typescript
// Example patterns:
// - When to throw vs return errors
// - Error types to use
// - Logging conventions
```

### Async Patterns

**TODO: Document async/await conventions**

- When to use async/await vs promises
- Error handling in async code
- Concurrency patterns

---

## Testing Strategy

### Test Structure

**TODO: Explain testing approach**

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/           # End-to-end tests
```

### Testing Conventions

**TODO: Document testing best practices**

- Test file naming: `*.test.ts` or `*.spec.ts`
- Test organization: describe/it blocks
- Mocking strategies
- Coverage requirements

### Running Tests

```bash
# TODO: Add actual test commands
npm test              # Run all tests
npm test:unit         # Unit tests only
npm test:integration  # Integration tests
npm test:watch        # Watch mode
npm test:coverage     # With coverage report
```

---

## Common Tasks

### Adding a New Feature

**TODO: Step-by-step guide for adding features**

1. Create feature branch
2. Implement feature
3. Add tests
4. Update documentation
5. Create pull request

### Fixing a Bug

**TODO: Bug fix workflow**

1. Reproduce the bug
2. Write failing test
3. Fix the bug
4. Verify test passes
5. Check for related issues

### Refactoring

**TODO: Safe refactoring practices**

1. Ensure tests exist and pass
2. Make incremental changes
3. Run tests after each change
4. Update documentation if needed

### Adding Dependencies

**TODO: Dependency management guidelines**

```bash
# Add production dependency
npm install package-name

# Add dev dependency
npm install -D package-name

# Consider:
# - Bundle size impact
# - Maintenance status
# - License compatibility
# - Security vulnerabilities
```

---

## AI Assistant Guidelines

### Code Reading Best Practices

1. **Always read files before modifying**: Never propose changes to code you haven't read
2. **Understand context**: Read related files to understand how code fits together
3. **Check existing patterns**: Follow established patterns in the codebase

### Making Changes

1. **Minimal changes**: Only change what's necessary for the task
2. **No over-engineering**: Don't add features or abstractions beyond what's requested
3. **Follow existing style**: Match the coding style of surrounding code
4. **Preserve formatting**: Maintain consistent indentation and spacing

### Security Considerations

**TODO: Document security-sensitive areas**

- Input validation requirements
- Authentication/authorization patterns
- Data sanitization
- Common vulnerabilities to avoid (XSS, SQL injection, etc.)

### What NOT to Do

1. **Don't add unnecessary features**: Stick to the requested changes
2. **Don't refactor unrequested code**: Fix bugs without cleaning up surrounding code
3. **Don't add comments to unchanged code**: Only comment new or modified logic when needed
4. **Don't add premature optimizations**: Solve the current problem simply
5. **Don't create unused abstractions**: Three similar lines > premature abstraction
6. **Don't add backward compatibility hacks**: Delete unused code completely

### File Organization Preferences

**TODO: Document preferences for file operations**

- Prefer editing existing files over creating new ones
- When to split large files
- How to organize imports
- Where to place different types of code

### Communication

- Use clear, concise messages
- Reference specific files and line numbers: `file.ts:123`
- Explain "why" not just "what" when making changes
- Ask questions when requirements are unclear

### Tool Usage

**TODO: Document any project-specific tools or scripts**

- Prefer specialized tools over bash commands for file operations
- Use parallel operations when tasks are independent
- Check build/test results after significant changes

---

## Project-Specific Notes

### Special Considerations

**TODO: Document any unique aspects of this project**

- Unusual architectural decisions
- Performance-critical sections
- Legacy code areas requiring special care
- External integrations

### Known Issues

**TODO: Document known limitations or technical debt**

- Areas that need refactoring
- Temporary workarounds
- Browser/environment compatibility issues

### Future Plans

**TODO: Document planned improvements or changes**

- Upcoming migrations
- Planned architecture changes
- Features in development

---

## Resources

### Documentation

**TODO: Link to relevant documentation**

- Internal wiki/docs
- API documentation
- Design documents

### External Resources

**TODO: Link to helpful external resources**

- Framework documentation
- Style guides
- Best practices articles

---

## Changelog

**TODO: Document significant updates to this guide**

- `YYYY-MM-DD` - Initial version created

---

## Contributing to This Document

This document should be updated whenever:
- New conventions are established
- Architecture changes significantly
- New developers (human or AI) struggle with common tasks
- Patterns emerge from code reviews

Keep this document accurate and up-to-date to maximize its value for all contributors.
