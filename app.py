import streamlit as st
import pandas as pd
import ratemyprofessor


# Streamlit UI
st.title("Rate My Professor Visualization")

container = st.container()

rating = 0.0
formattedRating = "N/A"

difficulty = 0.0
formattedDifficulty = "N/A"

again = 0.0
formattedAgain = "N/A"

def colored_box(value, color):
    return f'<div style="background-color:{color}; padding:10px; border-radius:10px; max-width: 80px; text-align: center;">{value}</div>'


# Sidebar for adding a class
st.sidebar.header("Search for a Professor or Class")
professor_name = st.sidebar.text_input("Professor Name")
class_name = st.sidebar.text_input("Class Code")
if st.sidebar.button("Search"):
    if professor_name:
        professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of North Texas"), professor_name)
        if professor is None:
            st.text("Professor Not Found!")
        else:    
            rating = float(professor.rating)
            formattedRating = "%.1f / 5.0" % professor.rating

            difficulty = float(professor.difficulty)
            formattedDifficulty = "%.1f / 5.0" % professor.difficulty

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
                container.markdown(colored_box(formattedDifficulty, 'red'), unsafe_allow_html=True)
            elif 2.0 < difficulty < 4.0:
                container.markdown(colored_box(formattedDifficulty, 'yellow'), unsafe_allow_html=True)
            elif difficulty >= 4.0:
                container.markdown(colored_box(formattedDifficulty, 'green'), unsafe_allow_html=True)

            container.header("Would Take Again")
            if again < 50:
                container.markdown(colored_box(formattedAgain, 'red'), unsafe_allow_html=True)
            elif 50 < again < 70:
                container.markdown(colored_box(formattedAgain, 'yellow'), unsafe_allow_html=True)
            elif again >= 70:
                container.markdown(colored_box(formattedAgain, 'green'), unsafe_allow_html=True)

            st.sidebar.text("Professor Found!")
    