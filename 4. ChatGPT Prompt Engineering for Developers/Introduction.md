# ChatGPT Prompt Engineering for Developers 🚀

## What You’ll Learn 🎯

* **Prompt engineering best practices** for application development.
* **New ways to use LLMs**—including building your own custom chatbot.
* **Hands-on practice** writing and iterating prompts with the OpenAI API.

---

## About This Course 🧠

In **ChatGPT Prompt Engineering for Developers**, you’ll learn how to harness large language models (LLMs) to build powerful apps quickly. Using the OpenAI API, you can implement features that were previously too costly, too technical, or downright impossible. Taught by **Isa Fulford (OpenAI)** and **Andrew Ng (DeepLearning.AI)**, the course explains how LLMs work, shares **prompt engineering best practices**, and demonstrates practical applications for:

* **Summarizing** (e.g., condensing user reviews) ✂️
* **Inferring** (e.g., sentiment, topics) 🧭
* **Transforming** text (e.g., translation, grammar correction, format conversion) 🔁
* **Expanding** content (e.g., drafting emails) ✍️

You’ll also learn two core principles for effective prompting, how to **iterate prompts systematically**, and how to **build a custom chatbot**. The concepts are illustrated with examples you can run in a Jupyter notebook for hands-on practice. 💻

---

## Introduction 🌟

Welcome! Andrew Ng introduces Isa Fulford, who co-built the ChatGPT Retrieval plugin, contributes to the **OpenAI Cookbook**, and teaches best practices for using LLMs in products. While many guides focus on one-off prompts in the ChatGPT UI, this course emphasizes **LLMs as developer tools via APIs** for building real applications fast.

You’ll explore:

1. **Prompting best practices** for software development.
2. **Common use cases**—summarizing, inferring, transforming, expanding.
3. **Building a chatbot** using an LLM.

### Base vs. Instruction-Tuned LLMs 🧩

* **Base LLMs** predict the next token from vast web text. They may continue your input (“Once upon a time…”) but might respond with unrelated question lists if you ask factual queries.
* **Instruction-tuned LLMs** are fine-tuned to **follow instructions** and often further refined with **RLHF** (Reinforcement Learning from Human Feedback) to be **helpful, honest, and harmless**. For most practical apps, the course recommends using **instruction-tuned** models.

**Mindset tip:** Treat prompting like giving instructions to a smart colleague who doesn’t know your task context yet. Be explicit about **what** you want (focus, tone, length, references) and **how** to handle inputs.

---

## Guidelines: Two Core Principles 🧭

### 1) Write **Clear and Specific** Instructions ✍️

Longer prompts can be **clearer**, not worse.

**Tactics:**

* **Use delimiters** to isolate user input or resources

  * Triple backticks, quotes, XML tags, section titles.
  * Helps avoid **prompt injection** (“ignore previous instructions…” stays inside the delimited text to be summarized, not executed).
* **Ask for structured output** 📦

  * Request **JSON/HTML** with specific keys (e.g., `{"book_id": "...", "title": "...", "author": "...", "genre": "..."}`) to simplify parsing.
* **Check preconditions** ✅

  * Instruct the model to verify assumptions first and return a fallback like **“No steps provided.”** if they aren’t met.
* **Few-shot prompting** 🧪

  * Show examples of **desired style** or **format** (e.g., a grandparent’s tone) and then ask for a new answer “in a consistent style.”

### 2) Give the Model **Time to Think** 🕰️

If tasks require reasoning, **ask for intermediate steps** or a **chain of reasoning** *before* a final answer.

**Tactics:**

* **Specify step-by-step actions** (e.g., summarize → translate → extract names → output JSON).
* **Constrain the output format** with simple labeled sections to make parsing robust.
* **Have the model solve first, then compare** 🧮

  * For grading a student’s solution, instruct: *“Work out your own solution, then compare; only then grade.”* This reduces reasoning mistakes.

**Limitation & Mitigation:**
LLMs can **hallucinate**. Reduce risk by requiring **grounded quotes** first and then answering **from those quotes**. Add traceability whenever possible. 🔍

---

## Iterative Prompt Development 🔁

Like ML model training, you **won’t get the perfect prompt on the first try**. Use a loop:
**Idea → First Prompt → Result → Error Analysis → Refine → Repeat.**

**Example:** Marketing description from a **technical fact sheet** for a chair.

* First pass: too long → add **length constraint** (words/sentences/characters).
* Change **audience** (retailers vs. consumers) to emphasize **technical details**.
* Append requirements like **“include every 7-character product ID.”**
* Eventually add **rendered HTML** and a **dimension table**.

Mature apps may evaluate prompts on many examples (10–100+) for **average/worst-case performance**. Early on, single examples + quick iterations are fine. ⚙️

---

## Summarizing 🗞️➡️✂️

Use LLMs to **digest long text** (e.g., product reviews) quickly.

**Patterns:**

* **General summary** with clear **length controls** (words/sentences/characters).
* **Audience-specific** summaries (e.g., **shipping** vs. **pricing** department).
* **Extraction instead of summary** when you only need one fact (e.g., “What happened with delivery?”).
* **Batch processing** loop: iterate over many reviews and print concise summaries for dashboards.

---

## Inferring 🔎

Treat inference as **analysis** over text: **sentiment**, **emotions**, **anger detection**, **entity extraction**, **topic tagging**.

**Examples:**

* **Binary sentiment** (“positive”/“negative”) for easy downstream logic.
* **Emotions list** (≤5 items).
* **Anger detection** (boolean for escalation workflows).
* **Information extraction**: item purchased, brand, etc., **as JSON**.
* **Multi-label topics**: provide a topic list and ask for **0/1 per topic** (prefer JSON for robustness).

This replaces multiple supervised models with **a single promptable API**—huge speed boost for development. ⚡

---

## Transforming 🔄

LLMs can convert across **languages, tones, and formats**—and fix **grammar/spelling**.

**Translation** 🌍

* Identify language.
* Translate to one or many languages (even playful ones like “English Pirate”).
* Handle **formal vs. informal** variants (e.g., Spanish *usted* vs. *tú*).
* Build a **universal translator** pipeline for multilingual IT support.

**Tone transformation** 🎭

* Convert slang to a **business letter**, or adjust for **audience** and **register**.

**Format conversion** 🗂️

* JSON → HTML table (or any structured format).
* Prefer explicit **input/output schemas** to reduce variance.

**Proofread & Rewrite** ✨

* Correct grammar and spelling.
* Add constraints: **“If no errors, say ‘No errors found.’”**
* Use diff tools (e.g., *redlines*) to highlight changes.
* Apply style guides (e.g., **APA**), increase **compelling tone**, and return **Markdown**.

---

## Building a Custom Chatbot 🤖

With the same prompting principles, assemble a **chatbot** that:

* Follows **clear system instructions** (role, boundaries, voice).
* Uses **structured outputs** for UI components.
* Reduces hallucinations by **retrieval** (quotes first, answer second).
* Iterates prompts with **evaluation sets** for stability.

---

## Conclusion 🎉

You now have a practical toolkit:

* **Two principles:** be **clear & specific**, and **give time to think**.
* **A process:** **iterate** prompts like experiments.
* **Capabilities:** **summarizing**, **inferring**, **transforming**, **expanding**, and **chatbot building**.

Start small and have fun—use your early projects to build better ones next. These tools are powerful: **use them responsibly** and aim for positive impact. 🌱

Happy building—and share what you create! ✨
