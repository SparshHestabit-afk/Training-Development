# WEEK 1 RETROSPECTIVE

## Overview

Week 1 was less about writing a large amount of code and more about learning how to think and work like an engineer. Throughout the week, I focused on understanding how systems behave beneath abstractions, how development tools interact with one another, and how small configuration mistakes can lead to significant failures.

Rather than prioritizing only successful outcomes, the training emphasized **process** — observing behavior, validating assumptions, debugging methodically, and documenting learnings. Many tasks intentionally broke along the way, and those failures became the most valuable learning points. This report documents what I worked on each day, how I approached the tasks, what I learned, and what broke during execution.

---

## Day 1 — System Awareness and Terminal Fundamentals

**Focus:** Understanding the environment before writing code

The first day focused on building awareness of the development environment itself. Instead of relying on IDEs or high-level tooling, I worked primarily from the terminal to understand how the operating system, Node.js runtime, and environment variables interact.

### What I did
- Explored OS-level information using terminal commands  
- Verified Node.js and npm installations and paths  
- Inspected environment variables such as `PATH`  
- Wrote a Node.js script to introspect system and runtime details  
- Compared file processing using buffers versus streams  

### How I did it
I used commands like `uname`, `which`, and environment variable inspection to understand binary resolution. Using Node’s `os` and `process` modules, I created a script that exposed system metadata. To analyze performance, I generated large files and processed them using both buffer-based reads and stream-based reads while observing memory usage and execution time.

### What I learned
- Understanding the runtime environment is essential for debugging 
- Environment variables can silently alter application behavior 
- Streams are significantly more memory-efficient for large files 
- Performance assumptions must be validated with measurements 

### What broke
- Misconfigured `PATH` values caused unexpected runtime resolution 
- Buffer-based file reads caused noticeable memory spikes 

---

## Day 2 — Node.js CLI Tools and Concurrency

**Focus:** Building practical tools and measuring performance

Day 2 shifted from observation to creation. The objective was to build a functional command-line tool and understand how concurrency and input size affect performance.

### What I did
- Generated a large text dataset (file with 200,000+ words)for testing 
- Built a Node.js CLI tool to process text files 
- Added command-line arguments for customization 
- Implemented concurrent processing logic 
- Benchmarked execution under different concurrency levels 

### How I did it
I used file streams to process large files incrementally, avoiding memory overload. Command-line arguments were parsed using `process.argv`. The workload was divided into chunks and processed concurrently using promises, with execution times logged for comparison.

### What I learned
- CLI tools require strong input validation 
- Concurrency improves performance only up to a limit 
- File execution permissions are critical for CLI tools 
- Benchmarking often exposes non-obvious bottlenecks 
- Promise.all vs Worker Threads, difference between them and diff. between CONCURRENCY vs PARALLELISM

### What broke
- The CLI failed to execute due to missing permissions 
- Incorrect chunking logic produced inaccurate results 
- Excessive concurrency reduced performance due to overhead 

---

## Day 3 — Git Workflows and Recovery Techniques

**Focus:** Using Git as a debugging and recovery tool

Day 3 completely changed how I view Git. Instead of seeing it only as a version control system, I learned to use Git as a diagnostic and recovery tool for real-world issues.

### What I did
- Created repositories with intentional regressions 
- Used `git bisect` to locate faulty commits 
- Practiced `git revert` and `git stash` workflows 
- Simulated merge conflicts using multiple clones 
- Explored Git submodule behavior and common errors 

### How I did it
I marked known good and bad commits to guide `git bisect` toward the breaking change. Regressions were fixed using `git revert` to preserve shared history. Stash workflows were used during interrupted pulls, and merge conflicts were resolved manually by reviewing changes carefully.

### What I learned
- Git history can function as a debugging timeline 
- Reverting commits is safer than rewriting history 
- Stash is best suited for short-term recovery 
- Merge conflicts are normal and manageable
- Diff. between RESTORE ,RESET and REVERT
- Concepts and commands like 'git rebase', etc.

### What broke
- Submodules failed due to incorrect folder handling 
- Pulls were blocked by unresolved conflicts 
- Early misuse of stash caused confusion 
- Binary Searching (git bisect) failed due to improper marking and description , which is varrying between good and bad commits

---

## Day 4 — API Investigation and Network Fundamentals

**Focus:** Understanding APIs as distributed systems

Day 4 expanded the scope beyond local systems to include networking. The focus was on understanding how APIs behave over the network and how headers, caching, and routing influence responses.

### What I did
- Performed DNS lookups and traceroutes 
- Investigated APIs using `curl` and Postman 
- Modified request headers to observe server behavior 
- Tested caching using conditional requests 

### How I did it
I used tools like `nslookup` and `traceroute` to analyze network paths. With `curl -v`, I sent requests with varying headers to observe differences in responses. Postman was used to visually inspect and validate API behavior.

### What I learned
- HTTP headers significantly impact server responses 
- Caching mechanisms reduce unnecessary network traffic 
- API Pagination can improve performance and time efficiency (speed)
- Network-level tools complement application-level testing 

### What broke
- Missing headers caused unexpected API behavior 
- Incorrect caching assumptions led to confusion 
- API responses varied across tools without proper configuration 

---

## Day 5 — Automation, Validation, and Pre-Commit Enforcement

**Focus:** Preventing errors through automation

The final day consolidated the week’s learning into automation and quality enforcement. The goal was to prevent issues before code reached the repository by enforcing checks automatically.

### What I did
- Created a validation shell script to enforce project structure 
- Integrated ESLint and Prettier 
- Configured Husky pre-commit hooks 
- Generated build artifacts with checksums 
- Explored scheduling concepts using cron 

### How I did it
Shell scripts were written to validate conditions and exit with non-zero codes on failure. ESLint was configured using the latest configuration format, and Husky hooks were set up to run validation and linting before commits. Build artifacts were created using `tar` and verified using SHA256 checksums.

### What I learned
- Automation enforces consistency and discipline 
- Git hooks always execute from the repository root 
- Tooling versions can significantly impact configuration 
- Build artifacts improve reproduce ability and traceability 
- Learned about concepts like linters, CI/CD pipeline (for automation), hsuky, etc.

### What broke
- Husky hooks initially failed due to deprecated syntax 
- Hooks did not run when paths were misconfigured 
- ESLint failed when outdated configuration formats were used 
- Husky didn't worked and was unable to click/link with git due to path issues (as I created and initialized it in repo inside a repo, raising a sumodule inconsistency)

---

## Final Takeaways

By the end of Week 1, my mindset shifted from simply completing tasks to understanding systems holistically. Debugging became less intimidating as I learned to approach problems methodically. The repeated cycle of failure, investigation, and correction reinforced the importance of discipline, documentation, and automation.

This week established a strong foundation for future learning and provided hands-on experience with real-world engineering challenges.

