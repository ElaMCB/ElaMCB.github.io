# Week 2: Evaluation, Data & Iteration

**Goal**: Show you can prove a prompt is better, not just feel it

**Time**: ~10 hours (90-minute daily blocks)

---

## Day 1: LLM Evaluation Frameworks

### Read
- "Evaluating LLMs" paper
- OpenAI evals repo readme

### Do
- Fork evals repo
- Add a custom eval for "toxicity refusal"
- Use 50 adversarial prompts

### Deliverable
- Forked OpenAI evals repo
- Custom toxicity refusal eval
- 50 adversarial test prompts
- Results summary

---

## Day 2: Metrics Deep-Dive

### Metrics to Implement
- Exact-match
- BLEURT
- BERTScore
- LLM-as-judge

### Task
On your Week 1 Q&A set:
- Compute all four metrics
- Note where LLM-as-judge disagrees with exact-match >10%
- Analyze discrepancies

### Deliverable
- Metric calculations for all 4 types
- Discrepancy analysis report
- Insights on when to use which metric

---

## Day 3: Human-in-the-Loop Label UI

### Build
A cheap "human-in-the-loop" label UI using Streamlit that:
- Lets you swipe left/right on outputs
- Exports to CSV
- Tracks labeling progress

### Features
- Simple swipe interface
- CSV export functionality
- Progress tracking
- Easy to use for non-technical users

### Deliverable
- Streamlit app (deployed or local)
- CSV export functionality
- README with setup instructions
- Example labeled dataset

---

## Day 4: Error Analysis & Prompt Patches

### Task
1. Tag 50 failures into taxonomy:
   - Ambiguity
   - Missing context
   - Format error
   - Safety refusal

2. Write one "prompt patch" per class
3. Measure delta (improvement)

### Deliverable
- Failure taxonomy with 50 examples categorized
- 4 prompt patches (one per failure class)
- Before/after metrics showing improvement
- Analysis of which patches work best

---

## Day 5: Case Study Blog Post

### Write
500-word case study: "Improving summarization recall from 72% → 91% without fine-tuning"

### Structure
- Problem statement
- Initial approach (72% recall)
- Methodology (what changed)
- Results (91% recall)
- Key learnings
- Next steps

### Publish
- Medium or LinkedIn
- Include metrics and data
- Add visualizations if possible

### Deliverable
- Published blog post (500+ words)
- Real metrics and data
- At least 1 visualization/chart
- Link to GitHub repo if applicable

---

## Week 2 Checkpoint

By end of Week 2, you should have:
- [ ] Custom eval in forked OpenAI evals repo
- [ ] 4-metric comparison analysis
- [ ] Streamlit labeling UI
- [ ] Error taxonomy with prompt patches
- [ ] Published case study blog post

---

## Resources

- [OpenAI Evals Repo](https://github.com/openai/evals)
- Streamlit documentation
- BLEURT/BERTScore libraries
- Medium/LinkedIn publishing platforms

---

## Notes

This week focuses on proving your prompts work with data, not just intuition. Every claim should be backed by metrics.

