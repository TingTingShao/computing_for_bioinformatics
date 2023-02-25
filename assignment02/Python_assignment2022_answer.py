# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def my_name():
    # Replace this with your full name.
    return "Jane Doe"
    

def build_datastructure_lineage_query(lineage_file):
    """ Given a lineage file, build a datastructure that allows to retrieve the parents of a given cell

    Parameters:
        lineage_file (str or Path) : the input lineage file
    Returns:
        Dict: map of a cell name to the name of its parent
    """
    d_self_cell = {}
    d_cell_selfParent = {}
    file = open(lineage_file, 'r')
    for ix_line, line in enumerate(file.readlines()):
        fields = line.split(sep='\t')
        if ix_line == 0:
            IX_CELL, IX_SELF, IX_PARENT = fields.index(
                'cell'), fields.index('self'), fields.index('parent')
        else:
            d_self_cell[fields[IX_SELF]] = fields[IX_CELL]
            if fields[IX_CELL] not in d_cell_selfParent:
                d_cell_selfParent[fields[IX_CELL]] = fields[IX_PARENT]

    # translate cell-indices into names
    d_cell_parent = {
        cell: d_self_cell[parentSelf] for cell,
        parentSelf in d_cell_selfParent.items() if parentSelf != '-1'}

    return d_cell_parent


def get_parents_for_cell(query_cell, ds_parents_query):
    """ Given a cell, return a list of its parent cells

    Parameters:
        query cell (str) name of a cell
    Returns:
        List : parents of the the given cell, sorted, so as to go back in time
    """
    parents = []
    parent = ds_parents_query.get(query_cell)

    if not parent:
        print(f"{query_cell} is not a valid input cell !")
        return None

    while parent:
        parents.append(parent)
        parent = ds_parents_query.get(parent)
    return parents


def get_volume_ratios(volsurf):
    """ Calculate average volume ratios of sisters cells

    Parameters:
        volsurf (dataframe) : volume data of all cells over all samples
    Returns:
        Dataframe: average volume ratios of sisters cells
    """
    volsurf['cell_mother'] = volsurf.cell.str.extract('(.*)[a,p,l,r]')
    cond_al = volsurf.cell.str.endswith(('a', 'l'))
    cond_pr = volsurf.cell.str.endswith(('p', 'r'))
    sister_vol_ratio = pd.merge(
        volsurf[cond_al], volsurf[cond_pr], how='inner', on=[
            'sample', 't', 'cell_mother'], suffixes=(
            '_daughter1', '_daughter2'))
    sister_vol_ratio['vol_ratio_daughters'] = sister_vol_ratio.volume_daughter1 / \
        sister_vol_ratio.volume_daughter2

    key = ['cell_mother', 'cell_daughter1', 'cell_daughter2']
    # first, aggregate within each sample
    sister_vol_ratio = sister_vol_ratio.groupby(by=['sample'] + key).mean()
    # second, aggregate across samples
    sister_vol_ratio = sister_vol_ratio.reset_index().groupby(by=key).mean()

    sister_vol_ratio = sister_vol_ratio.reset_index()[
        key + ['vol_ratio_daughters']]
    return sister_vol_ratio


def plot_surf_vol_ratio_over_time(volsurf, file_out=None):
    """ Plot mean surface area to volume ratio for all cells wrt time

    Parameters:
        volsurf (dataframe) : volume data of all cells over all samples
        file_out (str or Path) : save location
    """
    volsurf['surf_vol_ratio'] = volsurf.surface / volsurf.volume
    df_ratios = volsurf.groupby(by=['cell']).mean()

    sns.lmplot(x='t', y='surf_vol_ratio', data=df_ratios, markers='.')

    if file_out:
        plt.savefig(
            file_out,
            transparent=False,
            dpi=350,
            facecolor='white',
            edgecolor='none')


if __name__ == "__main__":
    # set path names
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
    plot_surf_vol_ratio_over_time(
        volsurf,
        (output_folder / 'volumeRatios_over_time.png'))

    # Part 3 : get cell divisions with volume ratios
    vol_ratios = get_volume_ratios(volsurf)
    vol_ratios.to_csv(output_folder / 'volumeRatios.csv', index=False)
