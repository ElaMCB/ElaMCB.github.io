# Week 1: Core Prompting & Mental Models

**Goal**: Build reflex-level prompting hygiene

**Time**: ~10 hours (90-minute daily blocks)

---

## Day 1: Prompt Engineering Fundamentals

### Read
- "Prompt Engineering Guide" (promptingguide.ai)
- Focus on: Zero-Shot → Chain-of-Thought progression

### Do
- Replicate every example in the playground
- Change one variable at a time and record delta
- Document what works and what doesn't

### Deliverable
- Playground experiment log with at least 10 variations
- Notes on key patterns discovered

---

## Day 2: Mental Models

### Mental Model
"LLM as an eager intern with a 7-second memory."

### Exercise
Take 5 random Reddit ELI5 questions → write 3 prompts each:
- Zero-shot
- Few-shot
- Chain-of-Thought (CoT)

Pick best and explain why in 1 sentence.

### Deliverable
- 5 Reddit questions with 3 prompt variations each (15 prompts total)
- Best prompt selection with 1-sentence justification per question

---

## Day 3: Failure Modes & Guardrails

### Focus Areas
- Hallucination
- Verbosity
- Format drift

### Drill
1. Intentionally trigger each failure mode
2. Patch with 3 different guardrails:
   - System message
   - Inline instruction
   - Post-parse validation

### Deliverable
- Failure mode examples (3 types)
- Guardrail implementations (3 per failure = 9 total)
- Comparison of effectiveness

---

## Day 4: Temperature & Sampling Deep-Dive

### Task
Generate 50-line Python micro-benchmark that:
- Sweeps temperature (0–1.2) on a closed Q&A set
- Plots exact-match vs temperature
- Identifies optimal temperature range

### Deliverable
- Python script with temperature sweep
- Visualization (plot) showing exact-match vs temperature
- Analysis of optimal temperature for the task

---

## Day 5: Mini-Project - Prompt A/B CLI

### Build
A "Prompt A/B CLI" tool that:
- Takes two prompts + 20 test cases
- Auto-runs both prompts
- Caches results
- Prints win-rate comparison

### Requirements
- Command-line interface
- Test case input (JSON/CSV)
- Results caching
- Win-rate calculation
- Clear output formatting

### Deliverable
- GitHub repo (public)
- Working CLI tool
- README with usage instructions
- At least 20 test cases included

---

## Week 1 Checkpoint

By end of Week 1, you should have:
- [ ] Playground experiment log (10+ variations)
- [ ] 15 prompt variations (5 questions × 3 types)
- [ ] Failure mode analysis with guardrails (9 implementations)
- [ ] Temperature sweep analysis with visualization
- [ ] Prompt A/B CLI tool on GitHub

---

## Resources

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- OpenAI Playground
- Reddit r/explainlikeimfive
- Python plotting libraries (matplotlib, seaborn)

---

## Notes

Track all experiments in your Notion database:
- Prompt text
- Variables changed
- Metrics/results
- URL/link to experiment

