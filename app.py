import streamlit as st
import pandas as pd
import ratemyprofessor

# Create a DataFrame to store the class and professor information
class_data = pd.DataFrame(columns=['University', 'Class Code', 'Professor Name', 'Rating', 'Difficulty'])

# Streamlit UI
st.title("Rate My Professor Visualization")

# Sidebar for adding a class
st.sidebar.header("Add a Class")
university = st.sidebar.text_input("University Name")
class_code = st.sidebar.text_input("Class Code")
professor_name = st.sidebar.text_input("Professor Name")
if st.sidebar.button("Add Class"):
    if class_code and professor_name:
        professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name(university), professor_name)
        if professor is not None:
            new_class = pd.DataFrame({
                'University': [professor.school.name],
                'Class Code': [class_code],
                'Professor Name': [professor.name],
                'Rating': ["%s / 5.0" % professor.rating],
                'Difficulty': ["%s / 5.0" % professor.difficulty],
                'Would': ["%s" % round(professor.would_take_again, 1) + '%'],
                'Total_Ratings': ["%s" % professor.num_ratings]
            })
        class_data = pd.concat([class_data, new_class], ignore_index=True)
        st.sidebar.text("Class added!")

# Main content
st.subheader("Classes")
if not class_data.empty:
    st.table(class_data[['University', 'Class Code', 'Professor Name','Rating', 'Difficulty', 'Total_Ratings' ]])
