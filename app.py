
#importing dependencies
import streamlit as st
import requests
import base64
import openai
import urllib.parse
from decouple import config




# SECTION 1
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOGIC TO SEND REQUEST TO OPEN AI >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
openai.api_key = config('KEY')
# function for preparing and formating prompts
def generate_prompt(blockchain):
    main_prompt = """Give the token name, token symbol, chain, chain layer type, founder and year, consensus mechanism, TPS, programming language and framework, and Hex Code for Color of Blockchain Logo:"""

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
    blockchain_lower = blockchain.lower()
    if blockchain_lower in sample_prompts:
        return f"{main_prompt} {blockchain}"
    else:
        return f"{main_prompt} {blockchain}\nResponse: {{}}"
    
# core logic prompting openai
def generate_response(blockchain):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(blockchain),
        temperature=0.6,
        max_tokens=400,  
    )
    return response.choices[0].text


#function for actually sending the prompt and transforming the response
def send_to_openai_and_transform(blockchain):
        if blockchain:
            response = generate_response(blockchain)
            decoded_response = urllib.parse.unquote(response)
            response_lines = decoded_response.split('\n')
            parsed_response = {}
            for line in response_lines:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    parsed_response[key] = value

            return parsed_response
        
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



# SECTION 2
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOGIC FOR FETCHING TOKEN LOGO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

api_key = config('ORACLE_KEY')

def get_token_logo_url(token_symbol):
    try:
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        params = {
            "symbol": token_symbol,
        }
        headers = {
            "X-CMC_PRO_API_KEY": api_key, 
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if "data" in data and token_symbol in data["data"]:
            logo_url = data["data"][token_symbol]["logo"]
            return logo_url

    except Exception as e:
        print(f"Error fetching token logo URL: {e}")

    return None
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# SECTION 3
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LOGIC FOR RESPONSE DISPLAY >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def  prepare_output(response):
        container = st.container()
        logo_url = get_token_logo_url(response['Token Symbol'])

        logo_style = f"""
            width: 20px;  /* Adjust the width as needed to reduce the size */
            height: 20px; /* Adjust the height as needed to reduce the size */
            border-radius: 50%;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 10px;  /* Add some spacing between the logo and name */
        """

        container.markdown(
            f"<div style='{logo_style}'><img src='{logo_url}' alt='Token Logo'></div> <br/> ",
            unsafe_allow_html=True
        )

        st.text("") 
        border_color = response.get('Hex Code for Color of Blockchain Logo', '')
        
        savedresponse = response.copy()
        keys_to_remove = ['Token Name', 'Hex Code for Color of Blockchain Logo']
        for key in keys_to_remove:
            savedresponse.pop(key, None)

        key_style = f'background-color: #444444; padding: 5px; border: 1px solid {border_color}; display: inline-block;'
        value_style = f'padding: 5px; border: 1px solid {border_color}; display: inline-block;'

        details_text = "<div style='display: flex; flex-wrap: wrap;'>"
        details_text = ""
        for key, value in savedresponse.items():
            details_text += f"<div style='{key_style}'>{key}:</div>"
            details_text += f"<div style='{value_style}'>{value}</div>"
            details_text += "<br />" 
            
        container.markdown(details_text, unsafe_allow_html=True)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



# SECTION 4
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> GENERAL UI LOGIC>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




# SECTION 4A
#>>>>>>>>>>>>>>>>> PREPARING THE STATIC IMAGE >>>>>>>>>>>>

file_ = open("./img/chattie.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





# SECTION 4B
#>>>>>>>>>>>>>>>>> APP TITLE, OPEN_API_KEY FIELD AND CARDS >>>>>>>>>>>>


col_a, col_b =  st.columns(2)
st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: -2rem;
    }
    </style>
    """,unsafe_allow_html=True)
# Add components to the first column
with col_a:
    st.title("✨Chattie")
    
with col_b:
    text_input = st.text_input("Your Open API Key")
    if text_input:
         openai.api_key = text_input

    
is_visible = True

#card container
container_height = 200
background_color = "#F2F2F2" 
border_color = "#CCCCCC"  
border_radius = 10  
row_spacing = "20px"  
column_spacing = "20px" 

if is_visible:
        # two rows with two columns each
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        # Function to create a container with custom CSS styling
        def create_container(height, bg_color, border_color, radius, margin):
            container_style = f"height: {height}px; background-color: {bg_color}; border: 2px solid {border_color}; padding: 20px; border-radius: {radius}px; margin: {margin};"
            return container_style
        
        # creating containers and adding them to the layout with spacing
        row1_col1.markdown(
            f'<div style="{create_container(container_height, background_color, border_color, border_radius, margin=row_spacing)}">' 
            f'<div style="display: flex; justify-content: center; align-items: center; text-align: center; font-size: 24px; font-weight: bold; color:#000000; height: 100%;">'
            f'LEARN ABOUT </div> </div>',
            unsafe_allow_html=True
        )
        row1_col2.markdown(
            f'<div style="{create_container(container_height, background_color, border_color, border_radius, margin=row_spacing)}">' 
            f'<div style="display: flex; justify-content: center; align-items: center; text-align: center; font-size: 24px; font-weight: bold; color:#000000; height: 100%;">'
            f'CRYPTOCURRENCIES </div> </div>',
            unsafe_allow_html=True
        )
        row2_col1.markdown(
            f'<div style="{create_container(container_height, background_color, border_color, border_radius, margin=row_spacing)}">' 
            f'<div style="display: flex; justify-content: center; align-items: center; text-align: center; font-size: 24px; font-weight: bold; color:#000000; height: 100%;">'
            f'EASILY </div> </div>',
            unsafe_allow_html=True
        )
        row2_col2.markdown(
           f'<div style="{create_container(container_height, background_color, border_color, border_radius, margin=row_spacing)}">'
            f'<div style="display: flex; justify-content: center;">'
            f'<img src="data:image/png;base64,{data_url}"style="max-width: 160px; max-height: 160px;" alt="Image">'
            f'</div> </div>',
            unsafe_allow_html=True
        )

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




# SECTION 4C
#>>>>>>>>>>>>>>>>> CHAT DISPLAY AND LOGIC >>>>>>>>>>>>


# Initializing the  chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying chat messages from history on app rerun
for message in st.session_state.messages:
    if(message["role"] == 'assistant'):
        with st.chat_message(message["role"]):
                    response = message["content"]
                    prepare_output(response)

    else:
        with st.chat_message(message["role"],avatar="🐒"):
                    response = message["content"]
                    st.markdown(response)

# Accepting user inputs
if prompt := st.chat_input("Howdy, ask me about a cryptocurrency ..."):

    is_visible = False
    # Adding user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Displaying user message in chat message container
    with st.chat_message("user", avatar="🐒"):
         st.markdown(prompt)

    # Displaying bot response in chat message container
    with st.chat_message("assistant"):
        response = send_to_openai_and_transform(prompt)
        print(response)
        print("<<<<<<<")
        prepare_output(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


