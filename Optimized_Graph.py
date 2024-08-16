import pandas as pd
import networkx as nx
import itertools

class GraphCreator:
    def __init__(self, df):
        self.df = df

    def create_graph(self):
        # Group by URL and find pairs of organizations
        df_edge = self.df.groupby("URL").Organization.apply(lambda x: list(itertools.combinations(x, 2))).explode().dropna().reset_index(drop=True)

        # Create a DataFrame from source-destination pairs and calculate weights
        source_dest = pd.DataFrame(df_edge.tolist(), columns=["Source", "Dest"])
        source_dest["weight"] = source_dest.groupby(["Source", "Dest"])["Source"].transform('size')

        # Create a graph from the source-destination pairs with weights
        self.G = nx.from_pandas_edgelist(source_dest.drop_duplicates(), source="Source", target="Dest", edge_attr="weight", create_using=nx.Graph)
        
        # Get the set of unique organizations
        self.organizations = set(source_dest["Source"]).union(source_dest["Dest"])
        
        return self.G
