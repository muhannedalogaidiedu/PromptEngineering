#!/usr/bin/env python3
"""
Prompt Engineering Playbook — CLI
---------------------------------
Run 20 prompting technique examples from the command line with a provider-agnostic wrapper.

Usage examples:
  python prompting_playbook_cli.py --technique 1
  python prompting_playbook_cli.py --technique all --provider dummy
  python prompting_playbook_cli.py --provider openai --model gpt-4.1-mini --technique 9 --temperature 0.2

Providers supported (choose with --provider):
  - dummy (default, no SDK needed; echoes a fake response)
  - gemini  (pip install google-generativeai; export GOOGLE_API_KEY)
  - openai  (pip install openai; export OPENAI_API_KEY)
  - anthropic (pip install anthropic; export ANTHROPIC_API_KEY)
  - mistral (pip install mistralai; export MISTRAL_API_KEY)
  - cohere  (pip install cohere; export COHERE_API_KEY)
"""

import os, json, argparse, collections

# ------------------------------
# Provider wrappers
# ------------------------------

def _dummy_llm(prompt: str, model: str = None, temperature: float = 0.2):
    return f"[DUMMY RESPONSE]\nModel={model or 'dummy-model'} Temp={temperature}\nPrompt (truncated): {prompt[:240]}..."

def _gemini_llm(prompt: str, model: str = "gemini-1.5-pro", temperature: float = 0.2):
    try:
        import google.generativeai as genai
    except ImportError as e:
        raise RuntimeError("Gemini provider requires 'google-generativeai'. Install with: pip install google-generativeai") from e
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GOOGLE_API_KEY (or GEMINI_API_KEY) in your environment.")
    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    resp = model_obj.generate_content(prompt, generation_config={"temperature": temperature})
    return getattr(resp, "text", str(resp))

def _openai_llm(prompt: str, model: str = "gpt-4.1-mini", temperature: float = 0.2):
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError("OpenAI provider requires 'openai'. Install with: pip install openai") from e
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment.")
    client = OpenAI(api_key=api_key)
    r = client.chat.completions.create(model=model, temperature=temperature, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content

def _anthropic_llm(prompt: str, model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.2):
    try:
        import anthropic
    except ImportError as e:
        raise RuntimeError("Anthropic provider requires 'anthropic'. Install with: pip install anthropic") from e
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Set ANTHROPIC_API_KEY in your environment.")
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(model=model, max_tokens=1200, temperature=temperature, messages=[{"role":"user","content":prompt}])
    # Concatenate only text blocks
    out = []
    for blk in msg.content:
        if getattr(blk, "type", "") == "text":
            out.append(blk.text)
    return "\n".join(out) if out else str(msg)

def _mistral_llm(prompt: str, model: str = "mistral-large-latest", temperature: float = 0.2):
    try:
        from mistralai.client import MistralClient
    except ImportError as e:
        raise RuntimeError("Mistral provider requires 'mistralai'. Install with: pip install mistralai") from e
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("Set MISTRAL_API_KEY in your environment.")
    client = MistralClient(api_key=api_key)
    r = client.chat(model=model, temperature=temperature, messages=[{"role":"user","content":prompt}])
    return r.choices[0].message.content

def _cohere_llm(prompt: str, model: str = "command-r-plus", temperature: float = 0.2):
    try:
        import cohere
    except ImportError as e:
        raise RuntimeError("Cohere provider requires 'cohere'. Install with: pip install cohere") from e
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Set COHERE_API_KEY in your environment.")
    co = cohere.Client(api_key=api_key)
    r = co.chat(model=model, temperature=temperature, messages=[{"role":"user","content":prompt}])
    return r.text

PROVIDERS = {
    "dummy": _dummy_llm,
    "gemini": _gemini_llm,
    "openai": _openai_llm,
    "anthropic": _anthropic_llm,
    "mistral": _mistral_llm,
    "cohere": _cohere_llm,
}

# ------------------------------
# Techniques 1..20
# ------------------------------

def t1_zero_shot(llm):
    prompt = """Summarize this quarterly financial risk report into 5 bullets, plain English:
[PASTE REPORT TEXT HERE]"""
    return llm(prompt)

def t2_one_shot(llm):
    example = """Example summary style:
- Key risk drivers: liquidity, FX exposure
- Material changes: inventory +12% QoQ
- Action items: hedge EUR, tighten DSO
"""
    prompt = example + "\nNow summarize the new report similarly:\n[NEW REPORT]"
    return llm(prompt)

def t3_few_shot(llm):
    shots = """
Task: Classify transaction as FRAUD or OK.

Example 1:
Input: Merchant=ABC Travel, Amount=$4,920, Country=US
Label: OK

Example 2:
Input: Merchant=CryptoX, Amount=$9,990, Country=RU
Label: FRAUD
"""
    prompt = shots + "\nPredict label for:\nInput: Merchant=XYZ GiftCards, Amount=$7,500, Country=Unknown\nLabel:"
    return llm(prompt)

def t4_cot(llm):
    prompt = """Analyze these ratios and conclude company health.
Think step-by-step (show brief reasoning, then final verdict):

Data:
- Current ratio 1.9
- Debt/Equity 0.6
- Gross margin 42%

Output: Reasoning (brief) -> Verdict
"""
    return llm(prompt)

def t5_self_consistency(llm):
    prompt = "Given symptoms: fever, rash, joint pain—list top likely diagnoses (3)."
    # In a real run, you'd loop multiple calls and vote. Here we simulate 3 calls.
    responses = [llm(prompt) for _ in range(3)]
    return "=== Self-consistency candidates ===\n" + "\n---\n".join(responses)

def t6_react(llm):
    # Simulated tool: "external DB"
    def search_db(query: str) -> str:
        return "DB_RESULT: Latest EPS $1.22, YoY +8%."
    plan = llm("""You can REASON then ACT with tools.
Question: "Is the company's EPS trending up?"
Think: We should fetch EPS.
Act: search_db("EPS trend for ACME")""")
    tool_result = search_db("EPS trend for ACME")
    final = llm(f"Context from tool: {tool_result}\nAnswer the original question succinctly.")
    return f"Plan:\n{plan}\n\nTool:\n{tool_result}\n\nFinal:\n{final}"

def t7_tree_of_thought(llm):
    question = "Choose best portfolio: {A: 70/30}, {B: 50/50}, {C: 30/70} for a 5-yr horizon."
    branches = [llm(f"Option {opt}: pros/cons, risk, return, suitability for moderate-risk investor.") for opt in ["A","B","C"]]
    judge = llm("Evaluate the following analyses and pick the best for a moderate-risk investor:\n"+"\n\n".join(branches))
    return "=== Branches ===\n" + "\n\n".join(branches) + "\n\n=== Verdict ===\n" + judge

def t8_generated_knowledge(llm):
    knowledge = llm("Summarize company ACME: products, markets, risks, last 2 years trends.")
    answer = llm(f"Using this background:\n{knowledge}\nNow: Assess ACME’s liquidity risks in 5 bullets.")
    return "Background:\n" + knowledge + "\n\nAssessment:\n" + answer

def t9_rag_stub(llm):
    retrieved = [
        "10-K excerpt: Operating cash flow up 12%, CAPEX stable.",
        "Earnings call: Guidance raised for FY, FX headwinds easing."
    ]
    prompt = f"Ground your answer ONLY in these docs:\n{retrieved[0]}\n{retrieved[1]}\n\nQuestion: Summarize growth drivers."
    return llm(prompt)

def t10_instruction(llm):
    prompt = """Extract all dollar amounts > $10,000 and return JSON array of numbers only.
Text:
- Purchase: $4,500
- Equipment: $25,000
- Settlement: $180,000
- Fees: $9,900
"""
    return llm(prompt)

def t11_contextual(llm):
    prompt = """Context: You are a senior medical reviewer.
Task: Turn these notes into a concise assessment & plan (<=120 words).
Notes: [PASTE CLINICAL NOTES]
"""
    return llm(prompt)

def t12_role(llm):
    prompt = """You are a compliance officer. Identify high-risk clauses in this NDA and explain why in 3 bullets:
[PASTE NDA]
"""
    return llm(prompt)

def t13_cot_explicit(llm):
    prompt = """Follow these steps:
1) Read contract text
2) Extract obligations per party
3) List 3 risks with brief rationale
Contract:
[PASTE CONTRACT]
Output format:
- Obligations: {Party A:[], Party B:[]}
- Risks: [..]
"""
    return llm(prompt)

def t14_multi_turn(llm):
    history = []
    def chat(user):
        history.append({"role":"user","content":user})
        response = llm("Conversation:\n"+json.dumps(history)+"\nAssistant:")
        history.append({"role":"assistant","content":response})
        return response
    a = chat("We saw revenue up 12%. Do we have regional breakdown?")
    b = chat("Yes, EMEA led. Summarize next steps.")
    return "Turn1:\n" + a + "\n\nTurn2:\n" + b

def t15_program_aided(llm):
    ratios = {"current":1.9, "quick":1.5, "de_ratio":0.6}
    prompt = f"Given ratios = {ratios}, provide a concise health assessment (<=80 words)."
    return llm(prompt)

def t16_least_to_most(llm):
    growth = llm("Compute revenue growth: 120M -> 138M YoY. Give % growth only.")
    hard = llm(f"Given growth={growth}, discuss sustainability in 4 bullets (drivers, risks, outlook, watchlist).")
    return "Easy step:\n" + growth + "\n\nHard step:\n" + hard

def t17_meta(llm):
    prompt = """I need a better prompt to extract ‘change of control’ clauses reliably.
Suggest 3 improved prompts with rationale, and one evaluation metric to compare them.
"""
    return llm(prompt)

def t18_ape_stub(llm):
    candidates = [
        "Extract change-of-control clauses. Return standardized JSON with clause text and risk level.",
        "Identify change-of-control clauses. Add span indices and a one-line rationale.",
        "Find ALL change-of-control clauses; output CSV fields: start,end,text,risk(score 1-5)."
    ]
    grades = [llm(f"Rate this prompt for recall & precision (0-10 each), then give total:\n{p}") for p in candidates]
    return "=== Candidates & Grades ===\n" + "\n\n".join(f"{i+1}) {c}\nGrade:\n{g}" for i,(c,g) in enumerate(zip(candidates, grades)))

def t19_multimodal_stub(llm):
    return ("[Multimodal placeholder] In a real environment, pass both text + image to a multimodal model.\n"
            "Prompt: 'Given the attached chest X-ray, list 3 notable findings with caveats.'")

def t20_contrastive(llm):
    prompt = """Compare two treatments (A: ACE inhibitor, B: ARB) for hypertension.
Provide: efficacy, side effects, cost, guideline stance. End with a balanced recommendation."""
    return llm(prompt)

TECHNIQUES = {
    1: ("Zero-shot", t1_zero_shot),
    2: ("One-shot", t2_one_shot),
    3: ("Few-shot", t3_few_shot),
    4: ("Chain-of-Thought", t4_cot),
    5: ("Self-Consistency", t5_self_consistency),
    6: ("ReAct", t6_react),
    7: ("Tree-of-Thought", t7_tree_of_thought),
    8: ("Generated Knowledge", t8_generated_knowledge),
    9: ("RAG (stub)", t9_rag_stub),
    10: ("Instruction", t10_instruction),
    11: ("Contextual", t11_contextual),
    12: ("Role", t12_role),
    13: ("CoT (Explicit Steps)", t13_cot_explicit),
    14: ("Multi-turn", t14_multi_turn),
    15: ("Program-Aided", t15_program_aided),
    16: ("Least-to-Most", t16_least_to_most),
    17: ("Meta", t17_meta),
    18: ("Automatic Prompt Engineering (stub)", t18_ape_stub),
    19: ("Multimodal (stub)", t19_multimodal_stub),
    20: ("Contrastive", t20_contrastive),
}

# ------------------------------
# CLI
# ------------------------------

def make_llm(provider: str, model: str, temperature: float):
    provider = provider.lower()
    if provider not in PROVIDERS:
        raise SystemExit(f"Unsupported provider '{provider}'. Choose one of: {list(PROVIDERS.keys())}")
    fn = PROVIDERS[provider]
    return lambda prompt: fn(prompt, model=model, temperature=temperature)

def main():
    ap = argparse.ArgumentParser(description="Prompt Engineering Playbook — CLI")
    ap.add_argument("--provider", default="dummy", help="dummy|gemini|openai|anthropic|mistral|cohere")
    ap.add_argument("--model", default=None, help="Model name for selected provider (e.g., gpt-4.1-mini, gemini-1.5-pro)")
    ap.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature (0.0..1.0)")
    ap.add_argument("--technique", default="all", help="'all' or a number 1..20")
    args = ap.parse_args()

    llm = make_llm(args.provider, args.model, args.temperature)

    if args.technique == "all":
        for idx in range(1, 21):
            name, fn = TECHNIQUES[idx]
            print("="*80)
            print(f"{idx}) {name}")
            print("-"*80)
            try:
                out = fn(llm)
            except Exception as e:
                out = f"[ERROR] {e}"
            print(out)
            print()
    else:
        try:
            idx = int(args.technique)
            if idx < 1 or idx > 20:
                raise ValueError()
        except ValueError:
            raise SystemExit("Please pass 'all' or a number 1..20 to --technique")
        name, fn = TECHNIQUES[idx]
        print(f"{idx}) {name}")
        print("-"*80)
        try:
            out = fn(llm)
        except Exception as e:
            out = f"[ERROR] {e}"
        print(out)

if __name__ == "__main__":
    main()
