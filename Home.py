import streamlit as st

st.set_page_config(
    page_title="Home", layout="wide"
)

st.write("# A look at Otherside Resource Price Manipulation Risks")

st.sidebar.success("Select Percentage of Resource Control Above")

st.markdown(
    """
    ### What is the Otherside? From Yuga Labs
    - Otherside is a gamified, interoperable metaverse currently under development. The game blends mechanics from massively multiplayer online role playing games (MMORPGs) and web3-enabled virtual worlds. 
    Think of it as a metaRPG where the players own the world, your NFTs can become playable characters, and thousands can play together in real time. 

    - The Otherside is currently represented as 100,000 NFTs/plots of land with four resource slots (North,East,West,South) each for which can be filled with one of 74 different in-game resources. For a more
    in-depth look into Otherside Resources overall I highly recommend the Otherside Wiki which can be found [here](https://www.otherside-wiki.xyz/otherdeed/resource).
    ### Why did I create this dashboard?
    - Growing up I played MMORPGs like Runescape and World of Warcraft which frequently face price manipulation in their in-game economies. The difference between these MMORPGs and the Otherside is
    that with NFTs/blockchain players will now digitally own these in-game resources possibly limiting the options Yuga Labs will have to change or fix in-game economies vs their centalized counterparts. 
    
    - Blockchain has also shown to enable ease of
    coordination of funds through DAOs(Decentralized Autonomous Organizations), the best example of this was when a DAO raised $47 million USD to try to buy a copy of the US Constitution which you can read about
    [here](https://www.theverge.com/22820563/constitution-meme-47-million-crypto-crowdfunding-blockchain-ethereum-constitution). DAOs will likely upgrade the current model of alliances in MMORPGs which currently have 
    "guilds" and "clans" which allow for coordination in-game by those that frequently play together by tying coordination back to real life money instead of mainly in-game achievements.

    - To read more about in-game economies I recommend [this](https://www.gamedeveloper.com/production/mmo-economy-manipulation-#close-modal) article by Sam Sherwood titled "MMO Economy Manipulation." and [this](https://gameanalytics.com/blog/economic-research-mmorpgs-quick-overview/) article by Anders Drachen titled "Economic Research On MMORPGS: A Quick Overview".
   
    ### Basic assumptions and general guide to the dashboards
    - There is currently three dashboard pages available showing the price to aquire 1% or 2% or 3% of all of a certain resource from purchasing mulitple NFT plots with those resources.
    - Each dashboard also shows what resources are not available to be purchased to meet a certain percentage and a table within an expander of plot IDs used for the data visualization.
    - Data for what NFTs are for sale and their lowest price is updated hourly from [Reservoir.tools](Reservoir.tools) from an aggregate of NFT marketplaces.
    - NFTs that are considered outliers by high prices are not included in the data set. The method to determine which NFTs were outliers was a IQR Upper Bound/(Q3 + 1.5 * IQR) more about this statistical method can be found [here](https://towardsdatascience.com/why-1-5-in-iqr-method-of-outlier-detection-5d07fdc82097).
    - Otherside plot NFTs have resource tier levels 1 or 2 or 3 for each resource slot, but there currently is no information on how these will compare with each other or if they will be upgradeable, so currently all tier levels
    are treated the same. In the future this could be adjusted if more guidance is given.

"""
)