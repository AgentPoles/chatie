import streamlit as st
from scripts import fetch_response
import requests
import json
import base64

st.title("Chattie")


file_ = open("./img/chatie.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

is_visible = True
# Define the container properties
container_height = 200
background_color = "#F2F2F2"  # Light gray background color
border_color = "#CCCCCC"  # Light gray border color
border_radius = 10  # Border radius in pixels
row_spacing = "20px"  # Vertical spacing between rows
column_spacing = "20px"  # Horizontal spacing between columns

if is_visible:
        # Create two rows with two columns each
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        # Function to create a container with custom CSS styling
        def create_container(height, bg_color, border_color, radius, margin):
            container_style = f"height: {height}px; background-color: {bg_color}; border: 2px solid {border_color}; padding: 20px; border-radius: {radius}px; margin: {margin};"
            return container_style
        
        image_path = "/Users/poamen/projects/pau/drp/perspective/chatie/img/chatie.png"
        # Create containers and add them to the layout with spacing
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


# Your data as a dictionary
data = {
    'Token Name': 'Chainlink',
    'Chain': 'Ethereum',
    'Chain Layer Type': 'Smart Contract Platform',
    'Founder': 'Sergey Nazarov and Steve Ellis',
    'Year': '2014',
    'Consensus Mechanism': 'Proof of Stake',
    'TPS': 'Up to 1000 transactions per second',
    'Programming Language and Framework': 'Solidity, Node.js',
    'Hex Code for Blockchain Logo Color': '#00C1FF'
}

api_key = 'cbd98ded-2b5a-4f53-9898-ddc25c13ee38'



def get_token_logo_url(token_symbol):
    try:
        # Make a request to the CoinMarketCap API to get token information
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
        params = {
            "symbol": token_symbol,
        }
        headers = {
            "X-CMC_PRO_API_KEY": api_key,  # Replace with your CoinMarketCap API key
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        if "data" in data and token_symbol in data["data"]:
            # Extract the logo URL from the response
            logo_url = data["data"][token_symbol]["logo"]
            return logo_url

    except Exception as e:
        print(f"Error fetching token logo URL: {e}")

    return None

def  prepare_output(response):
        container = st.container()
        
        # Define the CSS styles for the circular logo
      
        logo_url = get_token_logo_url(response['Token Symbol'])
          # Display the circular logo and token name side by side
       # Define the CSS styles for the circular logo (smaller and more circular)
        logo_style = f"""
            width: 20px;  /* Adjust the width as needed to reduce the size */
            height: 20px; /* Adjust the height as needed to reduce the size */
            border-radius: 50%;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 10px;  /* Add some spacing between the logo and name */
        """

# Display the circular logo and "Token Name" side by side
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
        # Get the border color from the token details
       


        # Create CSS styles to apply to the key and value
        key_style = f'background-color: #444444; padding: 5px; border: 1px solid {border_color}; display: inline-block;'
        value_style = f'padding: 5px; border: 1px solid {border_color}; display: inline-block;'

        details_text = "<div style='display: flex; flex-wrap: wrap;'>"
        details_text = ""
        for key, value in savedresponse.items():
            details_text += f"<div style='{key_style}'>{key}:</div>"
            details_text += f"<div style='{value_style}'>{value}</div>"
            details_text += "<br />"  # Add a line break after each key-value pair
            
        container.markdown(details_text, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if(message["role"] == 'assistant'):
        with st.chat_message(message["role"]):
                    response = message["content"]
                    prepare_output(response)

    else:
        with st.chat_message(message["role"],avatar="🐒"):
                    response = message["content"]
                    st.markdown(response)

# Accept user input
if prompt := st.chat_input("Howdy, enter a blockchain ..."):

    is_visible = False
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar="🐒"):
         st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = fetch_response.index(prompt)
        print(response)
        print("<<<<<<<")
        prepare_output(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


