st.set_page_config(
    page_title="2% Resource Control", layout="wide"
)

st.sidebar.success("Select Percentage of Resource Control Above")

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)
st.write("# 2% Resource Control")



st.markdown(
    """
<style>
    div[data-testid="stExpander"] details summary p{
    font-size: 2rem;
}
</style>
""",
    unsafe_allow_html=True,
)


col1, col2 = st.columns([4, 1])
column_config={"Resource":"Resource",
            "Total Price to Control 2% in ETH":"Price for Plots (ETH)",
            "Number of Plots Needed for 2% Control": "# of Plots Needed",
            "Plot IDs for Sale":"Plot IDs",
            "Rarity Ranking (Lowest is Rarest)":"Rarity",
            "Total Number of Resource on All Plots":"Total # On All Plots",
            "Type":"Type"}
col2.write("Resources that 2% can not be purchased")
with col1:
    placeholder = st.container()
    placeholder2=st.container()
    placeholder3 = st.expander("To see breakdown of the data used for the visualization, click here for a table")
    exclude2 = placeholder2.toggle('Include Very Common Ranked 60-74 Resources',value=False, help="These resources are very plentiful, acquiring 2% would be very expensive. Turning this on makes the scale of the graph much larger.", key="toggle2")
    opensea_flag2=placeholder2.toggle('Exclude Plots That are Flagged by Opensea', value=False,help="NFTs flagged by Opensea marketplace are untradeable on Opensea, and usually trade at a discount on other marketplaces as they might be stolen.",key="opensea2" )   
    if exclude2 ==False and opensea_flag2==False:
        with placeholder.container():
            data_false_false_tuple=load_data(2,"with","yes")
            data_false_false=data_false_false_tuple[0]
            make_graph(data_false_false,2)
        with placeholder3.container():
            placeholder3.dataframe(data_false_false,column_config=column_config)
        data_false_false_zero=data_false_false_tuple[1]
        col2.dataframe(data_false_false_zero,hide_index=True)

    if exclude2 ==True and opensea_flag2==False:
        with placeholder.container():
            data_true_false_tuple=load_data(2,"with","no")
            data_true_false=data_true_false_tuple[0]
            make_graph(data_true_false,2)
        with placeholder3.container():
            placeholder3.dataframe(data_true_false,column_config=column_config)
        data_true_false_zero=data_true_false_tuple[1]
        col2.dataframe(data_true_false_zero, hide_index=True)

    if exclude2==False and opensea_flag2==True:
            with placeholder.container():
                data_false_true_tuple=load_data(2,"without","yes")
                data_false_true=data_false_true_tuple[0]
                make_graph(data_false_true,2)
            with placeholder3.container():
                placeholder3.dataframe(data_false_true,column_config=column_config)
            data_false_true_zero=data_false_true_tuple[1]
            col2.dataframe(data_false_true_zero, hide_index=True)

    if exclude2==True and opensea_flag2==True:
            with placeholder.container():
                data_true_true_tuple=load_data(2,"without","no")
                data_true_true=data_true_true_tuple[0] 
                make_graph(data_true_true,2)
            with placeholder3.container():
                placeholder3.dataframe(data_true_true,column_config=column_config)
            data_true_true_zero=data_true_true_tuple[1]
            col2.dataframe(data_true_true_zero,hide_index=True)
