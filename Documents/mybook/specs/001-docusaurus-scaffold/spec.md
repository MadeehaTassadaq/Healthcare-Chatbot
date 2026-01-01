# Chapter Specification: Docusaurus Project Scaffolding

**Feature Branch**: `001-docusaurus-scaffold`
**Created**: 2025-12-15
**Status**: Draft
**Input**: User description: "Book Structure: Intro: The Era of Embodied Intelligence..."

## Implementation Goals & Success Criteria

This specification outlines the requirements for scaffolding a Docusaurus project for the "Physical AI & Humanoid Robotics" book. The primary goal is to automatically generate the necessary configuration files and the complete documentation folder structure based on the user-provided book outline.

**Success is measured by the following criteria:**
- A valid `docusaurus.config.js` file is created.
- A `sidebars.js` file that accurately reflects the book's module/chapter hierarchy is generated.
- A complete `docs/` directory structure is created, with placeholder `.md` files for every chapter.
- The resulting project structure is ready for Docusaurus installation and startup (`npm install && npm start`).

---

## File Generation Requirements

### 1. `docusaurus.config.js`
A configuration file for the Docusaurus site MUST be generated. It should include:
- **title**: 'Physical AI & Humanoid Robotics'
- **tagline**: 'The Era of Embodied Intelligence'
- **url**: A placeholder (e.g., 'https://.github.io')
- **baseUrl**: A placeholder (e.g., '/physical-ai-robotics-book/')
- **organizationName**: A placeholder (e.g., 'your-username')
- **projectName**: 'physical-ai-robotics-book'
- Standard presets and a basic theme configuration.

### 2. `sidebars.js`
A sidebar configuration file MUST be generated to create the book's navigation structure. The structure MUST match the following hierarchy:

- **Intro**: The Era of Embodied Intelligence
- **Module 1**: The Robotic Nervous System (ROS 2)
  - Ch 1: ROS 2 Architecture & Workspace Setup
  - Ch 2: Communication Patterns
  - Ch 3: URDF: Building the Humanoid Skeleton
- **Module 2**: The Digital Twin (Gazebo & Unity)
  - Ch 4: Physics Simulation & Gravity
  - Ch 5: Sensor Fusion
- **Module 3**: The AI-Robot Brain (NVIDIA Isaac™)
  - Ch 6: Isaac Sim & Synthetic Data
  - Ch 7: Isaac ROS & Navigation
- **Module 4**: Vision-Language-Action (VLA)
  - Ch 8: Speech-to-Intent
  - Ch 9: LLM Cognitive Planning
- **Capstone**: Building the Autonomous Humanoid

### 3. `/docs` Directory Hierarchy
A directory structure under `docs/` MUST be created to house the chapter content. Empty placeholder files (`.md`) with a basic title frontmatter MUST be generated for each item.

```
docs/
├── intro.md
├── module1/
│   ├── chapter1.md
│   ├── chapter2.md
│   └── chapter3.md
├── module2/
│   ├── chapter4.md
│   └── chapter5.md
├── module3/
│   ├── chapter6.md
│   └── chapter7.md
├── module4/
│   ├── chapter8.md
│   └── chapter9.md
└── capstone.md
```

---

## Key Entities

The primary entities for this task are the files and directories to be generated.

- **`docusaurus.config.js`**: Site-level configuration.
- **`sidebars.js`**: Navigation and structure definition.
- **`docs/`**: The root folder for all content.
  - **`intro.md`**: Placeholder for the book's introduction.
  - **`module<N>/`**: Directories for each module.
  - **`chapter<N>.md`**: Placeholder markdown files for each chapter.
  - **`capstone.md`**: Placeholder for the final project chapter.
