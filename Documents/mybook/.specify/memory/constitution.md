<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- List of modified principles: None.
- Added sections: ## Technical Standards
- Removed sections: None.
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: None.
-->
# Physical-AI-Humanoid-Robotics-Book Constitution

## Core Principles

### I. Technical Accuracy
All content must be technically accurate and grounded in established principles of robotics, artificial intelligence, and control systems. All factual claims must be cited from peer-reviewed sources or official documentation.

### II. Hardware-Software Co-design Focus
The book must emphasize the interplay between hardware and software. Explanations should connect algorithmic concepts to their physical implementation, constraints, and real-world performance.

### III. Clear, Engineering-Oriented Explanations
Explanations must be clear, direct, and tailored to an audience of engineers, researchers, and technical professionals. The target Flesch-Kincaid grade level is 11–13 to ensure accessibility without sacrificing precision. A neutral, academic tone is required.

### IV. Real-World Applicability
Content must be linked to real-world applications and case studies. Theoretical concepts should be illustrated with practical examples from industrial, healthcare, or service robotics to ensure relevance.

### V. Safety, Ethics, and Human-Centered Design
The ethical and safety implications of robotics are a primary concern. All content must address physical safety, AI bias, and human autonomy where relevant. Safety disclaimers must be included where applicable.

## Content and Sourcing Standards

All factual claims MUST be cited. The required citation format is APA. A minimum of 60% of sources must be from peer-reviewed conferences (e.g., ICRA, IROS, RSS) and journals. The remaining sources may include official technical documentation and industry standards. No uncited or speculative claims are permitted. All content is subject to a zero-plagiarism tolerance policy.

## Content Structure

Content must be structured in modular chapters compatible with Docusaurus. Each chapter should be 2,500–4,000 words and include sections on concepts, system architecture, algorithms/models, hardware considerations, case studies, and limitations. The total manuscript length is constrained to 40,000–60,000 words.

## Technical Standards

- **Tech Stack**: The project MUST use Docusaurus (React) for content, Spec-Kit Plus for specification, and Markdown/MDX for writing.
- **Code Snippets**: All code examples and snippets MUST be compatible with ROS 2 Humble or ROS 2 Iron.
- **Diagrams**: All architecture diagrams MUST be created using Mermaid.js.
- **Deployment**: The book MUST be deployed to GitHub Pages using a GitHub Actions workflow.

## Governance

This constitution is the authoritative source for project standards. All contributions must adhere to these principles. All claims must be traceable, technically defensible, and ready for direct Docusaurus publication. Amendments require documentation and approval.

**Version**: 1.1.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-15
