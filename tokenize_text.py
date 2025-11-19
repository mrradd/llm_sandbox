import tiktoken

encoding = tiktoken.encoding_for_model("gpt-4.1-mini")

tokens = encoding.encode("Hi my name is Conrad, and I play Warhammer The Olde World.")

print(tokens)

for token_id in tokens:
    token_text = encoding.decode([token_id])
    print(f"{token_id} = {token_text}")