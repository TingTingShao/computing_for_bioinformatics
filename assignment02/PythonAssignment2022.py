# These are the only packages you are allowed import:
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd

# "pass" indicates an empty block of code, 
# remove it when filling in the functions.


def my_name():
    # Replace this with your full name.
    return "TingTing Shao"

###'''part1.1'''###
def build_datastructure_lineage_query(lineage_file):
    '''map self number to cell name dictionary'''
    fl=open(lineage_file,'r')
    cellNameMap={}
    for line in fl:
        line = line.split() #remove empty line
        if not line:  
            continue
        cellNameMap[line[6]] = line[0]
    '''remove all nondividing cells'''
    df=pd.read_csv(lineage_file, sep='\t')
    df2=df.drop(df[(df['child2'] == -1)].index)
    '''map 'self', 'child1', 'child2' number to cell names'''
    df2['self']=df2['self'].astype(str).map(cellNameMap)
    df2['child1']=df2['child1'].astype(str).map(cellNameMap)
    df2['child2']=df2['child2'].astype(str).map(cellNameMap)
    '''build child_parent_one_to_one dictionary'''
    child_parent={}
    child1_parent=pd.Series(df2.self.values,index=df2.child1).to_dict()
    child2_parent=pd.Series(df2.self.values,index=df2.child2).to_dict()
    child_parent.update(child1_parent)
    child_parent.update(child2_parent)
    return child_parent
####'''part1.2'''###
def get_parents_for_cell(query_cell, ds_lineage_query):
    if query_cell not in ds_lineage_query.keys():
        return []
    else: 
        parent=ds_lineage_query[query_cell]
        result = [parent]
        ###use recursion to search for parent cells
        new_result=get_parents_for_cell(parent, ds_lineage_query)
        list= result + new_result
        return list

###'''part2'''###
def plot_surf_vol_ratio_over_time(volsurf, file_out=None):
    volsurf_group=volsurf.groupby(
        ['cell'], as_index=False
    ).agg(
        mean_volume=('volume','mean'),
        mean_surface=('surface','mean'),
        mean_time=('t', 'mean')
        )
    volsurf_group['Ratio']=(volsurf_group["mean_surface"]/volsurf_group["mean_volume"])
    sns.lmplot(x='mean_time', y='Ratio',data=volsurf_group).set(title="volumeRatios_over_time")
    plt.tight_layout()
    plt.savefig(file_out)

###'''part3'''###
def get_volume_ratios(volsurf):
    vol=volsurf.groupby(
        ['cell'], as_index=False
        ).agg(
        mean_volume=('volume','mean'),
        )
    '''build a new dataframe'''
    df=pd.DataFrame(columns=['cell_mother','cell_daughter1', 'cell_daughter1_volume', 'cell_daughter2', 'cell_daughter2_volume'], index=range(5000))
    n=len(vol['cell'])
    cell_name=list(vol['cell'])
    for i in range(n):
        mh=vol['cell'].values[i]
        childL=mh+'l'
        childA=mh+'a'
        childR=mh+'r'
        childP=mh+'p'
        df['cell_mother'].values[i]=mh
        if childL in cell_name:
            df['cell_daughter1'].values[i]=childL
            df['cell_daughter1_volume'].values[i]=vol.loc[vol['cell'] == childL, 'mean_volume'].iloc[0]
        if childA in cell_name:
            df['cell_daughter1'].values[i]=childA
            df['cell_daughter1_volume'].values[i]=vol.loc[vol['cell'] == childA, 'mean_volume'].iloc[0]
        if childR in cell_name:
            df['cell_daughter2'].values[i]=childR
            df['cell_daughter2_volume'].values[i]=vol.loc[vol['cell'] == childR, 'mean_volume'].iloc[0]
        if childP in cell_name:
            df['cell_daughter2'].values[i]=childP
            df['cell_daughter2_volume'].values[i]=vol.loc[vol['cell'] == childP, 'mean_volume'].iloc[0]
    df.dropna(inplace=True)
    df['vol_ratio_daughters']=(df['cell_daughter1_volume']/df["cell_daughter2_volume"])
    del df['cell_daughter1_volume'], df['cell_daughter2_volume']
    return df.to_csv(output_folder/'VolumeRatios.csv', sep='\t')


if __name__ == "__main__":
    # set path names : 
    data_folder = Path('./data')
    lineage_file = data_folder / 'lineage_named_Sample04'
    volsurf_file = data_folder / 'volumeAndSurface.csv'
    output_folder = Path('./output')
    output_folder.mkdir(exist_ok=True)

    # Part 1 : Parse volume and surface data
    ds_lineage_query = build_datastructure_lineage_query(lineage_file)
    query_cell = "ABplppap"
    parents = get_parents_for_cell(query_cell, ds_lineage_query)
    print(f"The parents for cell {query_cell} are {parents}")

    # Part 2 : Plot surface / volume ratio per cell
    volsurf = pd.read_csv(volsurf_file)
    plot_surf_vol_ratio_over_time(volsurf, output_folder / 'volumeRatios_over_time.png')

    # Part 3 : get cell divisions with volume ratios
    vol_ratios = get_volume_ratios(volsurf)
    #  ...write to output

