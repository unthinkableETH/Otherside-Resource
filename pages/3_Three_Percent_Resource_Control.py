import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,Legend
from bokeh.io import curdoc
from bokeh.transform import factor_cmap


st.set_page_config(
    page_title="3% Resource Control", layout="wide"
)

st.sidebar.success("Select Percentage of Resource Control Above")

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)
st.write("# 3% Resource Control")


resource_type=["Ore","Anima","Root","Shard"]
@st.cache_data(experimental_allow_widgets=True) 
def load_data(percent,with_or_without_flag,exclude_yes_or_no):
    data=pd.DataFrame()
    data_zero=pd.DataFrame()
    url="https://raw.githubusercontent.com/unthinkableETH/Otherside-Resource/main/"+str(percent)+'%25TotalPrice_'+str(with_or_without_flag)+'_flag.csv'
    data=pd.read_csv(url, index_col=0)
    url_zero="https://raw.githubusercontent.com/unthinkableETH/Otherside-Resource/main/"+str(percent)+'%25TotalPrice_'+str(with_or_without_flag)+'_flag_zero.csv'
    data_zero=pd.read_csv(url_zero,index_col=0)
    data_zero_exclude=data_zero.loc[data_zero['Rarity'] <=59]
    data_with_exclude=data.loc[data['Rarity Ranking (Lowest is Rarest)'] <=59]
    if exclude_yes_or_no =='yes':
        return(data_with_exclude,data_zero_exclude)
    if exclude_yes_or_no == 'no':
         return(data,data_zero)
     
def make_graph(data_df,percent_v):
    TOOLTIPS = [
    ("Resource","@Resource"),
    ("Resource Rarity Rank", "@{Rarity Ranking (Lowest is Rarest)}"),
    ("Total Price to Control "+str(percent_v)+"%", "@{Total Price to Control "+str(percent_v)+"% in ETH}{0.00}ETH"),
    ("Number of Plots Needed for "+str(percent_v)+"% Control", "@{Number of Plots Needed for "+str(percent_v)+"% Control}"),
    ("Total Number of Resource on All Plots","@{Total Number of Resource on All Plots}{0,0}")]
    
    source=ColumnDataSource(data=data_df)
    p=figure(tooltips=TOOLTIPS, x_axis_label="Rarity Ranking (Lowest is Rarest)", y_axis_label="Total Price to Control "+str(percent_v)+"% in ETH")
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
    return(placeholder.bokeh_chart(p, use_container_width=True))

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("/home/shaun/DAPython/Otherside/Final/style.css")


col1, col2 = st.columns([4, 1])
column_config={"Resource":"Resource",
            "Total Price to Control 3% in ETH":"Price for Plots (ETH)",
            "Number of Plots Needed for 3% Control": "# of Plots Needed",
            "Plot IDs for Sale":"Plot IDs",
            "Rarity Ranking (Lowest is Rarest)":"Rarity",
            "Total Number of Resource on All Plots":"Total # On All Plots",
            "Type":"Type"}
col2.write("Resources that 3% can not be purchased")
with col1:
    placeholder = st.container()
    placeholder2=st.container()
    placeholder3 = st.expander("To see breakdown of the data used for the visualization, click here for a table")
    exclude3 = placeholder2.toggle('Include Very Common Ranked 60-74 Resources',value=False, help="These resources are very plentiful, acquiring 3% would be very expensive. Turning this on makes the scale of the graph much larger.", key="toggle3")
    opensea_flag3=placeholder2.toggle('Exclude Plots That are Flagged by Opensea', value=False,help="NFTs flagged by Opensea marketplace are untradeable on Opensea, and usually trade at a discount on other marketplaces as they might be stolen.",key="opensea3" )   
    if exclude3 ==False and opensea_flag3==False:
        with placeholder.container():
            data_false_false_tuple=load_data(3,"with","yes")
            data_false_false=data_false_false_tuple[0]
            make_graph(data_false_false,3)
        with placeholder3.container():
            placeholder3.dataframe(data_false_false,column_config=column_config)
        data_false_false_zero=data_false_false_tuple[1]
        col2.dataframe(data_false_false_zero,hide_index=True)

    if exclude3 ==True and opensea_flag3==False:
        with placeholder.container():
            data_true_false_tuple=load_data(3,"with","no")
            data_true_false=data_true_false_tuple[0]
            make_graph(data_true_false,3)
        with placeholder3.container():
            placeholder3.dataframe(data_true_false,column_config=column_config)
        data_true_false_zero=data_true_false_tuple[1]
        col2.dataframe(data_true_false_zero, hide_index=True)

    if exclude3==False and opensea_flag3==True:
            with placeholder.container():
                data_false_true_tuple=load_data(3,"without","yes")
                data_false_true=data_false_true_tuple[0]
                make_graph(data_false_true,3)
            with placeholder3.container():
                placeholder3.dataframe(data_false_true,column_config=column_config)
            data_false_true_zero=data_false_true_tuple[1]
            col2.dataframe(data_false_true_zero, hide_index=True)

    if exclude3==True and opensea_flag3==True:
            with placeholder.container():
                data_true_true_tuple=load_data(3,"without","no")
                data_true_true=data_true_true_tuple[0] 
                make_graph(data_true_true,3)
            with placeholder3.container():
                placeholder3.dataframe(data_true_true,column_config=column_config)
            data_true_true_zero=data_true_true_tuple[1]
            col2.dataframe(data_true_true_zero,hide_index=True)
