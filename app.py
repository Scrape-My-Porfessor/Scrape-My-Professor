import streamlit as st
import pandas as pd
import json
import ratemyprofessor
from streamlit_echarts import st_echarts
import plotly.express as px
# Load the JSON data into a pandas DataFrame
with open("complete.json", "r") as json_file:
    data = json.load(json_file)

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

compare = 0
title = 0

col1, col2 = st.columns(2)
col3, col4 = st.columns([0.6, 0.4])

container = st.container()

rating = 0.0
formattedRating = "N/A"

difficulty = 0.0
formattedDifficulty = "N/A"

again = 0.0
formattedAgain = "N/A"

title_style = 'text-align: center;'
header_style = 'text-align: center; color: green;'


def colored_box(value, color):
    return f'<div style="background-color:{color}; padding:10px; border-radius:10px; max-width: 80px; text-align: center;">{value}</div>'


def checkFields(name1, name2):
    return name1.strip().lower() == name2.strip().lower() if name1 and name2 else False

def rateMyProfessor(professor_name):
    professor = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name("University of North Texas"), professor_name)
    if professor is None:
        st.title("Professor Not Found!")
    else: 
        if compare == 1:
            st.title(f"Professor {professor_name}")
        else:    
            st.title(f"Professor {professor_name} of the %s Department." % (professor.department))   
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
            st.markdown(colored_box(formattedRating, '#eb2d3a'), unsafe_allow_html=True)
        elif 2.0 < rating < 4.0:
            st.markdown(colored_box(formattedRating, '#ffec00'), unsafe_allow_html=True)
        elif rating >= 4.0:
            st.markdown(colored_box(formattedRating, '#50b458'), unsafe_allow_html=True)

        st.header("Difficulty")
        if difficulty < 2.0:
            st.markdown(colored_box(formattedDifficulty, '#50b458'), unsafe_allow_html=True)
        elif 2.0 < difficulty < 4.0:
            st.markdown(colored_box(formattedDifficulty, '#ffec00'), unsafe_allow_html=True)
        elif difficulty >= 4.0:
            st.markdown(colored_box(formattedDifficulty, '#eb2d3a'), unsafe_allow_html=True)

        st.header("Would Take Again")
        if again < 50:
            st.markdown(colored_box(formattedAgain, '#eb2d3a'), unsafe_allow_html=True)
        elif 50 < again < 70:
            st.markdown(colored_box(formattedAgain, '#ffec00'), unsafe_allow_html=True)
        elif again >= 70:
            st.markdown(colored_box(formattedAgain, '#50b458'), unsafe_allow_html=True)

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

        # Create a bar chart for combined grades using Plotly
        df_combined = pd.DataFrame({
            'Grade': list(combined_grades.keys()),
            'Count': list(combined_grades.values())
        })

        fig = px.bar(
            df_combined, x='Grade', y='Count',
            color='Grade',
            labels={'Count': 'Count', 'Grade': 'Grades'},
            color_discrete_map={'A': '#50b458', 'B': '#ffec00', 'C': 'orange', 'D': 'maroon', 'F': '#eb2d3a', 'W': 'grey'},
        )
        if compare == 0:
            fig.update_layout(width=700)
        else:
            fig.update_layout(width=350)        
        st.plotly_chart(fig)

    else:
        st.write("No matching results found for the specified professor and class.")


def pi(professor_name, class_name):
            ##########################################Pie Chart#################################################
            #Pass/Fail/Drop grades
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
                    "title": {"text": "Pass/Fail/Drop", "left": "center", "top": "37%"},
                    "tooltip": {"trigger": "item", "top": "37%"},
                    "legend": {"orient": "vertical", "left": "left", "top": "37%"},
                    "series": [
                        {
                            "name": "Pass/Fail/Drop",
                            "type": "pie",
                            "radius": "70%",
                            "top": "40%",
                            "data": [
                                {"value": pass_count, "name": "Pass", "itemStyle": {"color": "#50b458"}},
                                {"value": fail_count, "name": "Fail", "itemStyle": {"color": "#eb2d3a"}},
                                {"value": drop_count, "name": "Drop", "itemStyle": {"color": "#ffec00"}},
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
                    options=options, height="600px"
                )
            else:
                st.write("")

st.sidebar.header("Search for a Professor or Class")
if st.sidebar.checkbox("Compare"):
    professor_name2 = st.sidebar.text_input("(Additional) Professor Name", placeholder = "First Last")
    class_name2 = st.sidebar.text_input("(Additional) Class Name", placeholder = "Class Name")
    professor_name = st.sidebar.text_input("Professor Name", placeholder = "First Last")
    class_name = st.sidebar.text_input("Class Name", placeholder = "Class Name")
    if st.sidebar.button("Compare"):
        title = 1
        if checkFields(professor_name, professor_name2):
            st.text("Fields are the same!")
        elif checkFields(class_name, class_name2):
            st.text("Fields are the same!")
        else:    
            compare = 1
            with col1:
                if professor_name:
                    rateMyProfessor(professor_name)
                    if not class_name:
                        st.subheader(f"Grades for Professor {professor_name}")
                    else:
                        st.subheader(f"Grades for {class_name} by Professor {professor_name}")    
                    gradeJSON(professor_name, class_name)
                    pi(professor_name, class_name)
                elif class_name:
                    st.subheader(f"Grades for {class_name}")
                    gradeJSON(professor_name, class_name)   
                    pi(professor_name, class_name) 
            with col2:         
                if professor_name2:
                    rateMyProfessor(professor_name2)
                    if not class_name2:
                        st.subheader(f"Grades for Professor {professor_name2}")
                    else:
                        st.subheader(f"Grades for {class_name2} by Professor {professor_name2}")    
                    gradeJSON(professor_name2, class_name2)
                    pi(professor_name2, class_name2)
                elif class_name2:
                    st.subheader(f"Grades for {class_name2}")
                    gradeJSON(professor_name2, class_name2)  
                    pi(professor_name2, class_name2)   
else:    
    professor_name = st.sidebar.text_input("Professor Name", placeholder = "First Last")
    class_name = st.sidebar.text_input("Class Name", placeholder = "Class Name")
    if st.sidebar.button("Search"):
        title = 1
        if professor_name:
            with col3:
                rateMyProfessor(professor_name)
            if not class_name:
                st.subheader(f"Grades for Professor {professor_name}")
            else:
                st.subheader(f"Grades for {class_name} by Professor {professor_name}")    
            gradeJSON(professor_name, class_name)
            with col4:
                pi(professor_name, class_name)
        elif class_name:
            st.subheader(f"Grades for {class_name}")
            gradeJSON(professor_name, class_name)
            with col4:  
                pi(professor_name, class_name)  

if title == 0:
    st.markdown('<h1 style="{}">Welcome to Scrape My Professor</h1>'.format(title_style), unsafe_allow_html=True)
    st.markdown('<h2 style="{}">(UNT Edition)</h2>'.format(header_style), unsafe_allow_html=True)
    st.markdown('<h1 style="{}">Please Enter Professor or Class Name</h1>'.format(title_style), unsafe_allow_html=True)           
