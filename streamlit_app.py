# Import python packages.
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import streamlit as st
cnx = st.connection("snowflake")
session = cnx.session()
# Write directly to the app.
st.title(f"Customize YOUR Smoothie :cup_with_straw: {st.__version__}")
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

import streamlit as st
import requests
name_on_order = st.text_input("Name Of Smoothie:")
st.write("The name of YOUR smoothie will be:", name_on_order)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:"
     ,my_dataframe
     ,max_selections = 5
)
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutritional Information')
        smoothiefroot_response = requests.get("https://www.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Smoothie_Name)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    insertdata = st.button('Submit Order')
    if insertdata:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Smoothie_Name)
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)    
    #st.stop ()
    insertdata = st.button('Submit Order')
    if insertdata:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
  

