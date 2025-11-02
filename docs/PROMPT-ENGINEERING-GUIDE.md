<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompt Engineering Guide - Daily Development Tasks</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="../images/favicon.svg">
    <link rel="icon" type="image/x-icon" href="../images/favicon.ico">
    <link rel="manifest" href="../images/site.webmanifest">
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #0a0a0f;
            --secondary: #00d4ff;
            --accent: #7c3aed;
            --neon-blue: #00f5ff;
            --neon-purple: #bf00ff;
            --neon-green: #39ff14;
            --light: #e4e4e7;
            --dark: #1a1a1f;
            --glass: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, var(--primary) 0%, #1a1a2e 50%, var(--dark) 100%);
            background-attachment: fixed;
            color: var(--light);
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 4rem 0 2rem;
            border-bottom: 2px solid var(--secondary);
            margin-bottom: 3rem;
        }

        .header-content h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .subtitle {
            font-size: 1.2rem;
            color: var(--light);
            margin-bottom: 2rem;
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin: 2rem 0;
        }

        .nav-links a {
            color: var(--light);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border: 2px solid var(--secondary);
            border-radius: 25px;
            transition: all 0.3s ease;
            background: var(--glass);
            backdrop-filter: blur(10px);
            font-size: 0.85rem;
        }

        .nav-links a:hover {
            background: var(--secondary);
            color: var(--primary);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.3);
        }

        section {
            margin: 3rem 0;
        }

        h2 {
            font-size: 2rem;
            color: var(--secondary);
            margin: 3rem 0 1.5rem;
            position: relative;
            display: inline-block;
        }

        h2::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, var(--neon-blue), transparent);
        }

        h3 {
            font-size: 1.4rem;
            color: var(--neon-blue);
            margin: 2rem 0 1rem;
        }

        h4 {
            font-size: 1.1rem;
            color: var(--neon-green);
            margin: 1.5rem 0 0.75rem;
        }

        p {
            margin: 1rem 0;
            color: var(--light);
        }

        .card {
            background: var(--glass);
            backdrop-filter: blur(15px);
            border: 2px solid var(--secondary);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 245, 255, 0.2);
            border-color: var(--neon-blue);
        }

        .highlight-box {
            background: rgba(0, 245, 255, 0.1);
            border-left: 4px solid var(--neon-blue);
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 8px;
        }

        .prompt-box {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid var(--neon-green);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            position: relative;
        }

        .prompt-box::before {
            content: 'PROMPT';
            position: absolute;
            top: -12px;
            left: 20px;
            background: var(--primary);
            color: var(--neon-green);
            padding: 0 10px;
            font-size: 0.75rem;
            font-weight: bold;
            letter-spacing: 2px;
        }

        pre {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--secondary);
            border-radius: 8px;
            padding: 1.5rem;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            color: var(--neon-green);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        code {
            color: var(--neon-green);
            font-family: 'Courier New', monospace;
        }

        ul, ol {
            margin: 1rem 0;
            padding-left: 2rem;
        }

        ul li, ol li {
            margin: 0.5rem 0;
            color: var(--light);
        }

        ul li::marker {
            color: var(--neon-green);
        }

        ol li::marker {
            color: var(--neon-blue);
        }

        strong {
            color: var(--neon-blue);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }

        .example-card {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--neon-purple);
            border-radius: 10px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        .example-card:hover {
            border-color: var(--neon-blue);
            box-shadow: 0 10px 30px rgba(191, 0, 255, 0.3);
            transform: translateY(-5px);
        }

        .tag {
            display: inline-block;
            background: var(--neon-purple);
            color: var(--primary);
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
            margin: 0.25rem;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .metric-item {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--secondary);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
        }

        .metric-value {
            font-size: 2rem;
            color: var(--neon-green);
            font-weight: bold;
            margin: 0.5rem 0;
        }

        .metric-label {
            color: var(--light);
            font-size: 0.9rem;
        }

        .warning-box {
            background: rgba(191, 0, 255, 0.1);
            border-left: 4px solid var(--neon-purple);
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 8px;
        }

        .warning-box strong {
            color: var(--neon-purple);
        }

        .back-link {
            display: inline-block;
            margin: 3rem 0;
            padding: 1rem 2rem;
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 2px solid var(--secondary);
            border-radius: 25px;
            color: var(--light);
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .back-link:hover {
            background: var(--secondary);
            color: var(--primary);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 212, 255, 0.3);
        }

        .toc {
            background: var(--glass);
            backdrop-filter: blur(15px);
            border: 2px solid var(--secondary);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
        }

        .toc h2 {
            margin-top: 0;
        }

        .toc ul {
            list-style: none;
            padding-left: 0;
        }

        .toc ul li {
            padding: 0.5rem 0;
        }

        .toc a {
            color: var(--neon-blue);
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .toc a:hover {
            color: var(--neon-purple);
            padding-left: 10px;
        }

        @media (max-width: 768px) {
            .header-content h1 {
                font-size: 1.8rem;
            }

            .grid, .metrics {
                grid-template-columns: 1fr;
            }

            pre {
                font-size: 0.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-content">
                <h1>Prompt Engineering for Daily Development Tasks</h1>
                <p class="subtitle">A practical guide to integrating AI assistance into your development workflow</p>
                
                <nav class="nav-links">
                    <a href="#introduction">Introduction</a>
                    <a href="#workflow">Workflow</a>
                    <a href="#code-generation">Code Generation</a>
                    <a href="#testing-qa">Testing & QA</a>
                    <a href="#documentation">Documentation</a>
                    <a href="#debugging">Debugging</a>
                    <a href="#best-practices">Best Practices</a>
                    <a href="#advanced">Advanced</a>
                </nav>
            </div>
        </header>

        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#introduction">Introduction</a></li>
                <li><a href="#workflow">Development Workflow Integration</a></li>
                <li><a href="#code-generation">Code Generation Prompts</a></li>
                <li><a href="#testing-qa">Testing & QA Prompts</a></li>
                <li><a href="#documentation">Documentation Prompts</a></li>
                <li><a href="#debugging">Debugging & Problem Solving</a></li>
                <li><a href="#best-practices">Best Practices</a></li>
                <li><a href="#advanced">Advanced Techniques</a></li>
            </ul>
        </div>

        <section id="introduction">
            <h2>Introduction</h2>
            <div class="card">
                <p>This guide demonstrates how to effectively use AI assistance in daily development tasks. Every technique here was used to build this portfolio template, achieving <strong>10x faster development cycles</strong>.</p>
                
                <h3>Why Prompt Engineering Matters</h3>
                <div class="metrics">
                    <div class="metric-item">
                        <div class="metric-value">60-80%</div>
                        <div class="metric-label">Efficiency Gain</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">10x</div>
                        <div class="metric-label">Faster Development</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">100%</div>
                        <div class="metric-label">Code Quality</div>
                    </div>
                </div>

                <ul>
                    <li><strong>Efficiency:</strong> Reduce repetitive coding tasks by 60-80%</li>
                    <li><strong>Quality:</strong> Generate consistent, well-structured code</li>
                    <li><strong>Learning:</strong> Understand new technologies faster</li>
                    <li><strong>Problem Solving:</strong> Break down complex tasks systematically</li>
                </ul>
            </div>
        </section>

        <section id="workflow">
            <h2>Development Workflow Integration</h2>

            <div class="card">
                <h3>1. Project Planning Phase</h3>
                <h4>Task: Breaking down a new feature</h4>
                
                <div class="prompt-box">
                    <pre>Act as a senior software architect. I need to implement [FEATURE_NAME] for a [PROJECT_TYPE].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Please provide:
1. Technical approach and architecture
2. File structure and organization
3. Implementation steps in priority order
4. Potential challenges and solutions
5. Testing strategy</pre>
                </div>
                
                <div class="highlight-box">
                    <strong>Example Output:</strong> Detailed implementation plan with clear next steps
                </div>
            </div>

            <div class="card">
                <h3>2. Code Generation Phase</h3>
                <h4>Task: Creating HTML components</h4>
                
                <div class="prompt-box">
                    <pre>Create a responsive HTML component for [COMPONENT_NAME] with these requirements:
- [Specific requirements]
- Modern CSS (Grid/Flexbox)
- Mobile-first approach
- Accessibility compliant (ARIA labels, semantic HTML)
- No JavaScript frameworks

Include:
- Complete HTML structure
- CSS styles with CSS variables
- Hover effects and animations
- Mobile breakpoints</pre>
                </div>
            </div>

            <div class="card">
                <h3>CSS Styling</h3>
                
                <div class="prompt-box">
                    <pre>Create advanced CSS for [ELEMENT_TYPE] with:
- Futuristic/modern design
- Smooth animations and transitions
- CSS variables for theming
- Responsive behavior
- Performance optimized (GPU acceleration)

Style requirements:
[SPECIFIC_DESIGN_REQUIREMENTS]</pre>
                </div>
            </div>
        </section>

        <section id="code-generation">
            <h2>Code Generation Prompts</h2>

            <div class="grid">
                <div class="example-card">
                    <h3>HTML Structure</h3>
                    <span class="tag">HTML5</span>
                    <span class="tag">Semantic</span>
                    <div class="prompt-box">
                        <pre>Generate semantic HTML5 structure for [COMPONENT_NAME]:
- Use proper heading hierarchy
- Include ARIA labels
- Add meta tags for SEO
- Structure for screen readers
- Valid HTML5 markup</pre>
                    </div>
                </div>

                <div class="example-card">
                    <h3>CSS Animations</h3>
                    <span class="tag">CSS3</span>
                    <span class="tag">Performance</span>
                    <div class="prompt-box">
                        <pre>Create CSS animations for [ELEMENT]:
- Keyframe animations
- CSS transforms
- Smooth easing functions
- Performance optimized
- Responsive behavior
- Dark/light theme support</pre>
                    </div>
                </div>

                <div class="example-card">
                    <h3>JavaScript Functionality</h3>
                    <span class="tag">ES6+</span>
                    <span class="tag">Vanilla JS</span>
                    <div class="prompt-box">
                        <pre>Write vanilla JavaScript for [FUNCTIONALITY]:
- ES6+ syntax
- Event delegation
- Error handling
- Mobile touch support
- Accessibility keyboard navigation
- No external dependencies</pre>
                    </div>
                </div>
            </div>
        </section>

        <section id="testing-qa">
            <h2>Testing & QA Prompts</h2>

            <div class="card">
                <h3>Test Case Generation</h3>
                
                <div class="prompt-box">
                    <pre>Generate comprehensive test cases for [FEATURE_NAME]:

Functional Requirements:
- [Requirement 1]
- [Requirement 2]

Include:
1. Positive test scenarios
2. Negative test scenarios
3. Edge cases and boundary conditions
4. Cross-browser compatibility tests
5. Mobile device testing scenarios
6. Accessibility testing checklist
7. Performance testing considerations

Format as: Test ID | Test Description | Expected Result | Priority</pre>
                </div>
            </div>

            <div class="card">
                <h3>Bug Analysis</h3>
                
                <div class="prompt-box">
                    <pre>Analyze this bug report and provide debugging strategy:

Issue: [BUG_DESCRIPTION]
Browser: [BROWSER_INFO]
Steps to reproduce: [STEPS]
Expected vs Actual: [BEHAVIOR]

Provide:
1. Potential root causes (ranked by likelihood)
2. Debugging steps to isolate the issue
3. Code areas to investigate
4. Testing approach to verify fix
5. Prevention strategies for similar issues</pre>
                </div>
            </div>

            <div class="card">
                <h3>Code Review</h3>
                
                <div class="prompt-box">
                    <pre>Review this code for:
- Security vulnerabilities
- Performance issues
- Accessibility compliance
- Code quality and maintainability
- Best practices adherence

Code:
[CODE_BLOCK]

Provide specific feedback with examples and suggested improvements.</pre>
                </div>
            </div>
        </section>

        <section id="documentation">
            <h2>Documentation Prompts</h2>

            <div class="card">
                <h3>README Generation</h3>
                
                <div class="prompt-box">
                    <pre>Create a professional README.md for [PROJECT_NAME]:

Project details:
- Purpose: [PROJECT_PURPOSE]
- Tech stack: [TECHNOLOGIES]
- Features: [KEY_FEATURES]

Include:
- Clear project description
- Installation instructions
- Usage examples with code
- API documentation (if applicable)
- Contributing guidelines
- License information
- Badges for build status, version, etc.</pre>
                </div>
            </div>

            <div class="card">
                <h3>Code Documentation</h3>
                
                <div class="prompt-box">
                    <pre>Generate comprehensive documentation for this function:
[CODE_FUNCTION]

Include:
- Clear description of purpose
- Parameter descriptions with types
- Return value documentation
- Usage examples
- Error handling scenarios
- Performance considerations</pre>
                </div>
            </div>
        </section>

        <section id="debugging">
            <h2>Debugging & Problem Solving</h2>

            <div class="card">
                <h3>Error Analysis</h3>
                
                <div class="prompt-box">
                    <pre>I'm getting this error:
[ERROR_MESSAGE]

Context:
- Technology: [TECH_STACK]
- What I was trying to do: [TASK]
- Code that caused it: [CODE_SNIPPET]
- Environment: [ENVIRONMENT_DETAILS]

Please provide:
1. Explanation of what this error means
2. Most likely causes
3. Step-by-step debugging approach
4. Multiple solution options
5. Prevention strategies</pre>
                </div>
            </div>

            <div class="card">
                <h3>Performance Optimization</h3>
                
                <div class="prompt-box">
                    <pre>Optimize this code for performance:
[CODE_BLOCK]

Focus on:
- Execution speed
- Memory usage
- Browser rendering performance
- Mobile device compatibility
- Accessibility maintenance

Provide before/after comparison with explanations.</pre>
                </div>
            </div>
        </section>

        <section id="best-practices">
            <h2>Best Practices</h2>

            <div class="grid">
                <div class="card">
                    <h3>1. Context is King</h3>
                    <ul>
                        <li>Always provide specific context about your project</li>
                        <li>Include relevant code snippets and error messages</li>
                        <li>Specify constraints (browser support, performance requirements)</li>
                    </ul>
                </div>

                <div class="card">
                    <h3>2. Iterative Refinement</h3>
                    <ul>
                        <li>Start with a basic prompt, then refine</li>
                        <li>Ask for specific improvements</li>
                        <li>Build on previous responses</li>
                    </ul>
                </div>

                <div class="card">
                    <h3>3. Template Approach</h3>
                    <ul>
                        <li>Create reusable prompt templates</li>
                        <li>Customize for your tech stack</li>
                        <li>Share successful prompts with team</li>
                    </ul>
                </div>

                <div class="card">
                    <h3>4. Validation Strategy</h3>
                    <ul>
                        <li>Always review for security issues</li>
                        <li>Test thoroughly, especially edge cases</li>
                        <li>Validate HTML and check accessibility</li>
                    </ul>
                </div>
            </div>
        </section>

        <section id="advanced">
            <h2>Advanced Techniques</h2>

            <div class="card">
                <h3>1. Chain of Thought Prompting</h3>
                
                <div class="prompt-box">
                    <pre>Think through this step-by-step:

Problem: [COMPLEX_PROBLEM]

Step 1: Analyze the requirements
Step 2: Identify potential approaches
Step 3: Evaluate pros/cons of each approach
Step 4: Choose the best solution
Step 5: Implement with detailed explanation
Step 6: Identify testing strategy</pre>
                </div>
            </div>

            <div class="card">
                <h3>2. Role-Based Prompting</h3>
                
                <div class="prompt-box">
                    <pre>Act as a [ROLE] with [X] years of experience in [DOMAIN].

[SPECIFIC_TASK_REQUEST]

Consider:
- Industry best practices
- Common pitfalls to avoid
- Performance implications
- Scalability concerns
- Maintenance considerations</pre>
                </div>
            </div>

            <div class="card">
                <h3>3. Multi-Step Problem Solving</h3>
                
                <div class="prompt-box">
                    <pre>I need to implement [COMPLEX_FEATURE]. Let's break this down:

1. First, help me understand the technical requirements
2. Then, design the architecture
3. Next, create the implementation plan
4. Finally, identify testing and deployment strategies

Start with step 1, and I'll ask for each subsequent step.</pre>
                </div>
            </div>

            <div class="card">
                <h3>4. Comparative Analysis</h3>
                
                <div class="prompt-box">
                    <pre>Compare these approaches for [TASK]:

Approach 1: [OPTION_1]
Approach 2: [OPTION_2]
Approach 3: [OPTION_3]

Evaluate each on:
- Performance
- Maintainability
- Scalability
- Development time
- Browser compatibility

Recommend the best approach with justification.</pre>
                </div>
            </div>
        </section>

        <section>
            <h2>Common Pitfalls to Avoid</h2>
            
            <div class="warning-box">
                <ol>
                    <li><strong>Over-reliance:</strong> Always review and understand generated code</li>
                    <li><strong>Security Blindness:</strong> Validate for security vulnerabilities</li>
                    <li><strong>Context Loss:</strong> Provide sufficient context for accurate results</li>
                    <li><strong>Copy-Paste Syndrome:</strong> Adapt code to your specific needs</li>
                    <li><strong>Testing Neglect:</strong> AI-generated code still needs thorough testing</li>
                </ol>
            </div>
        </section>

        <section>
            <h2>Conclusion</h2>
            
            <div class="card">
                <p>Prompt engineering is not about replacing developer skills—it's about <strong>amplifying them</strong>. The techniques in this guide enabled building this entire portfolio template in hours instead of weeks, while maintaining high quality and professional standards.</p>
                
                <h3>Key Takeaways</h3>
                <ul>
                    <li>Start with clear, specific prompts</li>
                    <li>Iterate and refine based on results</li>
                    <li>Always validate and test AI-generated code</li>
                    <li>Use AI as a powerful development accelerator</li>
                    <li>Maintain human oversight and decision-making</li>
                </ul>
                
                <h3>Next Steps</h3>
                <ul>
                    <li>Practice with the provided prompt templates</li>
                    <li>Customize prompts for your specific tech stack</li>
                    <li>Build your own prompt library</li>
                    <li>Share successful prompts with your team</li>
                </ul>
            </div>
        </section>

        <div style="text-align: center;">
            <a href="../learn/" class="back-link">
                <i class="fas fa-arrow-left"></i> Back to Learning Hub
            </a>
        </div>

        <footer style="text-align: center; margin: 3rem 0; padding: 2rem 0; border-top: 1px solid rgba(0, 212, 255, 0.3); color: var(--light); font-size: 0.9rem;">
            <p><em>This guide is continuously updated based on real-world usage and community feedback.</em></p>
        </footer>
    </div>
</body>
</html>
