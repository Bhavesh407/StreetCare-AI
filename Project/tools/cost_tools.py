"""Cost of language model calls, in US dollars and Indian rupees, worked out from their logged tokens.

Read-only arithmetic: nothing here calls a model or writes to the database.
"""
from config import config


def _prices(model_name):
    return config.LLM_TOKEN_PRICES_USD_PER_MILLION.get(model_name, config.LLM_DEFAULT_TOKEN_PRICES_USD)


def estimate_call_cost(model_name, prompt_tokens, response_tokens):
    """The cost of one call: prompt tokens at the input price, response tokens at the output price."""
    prices = _prices(model_name)
    usd = (prompt_tokens * prices["prompt"] + response_tokens * prices["response"]) / config.TOKENS_PER_PRICE_UNIT
    return {"usd": usd, "inr": usd * config.USD_TO_INR_RATE}


def estimate_calls_cost(calls):
    """Total cost of a list of llm_calls rows (each with model_name, prompt_tokens and response_tokens)."""
    usd = sum(estimate_call_cost(call["model_name"], call["prompt_tokens"], call["response_tokens"])["usd"]
              for call in calls)
    return {"usd": usd, "inr": usd * config.USD_TO_INR_RATE}


def format_usd(amount):
    return f"${amount:,.{config.COST_USD_DECIMALS}f}"


def format_inr(amount):
    return f"₹{amount:,.{config.COST_INR_DECIMALS}f}"
