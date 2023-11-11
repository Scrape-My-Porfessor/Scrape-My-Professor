#app.py
import streamlit as st
import pandas as pd

# Create a DataFrame to store the class and professor information
class_data = pd.DataFrame(columns=['Class Code', 'Section', 'Professor Name', 'Rating', 'Difficulty'])

# Streamlit UI
st.title("Rate My Professor Visualization")

# Sidebar for adding a class
st.sidebar.header("Add a Class")
class_code = st.sidebar.text_input("Class Code")
section = st.sidebar.text_input("Section")
professor_name = st.sidebar.text_input("Professor Name")
if st.sidebar.button("Add Class"):
    if class_code and section and professor_name:
        new_class = {
            'Class Code': class_code,
            'Section': section,
            'Professor Name': professor_name,
            'Rating': 0,
            'Difficulty': 0
        }
        class_data = class_data.append(new_class, ignore_index=True)
        st.sidebar.text("Class added!")

# Main content
st.subheader("Classes")
if not class_data.empty:
    st.table(class_data[['Class Code', 'Section', 'Professor Name']])

# Ratings
st.subheader("Rate Professors")
if not class_data.empty:
    selected_class = st.selectbox("Select a class to rate:", class_data['Professor Name'])
    rating = st.slider("Quality Rating (1-4)", 1, 4)
    difficulty = st.slider("Difficulty Level (1-4)", 1, 4)
    
    index = class_data.index[class_data['Professor Name'] == selected_class][0]
    class_data.at[index, 'Rating'] = rating
    class_data.at[index, 'Difficulty'] = difficulty

    st.text("Professor: " + selected_class)
    st.text(f"Quality Rating: {rating}/4")
    st.text(f"Difficulty Level: {difficulty}/4")

st.write(class_data)