# Academic Skills

A collection of academic skills for AI coding agents. Skills are packaged instructions that extend agent capabilities for scientific writing, literature research, figure generation, and scholarly communication.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

### nature-polishing

Polish, restructure, or translate academic prose into Nature-leaning English using writing-strategy principles, curated Nature/Nature Communications article patterns, and phrase-level support from Academic Phrasebank.

**Use when:**
- Polishing academic manuscript text
- Translating Chinese academic text to English
- Improving prose to Nature journal standards
- Restructuring sentences for clarity and impact

### nature-writing

Draft, restructure, or plan Nature-style manuscript sections from author-provided claims, results, figures, notes, or Chinese drafts.

**Use when:**
- Writing or rebuilding abstract, introduction, results, discussion, or conclusion
- Planning manuscript argument structure
- Drafting sections from research notes

### nature-figure

Submission-grade Nature/high-impact journal figure workflow for Python or R. Create, revise, audit, or polish manuscript figures and multi-panel scientific plots.

**Use when:**
- Creating publication-quality scientific figures
- Generating multi-panel plots for manuscripts
- Exporting SVG/PDF/TIFF for journal submission
- Auditing figures for Nature compliance

### nature-citation

Add strict Nature/CNS citations to manuscript text by searching accepted flagship and subjournal titles from Nature Portfolio, AAAS Science family, and Cell Press, with reference-manager-ready export.

**Use when:**
- Adding supporting references to manuscript
- Searching CNS-level journal citations
- Exporting citations for Zotero or other reference managers

### nature-data

Prepare, audit, or revise Nature-ready Data Availability statements, data repository plans, dataset citations, and FAIR metadata checklists.

**Use when:**
- Writing Data Availability statements
- Planning data repository uploads
- Checking FAIR metadata compliance
- Preparing dataset citations

### nature-reader

Build full-paper Chinese-English side-by-side, figure/table-aware, source-grounded Markdown readers for journal or conference papers.

**Use when:**
- Converting papers to bilingual Markdown
- Reading full-text papers with figure references
- Translating papers section by section

### nature-response

Draft, audit, or revise point-by-point reviewer response letters for Nature-family manuscript revisions.

**Use when:**
- Writing response to reviewers
- Preparing rebuttal letters
- Revising manuscripts based on review comments

### nature-paper2ppt

Build a complete Nature-style Chinese PPTX presentation from a scientific paper, producing a real .pptx deck with Chinese slide content and speaker notes.

**Use when:**
- Converting papers to presentation slides
- Preparing journal club or group meeting talks
- Generating PPT from PDF or article text

### nature-academic-search

Multi-source literature search, citation verification, MeSH search strategy, citation file management, and reference management via MCP tools.

**Use when:**
- Searching papers across PubMed, CrossRef, arXiv
- Verifying DOIs and citation accuracy
- Managing bibliographies (.nbib/.ris/.bib conversion)
- Coordinating multi-step literature workflows

### scientific-toolkit-skill

Research computing toolkit for MATLAB/Octave, Python scientific analysis, signal processing, image processing, statistics, simulation, optimization, and publication figures.

**Use when:**
- Running MATLAB or Python scientific computations
- Processing signals, images, or time-series data
- Statistical analysis and simulation
- Generating publication figures

### research-writing-skill

Chinese-first research paper writing, revision, polishing, section drafting, rebuttal, peer-review response, and manuscript argument planning.

**Use when:**
- Writing research papers in Chinese
- Drafting or revising manuscript sections
- Preparing peer-review responses

### office-academic-skill

Chinese-first academic Word and PowerPoint workflow for paper reading reports, thesis PPTs, editable DOCX/PPTX generation, and layout quality checks.

**Use when:**
- Generating academic DOCX or PPTX documents
- Creating paper reading reports
- Building thesis defense presentations

## Installation

```bash
npx add-skill ai-tools-mtl/academic-skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
```
Polish this abstract to Nature style
```
```
Create a publication-quality figure from this data
```
```
Build a response letter for these reviewer comments
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
