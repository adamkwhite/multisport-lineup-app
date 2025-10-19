Wrap up

Tasks
- Clean up root directory structure according to <dirStructure>
- Deactivate any virtual environments you created
- Consolidate test files if necessary
- Update todo.md with any outstanding tasks
- Update docs/archive/CHANGELOG.md with detailed session notes
- Update CLAUDE.md "Recent Changes" section with brief summary (keep concise, detailed history in CHANGELOG)
- Use the claude memory mcp to store learnings
- Create a final PR after making these updates


<dirStructure>
$PROJECT_NAME/
├── ai_docs/                # AI specific documentation
├── src/                    # Application source code
├── tests/                  # Unit and integration tests
├── docs/                   # Documentation and design materials
│   └── archive/            # Archived documentation including CHANGELOG.md
├── scripts/                # Build and deployment scripts
├── README.md               # Project overview and quick start
├── claude.md               # Project context for Claude AI (concise)
└── prd-$PROJECT_NAME.md    # Product Requirements Document (if applicable)
</dirStructure>

## Updates to consider

### For <project>/CLAUDE.md "Recent Changes" section:
- Add brief session summary (3-5 bullet points max)
- Keep token-efficient (this file is loaded in every session)
- Detailed history goes in CHANGELOG.md instead

### For <project>/docs/archive/CHANGELOG.md:
- Add detailed session entry with date
- Include all PRs, issues, commits
- List all changes, learnings, and code quality improvements
- Format: "## YYYY-MM-DD (Session N): Brief Title"

### Other sections to update in CLAUDE.md if needed:
- Current Status: Where you are in the development process
- Current Branch: Which branch we were last working on
- Implementation Details: Current architecture and design decisions
- Next Steps: What you plan to implement or change next
- Known Issues: Current bugs or limitations you're aware of
