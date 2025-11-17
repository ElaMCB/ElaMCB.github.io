# Week 3: Domain Transfer & Advanced Patterns

**Goal**: Prove you can jump domains and ship production-ready prompts

**Time**: ~10 hours (90-minute daily blocks)

---

## Day 1: Domain Exploration

### Pick 2 Verticals
Choose domains you're NOT expert in (e.g., medical, legal, finance)

### Task
For each domain:
1. Find a public 100-row dataset
2. Spend 2 hours reading domain-specific style guides:
   - Medical: AMA style guide
   - Legal: Bluebook citation
   - Finance: SEC reporting standards
3. Understand domain-specific terminology and conventions

### Deliverable
- 2 domain datasets (100 rows each)
- Domain style guide notes
- Key terminology glossary for each domain

---

## Day 2: Prompt Pattern Catalog

### Patterns to Map
- RAG (Retrieval-Augmented Generation)
- Reflection
- Tree-of-Thought
- Role-play

### Task
For each domain, create 1 prompt per pattern:
- Total: 2 domains × 4 patterns = 8 prompts
- Each prompt must pass a 5-minute expert sanity check

### Validation
- Post to relevant subreddit
- Gather 3 comments
- Iterate based on feedback

### Deliverable
- 8 prompts (2 domains × 4 patterns)
- Expert feedback (3 comments per prompt = 24 total)
- Iterated versions based on feedback
- Pattern effectiveness comparison

---

## Day 3: Tooling Comparison

### Debate
LangChain vs. pure Python

### Build
The same RAG chain both ways:
- LangChain implementation
- Pure Python implementation
- Compare: time-to-first-token <1s on laptop

### Metrics
- Time-to-first-token
- Code complexity
- Maintainability
- Performance

### Deliverable
- Both implementations (LangChain + pure Python)
- Performance comparison
- Pros/cons analysis
- Recommendation with justification

---

## Day 4: Cost & Latency Optimization

### Scenario
Given 1M tokens/day budget, design a prompt + model mix:
- GPT-4 vs. 3.5-turbo vs. Claude
- Keep <5% quality drop
- Achieve 50% cost cut

### Deliverable
Write as a 1-page internal memo:
- Current state (baseline)
- Proposed solution
- Cost analysis
- Quality impact
- Recommendation

---

## Day 5: Mini-Hackathon

### Task
4-hour sprint to solve a live Kaggle "LLM" competition task

### Requirements
- Submit solution
- Screenshot leaderboard rank
- Document approach

### Deliverable
- Kaggle submission
- Leaderboard screenshot
- Approach documentation
- Code on GitHub

---

## Week 3 Checkpoint

By end of Week 3, you should have:
- [ ] 2 domain datasets with style guide notes
- [ ] 8 prompts (4 patterns × 2 domains) with expert validation
- [ ] LangChain vs pure Python comparison
- [ ] Cost optimization memo
- [ ] Kaggle competition submission

---

## Resources

- Kaggle competitions
- Domain-specific datasets (PubMed, legal databases)
- LangChain documentation
- Claude/GPT-4 API documentation

---

## Notes

This week proves you can adapt to new domains and make production-ready decisions about tooling and cost.

