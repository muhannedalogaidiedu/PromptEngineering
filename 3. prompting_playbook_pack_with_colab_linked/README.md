# Prompt Engineering Playbook — CLI

This pack includes:
- `prompting_playbook_cli.py` — runnable CLI with **20 prompting techniques**
- `requirements.txt` — optional provider SDKs
- This README

## Quick start
```bash
# Option A: Run with dummy provider (no installs, shows prompts/results)
python prompting_playbook_cli.py --technique all

# Option B: Pick one technique
python prompting_playbook_cli.py --technique 9
```

## Use a real provider
Install the SDK and set your API key, then run with flags:

### OpenAI
```bash
pip install openai
export OPENAI_API_KEY=YOUR_KEY
python prompting_playbook_cli.py --provider openai --model gpt-4.1-mini --technique all --temperature 0.2
```

### Google Gemini
```bash
pip install google-generativeai
export GOOGLE_API_KEY=YOUR_KEY   # or GEMINI_API_KEY
python prompting_playbook_cli.py --provider gemini --model gemini-1.5-pro --technique 6
```

### Anthropic
```bash
pip install anthropic
export ANTHROPIC_API_KEY=YOUR_KEY
python prompting_playbook_cli.py --provider anthropic --model claude-3-5-sonnet-20241022 --technique 7
```

### Mistral
```bash
pip install mistralai
export MISTRAL_API_KEY=YOUR_KEY
python prompting_playbook_cli.py --provider mistral --model mistral-large-latest --technique 3
```

### Cohere
```bash
pip install cohere
export COHERE_API_KEY=YOUR_KEY
python prompting_playbook_cli.py --provider cohere --model command-r-plus --technique 20
```

## Techniques included
Zero-shot, One-shot, Few-shot, Chain-of-Thought, Self-Consistency, ReAct, Tree-of-Thought,
Generated Knowledge, RAG (stub), Instruction, Contextual, Role, CoT (Explicit Steps), Multi-turn,
Program-Aided, Least-to-Most, Meta, APE (stub), Multimodal (stub), Contrastive.

> Stubs (RAG, APE, Multimodal) are placeholders you can wire to your own tools.
