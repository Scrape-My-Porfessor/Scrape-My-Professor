import streamlit as st
import pandas as pd
import json
import ratemyprofessor
from streamlit_echarts import st_echarts
# Load the JSON data into a pandas DataFrame
with open("complete.json", "r") as json_file:
    data = json.load(json_file)

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

compare = 0

col1, col2 = st.columns(2)

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
    if compare == 1:
        st.title(f"Professor {professor_name}")
    else:    
        st.title(f"Professor {professor_name} of the %s Department." % (professor.department))
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

        st.header("Rating")
        if rating < 2.0:
            st.markdown(colored_box(formattedRating, 'red'), unsafe_allow_html=True)
        elif 2.0 < rating < 4.0:
            st.markdown(colored_box(formattedRating, 'yellow'), unsafe_allow_html=True)
        elif rating >= 4.0:
            st.markdown(colored_box(formattedRating, 'green'), unsafe_allow_html=True)

        st.header("Difficulty")
        if difficulty < 2.0:
            st.markdown(colored_box(formattedDifficulty, 'green'), unsafe_allow_html=True)
        elif 2.0 < difficulty < 4.0:
            st.markdown(colored_box(formattedDifficulty, 'yellow'), unsafe_allow_html=True)
        elif difficulty >= 4.0:
            st.markdown(colored_box(formattedDifficulty, 'red'), unsafe_allow_html=True)

        st.header("Would Take Again")
        if again < 50:
            st.markdown(colored_box(formattedAgain, 'red'), unsafe_allow_html=True)
        elif 50 < again < 70:
            st.markdown(colored_box(formattedAgain, 'yellow'), unsafe_allow_html=True)
        elif again >= 70:
            st.markdown(colored_box(formattedAgain, 'green'), unsafe_allow_html=True)

def gradeJSON(professor_name, class_name):
    # Filter the DataFrame for the specific professor and class
            filtered_data = df[(df["prof"].str.contains(professor_name, case=False)) & (df["desc"].str.contains(class_name, case=False))]

            if not filtered_data.empty:
                # Combine grades for all terms
                combined_grades = {
                    "A": 0,
                    "B": 0,
                    "C": 0,
                    "D": 0,
                    "F": 0,
                    "W": 0
                }

                for index, row in filtered_data.iterrows():
                    term_grades = row["grades"]
                    for grade, count in term_grades.items():
                        # Convert grades to integers before addition
                        if grade in combined_grades:
                            combined_grades[grade] += int(count)

                # Create a bar chart for combined grades using st_echarts
                options = {
                    "xAxis": {"type": "category", "data": list(combined_grades.keys())},
                    "yAxis": {"type": "value"},
                    "series": [
                        {"data": list(combined_grades.values()), "type": "bar", "name": "Grades", "itemStyle": {"color": "blue"}},
                    ],
                }
                st_echarts(options=options, height="500px")
            else:
                st.write("No matching results found for the specified professor and class.")
            ##########################################Pie Chart#################################################
            #Pass/Fail/Drop grades
            pass_fail_drop = {
                "Pass": ["A", "B", "C"],
                "Fail": ["D", "F"],
                "Drop": ["W"]
            }
            pass_count = fail_count = drop_count = 0
            #Combines Pass/Fail/Drop grades
            for grade, count in combined_grades.items():
                if grade in pass_fail_drop["Pass"]:
                    pass_count += count
                elif grade in pass_fail_drop["Fail"]:
                    fail_count += count
                elif grade in pass_fail_drop["Drop"]:
                    drop_count += count
            #Create the pie chart
            options = {
                "title": {"text": "Pass/Fail/Drop", "left": "center"},
                "tooltip": {"trigger": "item"},
                "legend": {"orient": "vertical", "left": "left"},
                "series": [
                    {
                        "name": "Pass/Fail/Drop",
                        "type": "pie",
                        "radius": "50%",
                        "data": [
                            {"value": pass_count, "name": "Pass", "itemStyle": {"color": "green"}},
                            {"value": fail_count, "name": "Fail", "itemStyle": {"color": "red"}},
                            {"value": drop_count, "name": "Drop", "itemStyle": {"color": "yellow"}},
                        ],
                        "emphasis": {
                            "itemStyle": {
                                "shadowBlur": 10,
                                "shadowOffsetX": 0,
                                "shadowColor": "rgba(0, 0, 0, 0.5)",
                            }
                        },
                    }
                ],
            }

            # Render the pie chart
            st_echarts(
                options=options, height="600px",
            )
st.sidebar.header("Search for a Professor or Class")
if st.sidebar.checkbox("Compare"):
    professor_name2 = st.sidebar.text_input("(Additional) Professor Name")
    class_name2 = st.sidebar.text_input("(Additional) Class Name")
    professor_name = st.sidebar.text_input("Professor Name")
    class_name = st.sidebar.text_input("Class Name")
    if st.sidebar.button("Compare"):
        compare = 1
        with col1:
            if professor_name:
                rateMyProfessor(professor_name)
                if not class_name:
                    st.subheader(f"Grades for Professor {professor_name}")
                else:
                    st.subheader(f"Grades for {class_name} by Professor {professor_name}")    
                gradeJSON(professor_name, class_name)
            elif class_name:
                st.subheader(f"Grades for {class_name}")
                gradeJSON(professor_name, class_name)   
        with col2:         
            if professor_name2:
                rateMyProfessor(professor_name2)
                if not class_name2:
                    st.subheader(f"Grades for Professor {professor_name2}")
                else:
                    st.subheader(f"Grades for {class_name2} by Professor {professor_name2}")    
                gradeJSON(professor_name2, class_name2)
            elif class_name2:
                st.subheader(f"Grades for {class_name2}")
                gradeJSON(professor_name2, class_name2)     
else:    
    professor_name = st.sidebar.text_input("Professor Name")
    class_name = st.sidebar.text_input("Class Name")
    if st.sidebar.button("Search"):
        if professor_name:
            rateMyProfessor(professor_name)
            if not class_name:
                st.subheader(f"Grades for Professor {professor_name}")
            else:
                st.subheader(f"Grades for {class_name} by Professor {professor_name}")    
            gradeJSON(professor_name, class_name)
        elif class_name:
            st.subheader(f"Grades for {class_name}")
            gradeJSON(professor_name, class_name)    