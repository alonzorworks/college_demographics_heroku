import pandas as pd 
#import numpy as np 
import streamlit as st 
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly
from streamlit_lottie import st_lottie
import requests



#NOTE Import Pictures 
def load_lottieurl(url):
    """If the lottie file does not display the image return nothing. This will prevent errors when trying to display the Lottie Files.
    Requires importing packages streamlit_lottie and requests"""
    r = requests.get(url)
    if r.status_code != 200:
        return None 
    return r.json()

def lottie_credit(credit):
    return st.markdown(f"<p style='text-align: center; color: gray;'>{credit}</p>", unsafe_allow_html=True)
    #return st.caption(credit)


df = pd.read_csv("college_degree_cleaned.csv")
st.title("College Information Demographic and Tuition :mortar_board: :school: :apple:")

# Camp is short for campus. Pictures of a school.
camp1 = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_pkxipgnh.json")
camp2 = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_wldncgll.json")
camp3 = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_bcsshanh.json")

# ca1, ca2, ca3 = st.columns(3)
# with ca1:
#     st_lottie(camp1, height = 400, key = "camp1")
# with ca2:
#     st_lottie(camp2, height = 400, key = "camp2")
# with ca3:
#     st_lottie(camp3, height = 400, key = "camp3")

ca1, ca2 = st.columns(2)
with ca1:
    st.subheader("Dataset Information/Credit")
    st.write("This dataset was uploaded by Jesse Mostipak. Mostipak is a Developer Advocate at RStudio. She derrived the dataset from various sources. These sources include National Center for Education Statistics (NCES), Chronicle of Higher Education, Pricenomics, TuitionTracker.org and Payscale. (However the Payscale information is not included in this dataframe because it was included in another CSV file that could not be joined.) However the payscale information may be explored in a future project). The data was cleaned by Thomas Mock.\n \n The two files utilized for this projects are the 'diversity.csv' and the 'tuition.csv' files that was joined into a single dataframe in pandas.")

with ca2:
    st_lottie(camp2, height = 500, key = "camp2")
    lottie_credit("The Library by Doug Fuchs LottieFiles")

st.subheader("Breakdown of The Variables")
st.write("The dataframe utilized in this dataset comes from two seperate CSV files.")

with st.expander("See the Variables Used in This Dataframe"):
    tab1, tab2 = st.tabs(["Diversity Dataset Breakdown", "Tuition Cost Dataset Breakdown"])
    with tab1:
        #st.write("diversity_school.csv")
        st.write("""diversity_school.csv \n
        name - School name
        total_enrollment = Total enrollment of students
        state - State name 
        category - Group/Racial/Gender category
        enrollment - enrollment by category
        """)
    with tab2:
        st.write("tuition_cost.csv")
        st.write("""room_and_board - Room and board in USD \n
        in_state_tuition - Tuition for in-state residents in USD
        in_state_total - Total cost for in-state residents in USD (sum of room and board + in-state tuition)
        out_of_state_tuition - Tuition for out-of-state residents in USD
        out_of_state_total - Total cost for out-of-state residents in USD (sum of room and board + out-of_state tuition)
        """)

football = load_lottieurl("https://assets10.lottiefiles.com/private_files/lf30_muej992g.json")
yard = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_pkxipgnh.json")

st.subheader("Project Purpose and Explanation  :school_satchel:")
pic1, pic2 = st.columns(2)
with pic1:
    st_lottie(football ,height = 400, key = "football")
    lottie_credit("The Stadium by Doug Fuchs LottieFiles")
with pic2:
    st_lottie(yard, height = 400, key = "yard")
    lottie_credit("The Yard by Doug Fuchs LottieFiles")


st.write("This project allows for people interested in pursuing higher education to  explore some of their options. Relevant options can be found using the filters below. It also gives more information about the schools such as the total ammount of students enrolled, diversity, in-state/out-of-state tuition, room and board fees (when available) etc.")


st.subheader("Filter the Data")
data_filter = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_u4liqX.json")
st_lottie(data_filter, height = 400, key = "filter")
lottie_credit("Omnisci Spot3 by Doug Fuchs on LottieFiles")

st.write("Filters are available to help narrow down the data presented to you. By default all of the data is shown. It is recommended that you take a look at the dataset without modifying any of the filters first, because once you change one or more of the filters it will affect all of the data presented.")

# NOTE Beggining of the Filter section
# Sliders Needed: enrollment, in_state_tuition, in_state_total, out_of_state_tuition, out_of_state_total
def slide_creator(column, step_pick):
    """Can create sliders in a single coding function. It returns something that can be used as a filter. """
    ranges = df[column].unique().tolist()
    ranger = st.slider(f"Select a range of values for {column}.",
    min_value = min(ranges),
    max_value = max(ranges),
    value = (min(ranges), max(ranges)),
    step = step_pick
    )
    st.caption(f"Selected Minimum Value:  {ranger[0]: ,}")
    st.caption(f"Selected Maximum Value: {ranger[1]: ,}")
    # return ranger
    return df[column].between(*ranger)

def multi_choose(column_name):
        listing = df[column_name].unique().tolist()
        listing.sort()
        checkbox_all = st.checkbox(f"Select all for {column_name}.", key = column_name, value = True)


        

        if checkbox_all:
            select = st.multiselect(f"Select values from {column_name} that you wish to select.", listing, default = listing)
        else:
            select = st.multiselect(f"Select values from {column_name} that you wish to select.", listing)

        return (df[column_name].isin(select))

with st.expander("Click to See the Filters"):
    mask = slide_creator("enrollment", 500) & slide_creator("in_state_tuition", 1000) & slide_creator("out_of_state_tuition", 1000) & slide_creator("in_state_total", 1000) & slide_creator("out_of_state_total", 1000) & multi_choose("state") & multi_choose("type") & multi_choose("degree_length")

df = df[mask]

# df = pd.read_csv("college_degree_cleaned.csv")

df
st.subheader("Total Students Enrolled in Each University")
b_enroll = px.bar(df.groupby("name", as_index= False).median().sort_values(by = "total_enrollment",ascending= False) , x = "name", y = "total_enrollment", width = 1100, height = 700)
# b_enroll.update_traces(width = 4)
st.plotly_chart(b_enroll)


# Selectors: State, type, degree

# Categorical Count Histogram 
def histomaker(column_name):
    """Note that the name of the university is also a central factor in grouping. It does not even have to be passed in.
    Because the other variable is unspecified we name it after Uni.
    
    """
    df_uni_grouped = df.groupby(["name", column_name]).count().reset_index()
    uni_single_list = df_uni_grouped[column_name].to_list()
    # Histogram is the easiest way to make a countplot.
    uni_chart = px.histogram(histfunc = "count", x = uni_single_list, text_auto = True, width = 1000).update_xaxes(categoryorder = "total descending")
    st.plotly_chart(uni_chart)

st.subheader("Colleges Per State :earth_americas:")
histomaker("state")

st.subheader("Countplot of Type of College :pencil2:")
histomaker("type")

st.subheader("Countplot of Program Length")
histomaker("degree_length")

#Grouped Dataset
df_grouped = df.groupby(["name", "category"]).sum().reset_index()

# Pie Chart
pie_chart_demo = px.pie(df_grouped, values = "enrollment", names = "category", title = "Breakdown of Student Demographics for All Schools")
st.plotly_chart(pie_chart_demo)

bar_chart_demo = px.bar(df_grouped.groupby("category").sum().reset_index() , x = "category", y = "enrollment", color = "category", text_auto = True, title = "College Enrollment by Demographic", width = 1000, height = 700)
st.plotly_chart(bar_chart_demo)


#NOTE in state vs out of state 
df_uni_grouped = df.groupby("name").min().reset_index()
chart = px.bar(df_uni_grouped, x = "name", y = ["in_state_tuition", "out_of_state_tuition"], text_auto = True, barmode = "group", title = f"In State and Out of State Tuition", width = 1000, height = 700 , color_discrete_sequence= ["#FFBC0A", "#87255B"])
st.plotly_chart(chart)

# In State Only 
in_state = px.bar(df_uni_grouped.sort_values("in_state_tuition", ascending = False), x = "name", y = ["in_state_tuition"], text_auto = True, barmode = "group", title = f"In State Tuition", width = 1000, height = 700 , color_discrete_sequence= ["#FFBC0A"])
st.plotly_chart(in_state)

# Out of State Only 
out_state = px.bar(df_uni_grouped.sort_values("out_of_state_tuition", ascending = False), x = "name", y = ["out_of_state_tuition"], text_auto = True, title = f"Out of State Tuition", width = 1000, height = 700 , color_discrete_sequence= ["#87255B"])
st.plotly_chart(out_state)



# NOTE Room and Board
# Sort df by room board
uni_rb = df_uni_grouped.sort_values("room_and_board",  ascending = False)
room_board = px.bar(uni_rb.loc[df_uni_grouped["room_and_board"] > 1], x = "name", y = "room_and_board", text_auto = True, title = "Room and Board Cost", width = 1000, height = 700 , color_discrete_sequence = ["#582630"])
st.plotly_chart(room_board)


null_room_board = pd.isnull(df["room_and_board"])
no_rb_info = df.loc[null_room_board]["name"].unique()
no_rb_info.sort()

with st.expander("Click to see a list of colleges with no room and board information."):
    no_rb_info

# NOTE Room and Board In State vs out of State TOTAL
valid_rb = pd.notnull(df_uni_grouped["room_and_board"])
total_cost = px.bar(df_uni_grouped.loc[valid_rb], x = "name", y = ["in_state_total", "out_of_state_total"], text_auto = True, barmode = "group", title = f"Total Cost of Attendance (Tuition + Room & Board) In State and Out of State", width = 1000, height = 700 , color_discrete_sequence= ["#5DA9E9", "#F26157"])
st.plotly_chart(total_cost)

# In State 
state_total = px.bar(df_uni_grouped.loc[valid_rb].sort_values("in_state_total", ascending= False), x = "name", y = ["in_state_total"], text_auto = True, barmode = "group", title = f"Total Cost of Attendance (Tuition + Room & Board) In State", width = 1000, height = 700 , color_discrete_sequence= ["#5DA9E9"])
st.plotly_chart(state_total)

# Out of State 
out_total = px.bar(df_uni_grouped.loc[valid_rb].sort_values("out_of_state_total", ascending= False), x = "name", y = ["out_of_state_total"], text_auto = True, barmode = "group", title = f"Total Cost of Attendance (Tuition + Room & Board) Out of State", width = 1000, height = 700 , color_discrete_sequence= ["#F26157"])
st.plotly_chart(out_total)


non_minority_students = df_grouped["total_enrollment"].sum() - df_grouped.loc[df_grouped["category"] ==  "Total Minority"]["enrollment"].sum() 
non_minority_students = f"{non_minority_students: ,}"

#Calculations 
st.subheader("Demographic Population Calculations")
st.write("The data must be wrangled to ensure that the total minority count is not over conted. Students can fall into multiple categories/designations. I.e Black women and the like are double minorities due to their race and sex. In addition to this Hispanic is not considered a racial designation in the US meaning they have to choose a racial identifier such as black or white. In addition to this certain columns contains a certain repeated value for the whole column for each school. (For example the column total_enrollment is repeated 11 times for each school). Since this process is slightly convulted a code snippet is provided below which should help elucidate this process.")
# Total Students enrolled in College
total_students = df_grouped.groupby("name").min().reset_index()["total_enrollment"].sum()
total_students = f"{total_students: ,}"
st.write("Total Number of students enrolled in college in 2014.", df_grouped.groupby("name").min().reset_index()["total_enrollment"].sum(),"(", total_students, ")")
st.code('df_grouped.groupby("name").min().reset_index()["total_enrollment"].sum()')
st.write(""" \n \n \n \n \n \n """)

# Minority Students Enrolled in College
total_minorities = df_grouped.loc[df_grouped["category"] ==  "Total Minority"]["enrollment"].sum()
total_minorities = f"{total_minorities: ,}"
st.write("Total Number of Minority Students Enrolled in College", df_grouped.loc[df_grouped["category"] ==  "Total Minority"]["enrollment"].sum(), "(",total_minorities, ")")
st.code('df_grouped.loc[df_grouped["category"] ==  "Total Minority"]["enrollment"].sum()')
st.write(""" \n \n \n \n \n \n """)

# Majority Students 
total_major = df_grouped.groupby("name").min().reset_index()["total_enrollment"].sum() - df_grouped.loc[df_grouped["category"] ==  "Total Minority"]["enrollment"].sum()
total_major_format = f"{total_major: ,}"
st.write("Total number of Non-minority students", total_major, "(", total_major_format, ")")
st.code('df_grouped.groupby("name").min().reset_index()["total_enrollment"].sum() - df_grouped.loc[df_grouped["category"] ==  "Total Minority"]["enrollment"].sum()')



def tuition_mapper(school_name):
    chart = px.bar(df_uni_grouped[df_grouped["name"] == f"{school_name}"], x = "name", y = ["in_state_tuition", "out_of_state_tuition"], text_auto = True, barmode = "group", title = f"{i} - In State and Out of State Tuition", color_discrete_sequence= ["#F95738", "#C7F0BD"])
    st.plotly_chart(chart)


with st.expander("Click to see in-state and out of state tuition for the colleges."):
    uni_list = df["name"].unique().tolist()
    uni_list.sort()

