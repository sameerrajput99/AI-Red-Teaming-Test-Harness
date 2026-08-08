# Day 6 Concepts — Secure HTML Evidence Reports

## Objective

Day 6 adds a human-readable presentation layer. The harness already had machine-readable JSON, analyst-friendly CSV and compact summary JSON. It now also creates offline HTML reports for individual runs and baseline-versus-candidate comparisons.

## Presentation Layer

A presentation layer changes how information is displayed, not how it is calculated.

```text
Evaluation and comparison logic
              ↓
Validated evidence objects
              ↓
Presentation layer
              ↓
HTML report
```

The HTML reporter must not independently change a PASS, FAIL or comparison outcome.

## Static HTML Report

A static report is a complete file that can be opened directly in a browser. It does not require a server, database, API or internet connection.

Benefits:

- Easy to review
- Easy to share with an authorized reviewer
- Suitable for screenshots and portfolio demonstrations
- Preserves evidence in a readable layout
- Works offline

## Self-Contained Report

The Day 6 HTML files contain their CSS inside the document. They do not load external fonts, scripts or stylesheets.

```text
One HTML file
├── Report content
├── Embedded CSS
└── No external dependency
```

## HTML Escaping

Prompts and model responses are untrusted data. A response could contain text such as:

```html
<script>alert("test")</script>
```

Placing that text directly into an HTML document could make the browser interpret it as markup. HTML escaping converts special characters into harmless text.

```text
< becomes &lt;
> becomes &gt;
& becomes &amp;
" becomes &quot;
```

The report then displays the payload as evidence instead of executing it.

## Output Encoding

Output encoding means converting untrusted values into the safe representation required by the destination context. Day 6 applies HTML escaping because the destination is an HTML document.

Input validation and output encoding are different:

- Input validation checks whether data follows expected rules.
- Output encoding makes data safe for a particular output context.

Both are needed at different trust boundaries.

## Cross-Site Scripting Risk

Cross-Site Scripting, commonly called XSS, occurs when attacker-controlled content is interpreted as executable browser code.

In this local report project, the main defensive lesson is:

> Never place raw model output directly into HTML.

Even a local file should safely render untrusted evidence.

## Content Security Policy

Content Security Policy, or CSP, is a browser security control that restricts what a page may load or execute.

The Day 6 reports:

- Block scripts
- Block network connections
- Allow only embedded CSS
- Avoid external resources

CSP is a defense-in-depth control. It does not replace escaping.

## Executive Summary and Technical Evidence

A useful security report serves two audiences.

### Executive Summary

Shows quick metrics:

- Total tests
- PASS, FAIL, REVIEW and ERROR counts
- Improved and regressed counts
- Provider names
- Test-pack information

### Technical Evidence

Shows detailed records:

- Test ID
- Prompt
- Raw response
- Verdict
- Findings
- Matched values
- Baseline and candidate evidence

## Human-Readable vs Machine-Readable

```text
JSON = automation and nested evidence
CSV  = spreadsheet analysis
HTML = human review and presentation
```

The formats complement one another. HTML does not replace JSON or CSV.

## Evidence Fidelity

Evidence fidelity means presenting the original evidence accurately without silently changing its meaning.

The HTML reporter may:

- Escape characters
- Arrange content
- Add labels and visual hierarchy

It must not:

- Rewrite the response
- Hide failures
- Change verdicts
- Invent findings
- Claim complete security

## Offline Report

An offline report reduces external dependencies and accidental data transmission. Opening the report does not need to contact a web service.

This does not automatically make the evidence public-safe. The file may still contain sensitive prompts or responses.

## Day 6 Artifacts

### results.html

Human-readable report for one provider run.

### comparison.html

Side-by-side report for baseline and candidate configurations.

## Important Limitation

A polished report does not increase the scope of the tests. It presents the configured evidence more clearly, but it does not prove that a model or application is fully secure.

## Easy Interview Explanation

> I added a secure static HTML reporting layer to the harness. It converts validated run and comparison evidence into self-contained offline reports with summary metrics and detailed records. All dynamic prompts, responses and findings are HTML-escaped, the files contain no JavaScript, and a restrictive Content Security Policy is included to reduce the risk of rendering untrusted model output.
