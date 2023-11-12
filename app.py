import streamlit as st
import pandas as pd
import json
import ratemyprofessor

# Load the JSON data into a pandas DataFrame
with open("complete.json", "r") as json_file:
    data = json.load(json_file)

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title("Scrape My Professor")
container = st.container()

rating = 0.0
formattedRating = "N/A"

difficulty = 0.0
formattedDifficulty = "N/A"

again = 0.0
formattedAgain = "N/A"

def colored_box(value, color):
    return f'<div style="background-color:{color}; padding:10px; border-radius:10px; max-width: 80px; text-align: center;">{value}</div>'

def rateMyProfessor(professor_name):
    professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of North Texas"), professor_name)
    if professor is None:
        st.text("Professor Not Found!")
    else:    
        rating = float(professor.rating)
        formattedRating = "%.1f / 5.0" % professor.rating

        difficulty = float(professor.difficulty)
        formattedDifficulty = "%.1f / 5.0" % professor.difficulty

        if professor.would_take_again is None:
            again = float(0)
            formattedAgain = f"0%"
        else:    
            again = float(professor.would_take_again)
            formattedAgain = f"{round(professor.would_take_again, 1)}%"

        container.header("Rating")
        if rating < 2.0:
            container.markdown(colored_box(formattedRating, 'red'), unsafe_allow_html=True)
        elif 2.0 < rating < 4.0:
            container.markdown(colored_box(formattedRating, 'yellow'), unsafe_allow_html=True)
        elif rating >= 4.0:
            container.markdown(colored_box(formattedRating, 'green'), unsafe_allow_html=True)

        container.header("Difficulty")
        if difficulty < 2.0:
            container.markdown(colored_box(formattedDifficulty, 'green'), unsafe_allow_html=True)
        elif 2.0 < difficulty < 4.0:
            container.markdown(colored_box(formattedDifficulty, 'yellow'), unsafe_allow_html=True)
        elif difficulty >= 4.0:
            container.markdown(colored_box(formattedDifficulty, 'red'), unsafe_allow_html=True)

        container.header("Would Take Again")
        if again < 50:
            container.markdown(colored_box(formattedAgain, 'red'), unsafe_allow_html=True)
        elif 50 < again < 70:
            container.markdown(colored_box(formattedAgain, 'yellow'), unsafe_allow_html=True)
        elif again >= 70:
            container.markdown(colored_box(formattedAgain, 'green'), unsafe_allow_html=True)

def gradeJSON(professor_name, class_name):
    filtered_data = df[(df["prof"].str.contains(professor_name, case=False)) & (df["desc"].str.contains(class_name, case=False))]

    if filtered_data.empty:
        st.text("No matching grades found for professor or class")
    else:
        # Create a bar chart for grades
        if "grades" in filtered_data.columns:
            grades = filtered_data["grades"].apply(pd.Series).astype(float)
            st.bar_chart(grades.T, use_container_width=True)

st.sidebar.header("Search for a Professor or Class")
professor_name = st.sidebar.text_input("Professor Name")
class_name = st.sidebar.text_input("Class Name")
if st.sidebar.button("Search"):
    if professor_name:
        rateMyProfessor(professor_name)
        if not class_name:
            st.subheader(f"Grades for Professor {professor_name}")
        else:
            st.subheader(f"Grades for Professor {professor_name} and {class_name}")    
        gradeJSON(professor_name, class_name)
    elif class_name:
        st.subheader(f"Grades for {class_name}")
        gradeJSON(professor_name, class_name)    
