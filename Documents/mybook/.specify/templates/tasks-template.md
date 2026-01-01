---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Objective] Description`

- **[P]**: Can be done in parallel (e.g., researching different claims)
- **[Objective]**: Which learning objective this task belongs to (e.g., LO1, LO2)
- Include exact file paths or document sections in descriptions.

## Path Conventions

- Chapter content: `docs/chapters/[chapter-name]/index.md`
- Chapter assets: `docs/chapters/[chapter-name]/assets/`
- Sources/bibliography: `docs/sources.bib`

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /sp.tasks command MUST replace these with actual tasks based on:
  - Learning Objectives from spec.md
  - Content Requirements from spec.md
  
  Tasks MUST be organized by learning objective so each can be:
  - Researched independently
  - Drafted independently
  - Validated against success criteria
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Research and Outlining (Shared Infrastructure)

**Purpose**: Creating the chapter's skeleton and gathering all necessary sources.

- [ ] T001 Create chapter file structure in `docs/chapters/[chapter-name]/`.
- [ ] T002 Develop a detailed, hierarchical outline for the chapter in `docs/chapters/[chapter-name]/outline.md`.
- [ ] T003 [P] Gather initial list of peer-reviewed papers and official docs for all claims. Add to `docs/sources.bib`.
- [ ] T004 Define all key concepts/entities that will be discussed.

**Checkpoint**: Outline is complete and a sufficient number of initial sources have been gathered.

---

## Phase 2: Drafting by Learning Objective

### Learning Objective 1 - [Title] (Priority: P1) 🎯 Core Content

**Goal**: [Brief description of what the reader will learn]

**Verification Tasks for LO1**:
- [ ] T010 [P] [LO1] Find and cite 3 peer-reviewed sources for the central claim in this section.
- [ ] T011 [P] [LO1] Verify technical accuracy of all algorithms/models with a second source.

**Drafting Tasks for LO1**:
- [ ] T012 [P] [LO1] Write the "Concepts" section related to this objective.
- [ ] T013 [P] [LO1] Write the "Algorithms/Models" section.
- [ ] T014 [LO1] Write the "Case Study" that demonstrates this objective in a real-world context.
- [ ] T015 [LO1] Draft the "Limitations" section for this topic.

**Checkpoint**: The content for Learning Objective 1 is drafted and all claims are cited.

---

### Learning Objective 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what the reader will learn]

**Verification Tasks for LO2**:
- [ ] T020 [P] [LO2] Find and cite primary sources for all hardware considerations.

**Drafting Tasks for LO2**:
- [ ] T021 [P] [LO2] Write the "Hardware Considerations" section.
- [ ] T022 [LO2] Write the "System Architecture" section, connecting software to the hardware.

**Checkpoint**: The content for Learning Objective 2 is drafted and all claims are cited.

---

[Add more learning objective phases as needed]

---

## Phase 3: Review and Finalization

**Purpose**: Polishing the chapter to meet all quality standards from the constitution.

- [ ] T100 Fact-check every claim in the chapter against its cited source.
- [ ] T101 Review the entire chapter for clarity, tone, and flow.
- [ ] T102 Run a Flesch-Kincaid grade level check on the text.
- [ ] T103 [P] Create textual descriptions for all diagrams and images using Mermaid.js.
- [ ] T104 Format all content for Docusaurus, including frontmatter and internal links.
- [ ] T105 Final review of all citations and bibliography format (APA).
- [ ] T106 Final plagiarism check.

---

## Phase 4: Deployment

**Purpose**: Publishing the book to GitHub Pages.

- [ ] T200 Configure GitHub Actions workflow for Docusaurus deployment.
- [ ] T201 Deploy book to GitHub Pages and verify the live site.

---

## Strategy

1.  **Outline First**: Complete the Research and Outlining phase before any drafting begins. A solid outline prevents rework.
2.  **Draft by Objective**: Draft the content for each Learning Objective incrementally. This allows for focused work.
3.  **Verify as You Go**: Don't leave all sourcing and fact-checking to the end. The "Verification Tasks" in each phase should be done alongside drafting.
4.  **Final Review is Critical**: The review and finalization phase is non-negotiable and ensures all constitutional requirements are met.
5.  **Deploy**: Once the content is finalized, deploy it.
