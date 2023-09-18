import os
import urllib.parse
import json
import openai



openai.api_key = "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"

def generate_response(blockchain):
    # Generate the prompt using the provided blockchain name
    prompt = generate_prompt(blockchain)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(blockchain),
        temperature=0.6,
        max_tokens=400,  # Increase this value to allow for longer responses
    )
    # Return the GPT-3 generated response
    return response.choices[0].text



def index(blockchain):
        if blockchain:
            # Process the blockchain name and generate a response
            response = generate_response(blockchain)
            

            # URL-decode the response
            decoded_response = urllib.parse.unquote(response)

            # Split the response into lines
            response_lines = decoded_response.split('\n')

            # Initialize a dictionary to store the parsed response
            parsed_response = {}

            # Iterate through the lines and parse key-value pairs
            for line in response_lines:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    parsed_response[key] = value

            return parsed_response
    


def generate_prompt(blockchain):
    # Define the main prompt question
    main_prompt = """Give the token name, token symbol, chain, chain layer type, founder and year, consensus mechanism, TPS, programming language and framework, and Hex Code for Color of Blockchain Logo:"""

    # Define sample responses for Ethereum and Polkadot
    sample_prompts = {
        "ethereum": """Blockchain: Ethereum
Response: {{
    "Token_Symbol": "ETH",
    "Consensus_Mechanism": "Proof Of Stake",
    "TPS": "15 to 45",
    "Programming_Language_and_Framework": "Go, C++, EVM",
    "Hex Code for Color of Blockchain Logo": "#3C3C3D"
}}""",
        "polkadot": """Blockchain: Polkadot
Response: {{
    "Token_Symbol": "DOT",
    "Consensus_Mechanism": "Nominated Proof-of-Stake, Grandpa (GHOST-based Recursive Ancestor Deriving Prefix Agreement)",
    "TPS": "1000",
    "Programming_Language_and_Framework": "Rust, C++, Go, WebAssembly (Wasm), WASM",
    "Hex Code for Color of Blockchain Logo": "#E6007A"
}}""",
    }

    # Check if the blockchain input matches a sample prompt
    blockchain_lower = blockchain.lower()
    if blockchain_lower in sample_prompts:
        return f"{main_prompt} {blockchain}"
    else:
        return f"{main_prompt} {blockchain}\nResponse: {{}}"




