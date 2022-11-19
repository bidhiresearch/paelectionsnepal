import pandas as pd
import plotly.express as px
import streamlit as st

st. set_page_config(page_title="२०७९ चुनाव उम्मेदवार",page_icon=":bar_chart:", layout="wide")



@st.cache
def get_data_from_excel():
    df = pd.read_excel(io='ALL_CANDIDATE_PA_2079_06_26_19_00.xlsx', engine='openpyxl', sheet_name='Eng_Data', skiprows=0, usecols="B:I")
    return df

df= get_data_from_excel()


# st.dataframe(df) # shows the complete dataset

#------------------_SIDEBAR-----------------_#
st.sidebar.header("(Choose)छान्नुहोस्")

province = st.sidebar.multiselect(
    "(Province)प्रदेश छान्नुहोस्",
    options=df["Province"].unique(),
    default=df["Province"].unique()
)

province_sel = df.query(
    "Province == @province"
)


# st.dataframe(province_sel) # displays dataframe for selected province

district = st.sidebar.multiselect(
    "(District)जिल्ला छान्नुहोस्",
    options=province_sel["District"].unique(),
    default=province_sel["District"].unique()
)

district_sel = df.query(
    "District == @district"
)

# st.dataframe(district_sel)  # displays dataframe for selected province and districts


party = st.sidebar.multiselect(
    "(Party)पार्टी छान्नुहोस्",
    options=district_sel["Party"].unique(),
    default=district_sel["Party"].unique()
)

party_sel = df.query(
    "Party == @party & District == @district"
)

# st.dataframe(party_sel) # displays dataframe for selected province, districts and party


# gender filter
gender = st.sidebar.multiselect(
    "(Gender)लिङ्ग छान्नुहोस्",
    options=district_sel["Gender"].unique(),
    default=district_sel["Gender"].unique()
)

gender_sel = df.query(
    "Gender == @gender & District == @district & Party == @party"
)



# st.dataframe(district_sel)



#--------------------------MAINPAGE-------------------__#

st.title(":flag-np:प्रदेश सभा सदस्य निर्वाचन तर्फको उम्मेदवारीको विवरण ")
st.markdown('##')

# Analytics
total_candidates = district_sel.shape[0]
total_independent = len(district_sel[district_sel["Party"]=="स्वतन्त्र"])
# # total_female = gender_sel["महिला"].sum()

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("जम्मा उम्मेदवार")
    st.subheader(total_candidates)


with right_column:
    st.subheader("जम्मा स्वतन्त्र उम्मेदवार")
    st.subheader(total_independent)

st.markdown("---")

st.markdown("## उम्मेदवारहरुको तालिका ")
st.dataframe(gender_sel)


#--------------------Analytics--------##

candidates_by_gender = (
    gender_sel.groupby(by=["Gender"]).count()[['Party']]

)

fig_gender_bar = px.bar(
    candidates_by_gender,
    x= "Party",
    y=candidates_by_gender.index,
    labels={
        "Party": "जम्मा(Total)",
        "Gender": "लिङ्ग",
        },
    orientation='h',
    title="<b>लिङ्गको आधारमा उम्मेदवारहरु</b>",
    template= "plotly_white",
)

fig_gender_bar.update_layout(
    plot_bgcolor= "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)

st.plotly_chart(fig_gender_bar)



#-------------------candidates by party 

candidates_by_party = (
    gender_sel.groupby(by=["Party"]).count()[['Age']]
)

fig_party_bar = px.bar(
    candidates_by_party,
    x= candidates_by_party.index,
    y= "Age",
    labels={
        "Age": "जम्मा(Total)",
        "Party": "पार्टी",
        },
    title="<b>पार्टीको आधारमा उम्मेदवारहरु</b>",
    template= "plotly_white",
)

fig_party_bar.update_layout(
    plot_bgcolor= "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
)

st.plotly_chart(fig_party_bar)



st.markdown("Made for Educational Purpose Only. Based on data provided by [Election Commission Nepal.](https://election.gov.np/np/page/candidate-list-hor)")


#--- hide streamlit style


hide_st_style= """
    <style>

    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    </style>

"""

st.markdown(hide_st_style, unsafe_allow_html=True)