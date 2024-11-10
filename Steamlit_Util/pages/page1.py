import streamlit as st
import numpy as np

st.sidebar.markdown("# Streamlit Behavior")
st.markdown("# Streamlit Behavior")

st.markdown("### Streamlit Layout (example show)")
with st.container():
    st.write("This is inside the container")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg",)

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")

with st.container():
    st.write("This is inside the container")
    left, middle, right = st.columns(3)
    left.text_input("Write something")
    middle.button("Click me")
    right.checkbox("Check me")

with st.container():
    st.write("This is inside the container")
    col1, col2 = st.columns([3, 1])
    data = np.random.randn(10, 1)

    col1.subheader("A wide column with a chart")
    col1.line_chart(data)

    col2.subheader("A narrow column with the data")
    col2.write(data)

container = st.container()
container.write("This is inside the container")
st.write("This is outside the container")

# Now insert some more in the container
container.write("This is inside too")

st.markdown("### Botton")
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = not st.session_state.clicked

st.button('Show and Hide', on_click=click_button)

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    st.write('Button clicked!')
    st.slider('Select a value')

st.markdown("### Image")

st.markdown("### Grid")


