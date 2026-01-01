# Tasks: Docusaurus Project Scaffolding

**Input**: Design documents from `specs/001-docusaurus-scaffold/`

## Phase 1: Project Initialization

**Purpose**: Create the base Docusaurus project structure.

- [x] T001 Run `npx create-docusaurus@latest physical-ai-robotics-book classic` to initialize the project in a new directory.

---

## Phase 2: Core Configuration

**Purpose**: Configure the project with the book's specific details and navigation structure. This phase assumes T001 is complete and the working directory is `physical-ai-robotics-book/`.

- [x] T002 Update `docusaurus.config.js` with the correct project details (title: "Physical AI & Humanoid Robotics", organizationName: "[Your-GitHub-Username]", projectName: "physical-ai-book", deploymentBranch: "gh-pages").
- [x] T003 [P] Create the `sidebars.js` file with the full navigation structure mapping to the chapter files.
- [x] T004 [P] Delete the default `docs/` and `blog/` directories created by the initializer.

---

## Phase 3: Content Structure Generation

**Purpose**: Create the entire folder and file hierarchy for the book content.

- [x] T005 [P] Create directory `docs/module1/`.
- [x] T006 [P] Create directory `docs/module2/`.
- [x] T007 [P] Create directory `docs/module3/`.
- [x] T008 [P] Create directory `docs/module4/`.
- [x] T009 [P] Create `docs/module1/_category_.json` with label "Module 1: The Robotic Nervous System (ROS 2)" and position 2.
- [x] T010 [P] Create `docs/module2/_category_.json` with label "Module 2: The Digital Twin (Gazebo & Unity)" and position 3.
- [x] T011 [P] Create `docs/module3/_category_.json` with label "Module 3: The AI-Robot Brain (NVIDIA Isaac™)" and position 4.
- [x] T012 [P] Create `docs/module4/_category_.json` with label "Module 4: Vision-Language-Action (VLA)" and position 5.
- [x] T013 [P] Create placeholder file `docs/intro.md` with frontmatter title "The Era of Embodied Intelligence".
- [x] T014 [P] Create placeholder file `docs/module1/chapter1.md` with frontmatter title "ROS 2 Architecture & Workspace Setup".
- [x] T015 [P] Create placeholder file `docs/module1/chapter2.md` with frontmatter title "Communication Patterns (Nodes, Topics, Services, Actions)".
- [x] T016 [P] Create placeholder file `docs/module1/chapter3.md` with frontmatter title "URDF: Building the Humanoid Skeleton".
- [x] T017 [P] Create placeholder file `docs/module2/chapter4.md` with frontmatter title "Physics Simulation & Gravity in Gazebo".
- [x] T018 [P] Create placeholder file `docs/module2/chapter5.md` with frontmatter title "Sensor Fusion: LiDAR, IMUs, and Depth Cameras".
- [x] T019 [P] Create placeholder file `docs/module3/chapter6.md` with frontmatter title "Isaac Sim & Synthetic Data Generation".
- [x] T020 [P] Create placeholder file `docs/module3/chapter7.md` with frontmatter title "Isaac ROS: Accelerated VSLAM & Nav2".
- [x] T021 [P] Create placeholder file `docs/module4/chapter8.md` with frontmatter title "Speech-to-Intent with OpenAI Whisper".
- [x] T022 [P] Create placeholder file `docs/module4/chapter9.md` with frontmatter title "LLM Cognitive Planning for Robotics".
- [x] T023 [P] Create placeholder file `docs/capstone.md` with frontmatter title "Capstone: Building the Autonomous Humanoid".

---

## Phase 4: Initial Content and Deployment Setup

**Purpose**: Populate the first chapter and create the deployment workflow.

- [x] T024 Populate `docs/module1/chapter1.md` with foundational content on "Physical AI" and a guide for ROS 2 installation.
- [x] T025 Create the GitHub Actions workflow file at `.github/workflows/deploy.yml` for automatic deployment to GitHub Pages.

---

## Phase 5: Verification and Final Audit

**Purpose**: Ensure the project is working and auditable.

- [x] T026 Run `npm install` inside the `physical-ai-robotics-book` directory.
- [x] T027 Run `npm run build` to confirm the Docusaurus site builds successfully.
- [x] T028 Perform a final audit for technical accuracy in the "Cognitive Planning" section (placeholder for future content).

---

## Dependencies & Execution Order

- **Phase 1** must complete before all other phases.
- **Phase 2** tasks can begin after Phase 1. T002-T004 are parallel.
- **Phase 3** tasks can begin after Phase 2. All T005-T023 tasks can run in parallel.
- **Phase 4** can begin after Phase 3.
- **Phase 5** is the final verification step.