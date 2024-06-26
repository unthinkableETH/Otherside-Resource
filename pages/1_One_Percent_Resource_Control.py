import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,Legend
from bokeh.io import curdoc
from bokeh.transform import factor_cmap
from bokeh.models import BasicTickFormatter

st.set_page_config(
    page_title="1% Resource Control", layout="wide"
)

st.sidebar.success("Select Percentage of Resource Control Above")

#Hides fullscreen button that was interfering with the legend
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)
st.write("# 1% Resource Control")


resource_type=["Ore","Anima","Root","Shard"]

#pulls data from s3 bucket that I created
def load_data(percent,with_or_without_flag,exclude_yes_or_no):
    data=pd.DataFrame()
    data_zero=pd.DataFrame()
    s3="s3://otherside-resource/"+str(percent)+'%TotalPrice_'+str(with_or_without_flag)+'_flag.csv'
    data=pd.read_csv(s3, index_col=0)
    s3_zero="s3://otherside-resource/"+str(percent)+'%TotalPrice_'+str(with_or_without_flag)+'_flag_zero.csv'
    data_zero=pd.read_csv(s3_zero)
    data_zero_exclude=data_zero.loc[data_zero['Rarity'] <=59]
    data_with_exclude=data.loc[data['Rarity Ranking (Lowest is Rarest)'] <=59]
    if exclude_yes_or_no =='yes':
        return(data_with_exclude,data_zero_exclude)
    if exclude_yes_or_no == 'no':
         return(data,data_zero)

#makes graph using bokeh
def make_graph(data_df,percent_v):
    TOOLTIPS = [
    ("Resource","@Resource"),
    ("Resource Rarity Rank", "@{Rarity Ranking (Lowest is Rarest)}"),
    ("Total Price to Control "+str(percent_v)+"%", "@{Total Price to Control "+str(percent_v)+"% in ETH}{0.00}ETH"),
    ("Number of Plots Needed for "+str(percent_v)+"% Control", "@{Number of Plots Needed for "+str(percent_v)+"% Control}"),
    ("Total Number of Resource on All Plots","@{Total Number of Resource on All Plots}{0,0}")]
    
    source=ColumnDataSource(data=data_df)
    p=figure(tooltips=TOOLTIPS, x_axis_label="Rarity Ranking (Lowest is Rarest)", y_axis_label="Total Price to Control "+str(percent_v)+"% in ETH (Log Scale)", y_axis_type="log")
    doc=curdoc()
    doc.theme = 'dark_minimal'
    doc.add_root(p)
    p.add_layout(Legend(),'right')
    p.legend.title="Resource Type"
    p.legend.title_text_color="white"
    p.legend.background_fill_color = "black"
    p.scatter(x='Rarity Ranking (Lowest is Rarest)', y='Total Price to Control '+str(percent_v)+'% in ETH', source=source, size=8, color=factor_cmap('Type','Category10_4', resource_type), legend_group="Type")
    p.xgrid.visible = False
    p.toolbar_location = None
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None
    p.yaxis.formatter = BasicTickFormatter(use_scientific=False)
    p.yaxis.ticker = [0.5, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50, 75, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    return(placeholder.bokeh_chart(p, use_container_width=True))
#increases font of expanded text
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
#custom column headers for table
column_config={"Resource":"Resource", 
            "Total Price to Control 1% in ETH":"Price for Plots (ETH)",
            "Number of Plots Needed for 1% Control": "# of Plots Needed",
            "Plot IDs for Sale":"Plot IDs",
            "Rarity Ranking (Lowest is Rarest)":"Rarity",
            "Total Number of Resource on All Plots":"Total # On All Plots",
            "Type":"Type"}
col2.write("Resources that 1% cannot be purchased")
with col1:
    placeholder = st.container()
    placeholder2=st.container()
    placeholder3 = st.expander("To see breakdown of the data used for the visualization, click here for a table")
    exclude1 = placeholder2.toggle('Include Very Common Ranked 60-74 Resources',value=False, help="These resources are very plentiful, acquiring 1% would be very expensive. Turning this on makes the scale of the graph much larger.", key="toggle1")
    opensea_flag1=placeholder2.toggle('Exclude Plots That are Flagged by Opensea', value=False,help="NFTs flagged by Opensea marketplace are untradeable on Opensea, and usually trade at a discount on other marketplaces as they might be stolen.",key="opensea1" )   
    #below decides which data to pull and use for the table and graph
    if exclude1 ==False and opensea_flag1==False:
        with placeholder.container():
            data_false_false_tuple=load_data(1,"with","yes")
            data_false_false=data_false_false_tuple[0]
            make_graph(data_false_false,1)
        with placeholder3.container():
            placeholder3.dataframe(data_false_false,column_config=column_config)
        data_false_false_zero=data_false_false_tuple[1]
        col2.dataframe(data_false_false_zero,hide_index=True)

    if exclude1 ==True and opensea_flag1==False:
        with placeholder.container():
            data_true_false_tuple=load_data(1,"with","no")
            data_true_false=data_true_false_tuple[0]
            make_graph(data_true_false,1)
        with placeholder3.container():
            placeholder3.dataframe(data_true_false,column_config=column_config)
        data_true_false_zero=data_true_false_tuple[1]
        col2.dataframe(data_true_false_zero, hide_index=True)

    if exclude1==False and opensea_flag1==True:
            with placeholder.container():
                data_false_true_tuple=load_data(1,"without","yes")
                data_false_true=data_false_true_tuple[0]
                make_graph(data_false_true,1)
            with placeholder3.container():
                placeholder3.dataframe(data_false_true,column_config=column_config)
            data_false_true_zero=data_false_true_tuple[1]
            col2.dataframe(data_false_true_zero, hide_index=True)

    if exclude1==True and opensea_flag1==True:
            with placeholder.container():
                data_true_true_tuple=load_data(1,"without","no")
                data_true_true=data_true_true_tuple[0] 
                make_graph(data_true_true,1)
            with placeholder3.container():
                placeholder3.dataframe(data_true_true,column_config=column_config)
            data_true_true_zero=data_true_true_tuple[1]
            col2.dataframe(data_true_true_zero,hide_index=True)

