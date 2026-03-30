# ARCHITECTURE: THE NEXUS_AI ECOSYSTEM 🧠

## 1. The Dynamic Governance Model
NEXUS_AI utilizes a **SelectorGroupChat** hierarchy. This creates a "Managed Autonomy" where the **Orchestrator** acts as the Speaker Selector, ensuring the right specialist is engaged at the right time.

### The Reasoning Loop (The "NEXUS-7" Protocol):
- **Planning Phase**: The `Planner` decomposes the User Prompt into a multi-phase roadmap.
- **Intelligence Phase**: The `Researcher` and `Analyst` work in parallel to gather facts and project feasibility.
- **Execution Phase**: The `Coder` generates and executes local scripts. If the shell returns a non-zero exit code, the Coder enters a self-correction loop.
- **Audit Phase**: The `Critic` performs a "Cold Eye Review" on the outputs. If it detects a hallucination or logic leap, it issues a `REVISE` command.
- **Refinement Phase**: The `Optimizer` refactors the logic for token efficiency and performance speed.
- **Certification Phase**: The `Validator` scans for "Red Flags": hardcoded credentials, PII leaks, or lack of error handling.
- **Synthesis Phase**: The `Reporter` generates a final professional document.

## 2. Advanced State & Memory Management
To handle 50k+ document RAG pipelines or complex startup plans, NEXUS_AI implements **Isolated Context Windows**:
- **Agent-Specific Buffers**: We use `BufferedChatCompletionContext` to ensure agents stay focused on their current sub-task without being distracted by the entire history.
- **Global Shared Memory**: The `SelectorGroupChat` maintains a shared state for cross-agent collaboration.
- **Memory Recall**: The `Researcher` is equipped with RAG capabilities to pull historical "Day 3" data or external documentation into the current context.

## 3. Resilience & Self-Correction
The system is built on the principle of **Agentic Resilience**. If an agent fails a task, the `Orchestrator` doesn't stop the program; it re-delegates. 
- **Internal Loop**: Coder $\leftrightarrow$ Local Environment (Self-Debugging).
- **External Loop**: Worker $\leftrightarrow$ Critic (Quality Control).
- **Security Loop**: Optimized Output $\leftrightarrow$ Validator (Compliance).