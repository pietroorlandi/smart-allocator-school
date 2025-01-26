import streamlit as st
import calls

# application title
st.title("Resource Allocator Interface")
st.write("This app helps you to allocare resources in the best way to save money!")

# lateral bar
if "api_key" not in st.session_state:
    st.session_state.api_key = None

st.sidebar.title("Insert your API Key")
st.session_state.api_key = st.sidebar.text_input(
    "API Key",
    type="password",  # Nasconde il testo inserito
    placeholder="Insert your API Key"
)

# budget
budget = st.number_input(
    "Insert your budget",
    min_value=0.0,
    value=20000.0,
    step=500.0,
    format="%.2f"
)

# insert a state
states = [
    "Rwanda" # , "Belize"
]

selected_state = st.selectbox(
    "Select a state",
    options=states
)


# submit button
if st.button("Submit"):
    with st.spinner("Wait until the operation is finished... "):
        if st.session_state.api_key:
            optimized_allocation_mk = calls.call_optimizer(selected_state, budget, st.session_state.api_key)
            st.markdown(optimized_allocation_mk, unsafe_allow_html=True)
            # Puoi aggiungere qui il codice per elaborare la tua API Key
        else:
            st.error("Request Error!")
