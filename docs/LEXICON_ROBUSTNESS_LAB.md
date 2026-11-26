# Lexicon Robustness Lab

A controlled research track for measuring whether language variation changes a model's interpretation of an otherwise equivalent request.

## Research question

How robustly does a model preserve intent classification and policy-relevant meaning across paraphrases, synonym substitutions, syntactic transformations, and contextual reframing?

This lab studies robustness and failure analysis. It is not a prompt-evasion toolkit and does not provide recipes for concealing harmful instructions from deployed safeguards.

## Experimental design

1. Define a benign semantic intent and its expected interpretation.
2. Create meaning-preserving variants using documented transformation labels.
3. Have evaluators independently label semantic equivalence and expected handling.
4. Submit variants to the model under identical settings.
5. Compare intent recognition, answer quality, refusal behavior, and consistency.
6. Record failures with model/version, date, configuration, and reproducible inputs.

## Transformation families

- synonym: replace a phrase with a close synonym.
- syntax: alter grammatical structure without changing meaning.
- register: change formality or conversational register.
- context: add benign context that should not alter the core intent.
- ambiguity: introduce ordinary lexical ambiguity and measure clarification behavior.
- noise: introduce harmless typographical or formatting variation.

Do not use encoded payloads, concealment schemes, or harmful operational instructions as benchmark content.

## Metrics

- Intent consistency: proportion of variants assigned the same intent label.
- Semantic preservation: human-verified proportion that retain the source meaning.
- False refusal rate: benign cases incorrectly refused.
- Unsafe acceptance rate: unsafe benchmark cases accepted when they should be declined. Use only abstract, non-operational safety test cases.
- Answer consistency: semantic similarity and rubric score across variants.
- Clarification quality: whether the model asks for clarification when ambiguity is material.

Report confidence intervals and separate human annotation disagreement from model errors. Do not treat a single model response as proof of a general vulnerability.

## Data format

Each case has an ID, a benign source request, variants, transformation labels, expected intent, and an evaluation rubric. Keep personal data and secrets out of fixtures.

## Responsible disclosure

If testing reveals a reproducible weakness in a third-party system, document the minimum evidence needed to reproduce it and report it through the provider's security or responsible-disclosure channel. Avoid publishing exploit instructions or sensitive payloads.

## Initial milestone

- Establish a small benign paraphrase set.
- Add a deterministic validator for fixture structure.
- Add a runner adapter only after provider configuration and test isolation are documented.
- Keep raw prompts, model outputs, and annotations explicitly opt-in; do not silently store user conversations.
