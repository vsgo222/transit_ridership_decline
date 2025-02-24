# import packages for the file usage
import pandas as pd
import matplotlib.pyplot as plt
import pathlib
import os.path
import numpy as np
import os


def filter_dataframe(_df, _startyear, _endyear):
    df = _df
    startyear = _startyear
    end_year = _endyear
    df_fitered = df[(df.Year >= startyear) & (df.Year <= end_year)]
    # df_queried = df.where(("Year">=str(startyear)) & ("Year"<=str(end_year)))
    return df_fitered


# make the charts
def prepare_charts(_df_org, _clustername, _filename, _startyear, _endyear):
    df_org = _df_org
    clustercolumn = _clustername
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    modes = df_org['Mode'].unique()
    modes.sort()
    figcounter = 1
    clusternumber = 1
    for cluster in clusters:
        df_fltr = df_org[df_org[clustercolumn] == cluster]
        # Print the cluster
        col_index = df_fltr.columns.get_loc(clustercolumn)
        cluster_code = str(df_fltr.iloc[0, col_index])
        print('Cluster Code:' + str(cluster_code))
        df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
        df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        # # create a color palette
        # palette = plt.get_cmap('Set1')
        # # # multiple line plot
        # # num = 0
        x = 1
        for mode in modes:
            chartcols = ['UPT_ADJ_VRM_ADJ_log_FAC_cumsum',
                         'UPT_ADJ_FARE_per_UPT_2018_log_FAC_cumsum',
                         'UPT_ADJ_POP_EMP_log_FAC_cumsum',
                         'UPT_ADJ_TSD_POP_PCT_FAC_cumsum',
                         'UPT_ADJ_GAS_PRICE_2018_log_FAC_cumsum',
                         'UPT_ADJ_TOTAL_MED_INC_INDIV_2018_log_FAC_cumsum',
                         # 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum',
                         'UPT_ADJ_PCT_HH_NO_VEH_FAC_cumsum',
                         'UPT_ADJ_JTW_HOME_PCT_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum',
                         'UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum',
                         'UPT_ADJ_BIKE_SHARE_FAC_cumsum',
                         'UPT_ADJ_scooter_flag_FAC_cumsum',
                         'UPT_ADJ_Unknown_FAC_cumsum']
            subplot_labels = ['Vehicle Revenue Miles',
                              'Average Fares (2018$)',
                              'Population + Employment',
                              '% of Population in Transit Supportive Density',
                              'Average Gas Price (2018$)',
                              'Median Per Capita Income (2018$)',
                              # 'Immigrant population',
                              '% of Households with 0 Vehicles',
                              '% Working at Home',
                              'Years Since Ride-hail Start on Bus for High Inc/NY',
                              'Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters',
                              'Years Since Ride-hail Start on Rail for High Inc/NY',
                              'Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters',
                              'Bike Share',
                              'Electric Scooters',
                              'Unmeasurable variables']
            fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(23, 16), constrained_layout=False)
            if ((cluster == 1) or (cluster == 10)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')

            if ((cluster == 1) or (cluster == 10)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')

            if ((cluster == 2) or (cluster == 3)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Rail for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
                subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')

            if ((cluster == 2) or (cluster == 3)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_MIDLOW_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_RAIL2_HINY_FAC_cumsum')
                chartcols.remove('UPT_ADJ_YEARS_SINCE_TNC_BUS2_HINY_FAC_cumsum')

                subplot_labels.remove('Years Since Ride-hail Start on Bus for Mid&Low Inc Clusters')
                subplot_labels.remove('Years Since Ride-hail Start on Rail for High Inc/NY')
                subplot_labels.remove('Years Since Ride-hail Start on Bus for High Inc/NY')

            df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
            col = 0
            row = 0
            transparency = 0.3
            num = 0
            for chartcol, subplotlable in zip(chartcols, subplot_labels):
                df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                  label='Hypothesized Ridership if no changes in ' +
                                                        str(subplotlable[:27]), ax=ax[row][col], legend=True,
                                                  fontsize=12)
                df_fltr_mode.groupby('Mode').plot(x='Year', y='UPT_ADJ', label='Observed Ridership', ax=ax[row][col],
                                                  legend=True, color='black', linewidth=2.4, fontsize=12)
                ax[row][col].set_xlabel(xlabel="Year", fontsize=14)
                ax[row][col].tick_params(labelsize=14)
                # Paint the area
                ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
                                          df_fltr_mode['UPT_ADJ'].values,
                                          where=df_fltr_mode['UPT_ADJ'].values > df_fltr_mode[chartcol].values,
                                          facecolor='green', interpolate=True, alpha=transparency)
                ax[row][col].fill_between(df_fltr_mode['Year'].values, df_fltr_mode[chartcol].values,
                                          df_fltr_mode['UPT_ADJ'].values,
                                          where=df_fltr_mode['UPT_ADJ'].values <= df_fltr_mode[chartcol].values,
                                          facecolor='red', interpolate=True, alpha=transparency)
                # ax[row][col].set(xlabel="Years", ylabel='Ridership')
                ax[row][col].legend(loc='best', fontsize=12)
                if "Ride-hail" not in subplotlable:
                    ax[row][col].set_title(str(subplotlable), fontsize=15)
                else:
                    ax[row][col].set_title(str(subplotlable[:28]), fontsize=15)
                ax[row][col].set_autoscaley_on(False)
                try:
                    ax[row][col].grid(True)
                    ax[row][col].margins(0.20)
                    min_val = min(df_fltr_mode[['UPT_ADJ', chartcol]].values.min(1))
                    max_val = max(df_fltr_mode[['UPT_ADJ', chartcol]].values.max(1))
                    ax[row][col].set_ylim([min_val * 0.5, max_val * 1.25])
                except ValueError:
                    pass
                if row >= 3:
                    row = 0
                    col += 1
                else:
                    row += 1

            for z in fig.get_axes():
                z.label_outer()

            fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
            _figno = x
            # get the abs path of the directory of the code/script
            # Factors and Ridership Data\ code
            current_dir = pathlib.Path(__file__).parent.absolute()
            # Change the directory
            # \Script Outputs
            # change the directory to where the file would be saved
            current_dir = current_dir.parents[0] / 'Script Outputs'
            os.chdir(str(current_dir))
            print("Current set directory: ", current_dir)
            outputdirectory = "Est7_Outputs"
            p = pathlib.Path(outputdirectory)
            p.mkdir(parents=True, exist_ok=True)
            current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
            os.chdir(str(current_dir))
            # Axis title
            fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
            figlabel = "Ridership"
            # if max(df_fltr['UPT_ADJ']) / 10 ** 9 > 0.0:
            #     figlabel = 'Ridership (in 100 million)'
            # else:
            #     figlabel = 'Ridership (in 10 million)'

            fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
                     fontsize=18)
            figname = ("Est7 - " + str(_startyear) + "-" + str(_endyear) + " Cluster " + str(
                cluster) + "-" + mode_name + ".png")
            figcounter += 1
            figlabel = ""

            fig.savefig(figname)

            plt.suptitle(clustercolumn, fontsize=18)

            plt.close(fig)
            x += 1
            clusternumber += 1
        print("Success")


def create_upt_fac_cluster_file(_filename, _clustervalue, _startyear, _endyear):
    # get the abs path of the directory of the code/script
    # Factors and Ridership Data\ code
    current_dir = pathlib.Path(__file__).parent.absolute()
    folder_name = chart_name = _filename.split('.')[0]
    # Change the directory
    # \Script Outputs \ Cluster_wise_summation_files
    current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
    os.chdir(str(current_dir))
    df = pd.read_csv(_filename)
    startyear = _startyear
    endyear = _endyear
    df_org = filter_dataframe(df, startyear, endyear)
    # create cumulative column and update the column
    # create new columns
    col_name = ['VRM_ADJ_log_FAC',
                'FARE_per_UPT_2018_log_FAC',
                'POP_EMP_log_FAC',
                'TSD_POP_PCT_FAC',
                'GAS_PRICE_2018_log_FAC',
                'TOTAL_MED_INC_INDIV_2018_log_FAC',
                # 'Tot_NonUSA_POP_pct_FAC',
                'PCT_HH_NO_VEH_FAC',
                'JTW_HOME_PCT_FAC',
                'YEARS_SINCE_TNC_BUS2_HINY_FAC',
                'YEARS_SINCE_TNC_BUS2_MIDLOW_FAC',
                'YEARS_SINCE_TNC_RAIL2_HINY_FAC',
                'YEARS_SINCE_TNC_RAIL2_MIDLOW_FAC',
                'BIKE_SHARE_FAC',
                'scooter_flag_FAC',
                'Unknown_FAC']
    cum_col = []
    col_UPT_ADJ = ['UPT_ADJ']
    # check for table records, wherever data is missing replace it with "0"
    for col in col_name:
        df[col] = np.where(df[col] == '-', 0, df[col])
        try:
            df[col] = df[col]
        except ValueError:
            pass

    for col in col_name:
        df_org[str(col) + '_cumsum'] = df_org[col]
        cum_col.append(str(col) + '_cumsum')

    cluster_values = _clustervalue

    # # for each cluster_id get the cumulative addition starting from 2002-->2018
    # os.chdir(output_folder)
    for col in cum_col:
        df_org[col] = df_org.groupby([cluster_values, 'RAIL_FLAG'])[col].cumsum()

    # # create a new column which is diff between UPT_ADJ - CUMSUM colmn
    for col in cum_col:
        df_org['UPT_ADJ_' + str(col)] = df_org['UPT_ADJ'] - df_org[col]

        # save the cumulative file as UPT_filename.csv
    df_org.to_csv("UPT_" + folder_name + "_b" + str(startyear) + '.csv')
    print("Successfully created " + "UPT_" + folder_name + "_b" + str(startyear) + '.csv')
    # df_queried = prepare_charts_timeframe(df_org, startyear, endyear)
    prepare_charts(df_org, cluster_values, _filename, startyear, endyear)


def get_cluster_chart_raw(_df, _filename, _chart_name, _clusterfile):
    df_org = _df
    filename = _filename
    chart_name = _chart_name
    clustercolumn = _clusterfile
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    modes = df_org['Mode'].unique()
    modes.sort()
    mode_name = ""
    figcounter = 1
    clusternumber = 1
    for cluster in clusters:
        df_fltr = df_org[df_org[clustercolumn] == cluster]
        # Print the cluster
        col_index = df_fltr.columns.get_loc(clustercolumn)
        cluster_code = str(df_fltr.iloc[0, col_index])
        print('Cluster Code:' + str(cluster_code))
        df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
        df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
        # Initialize the figure
        plt.style.use('seaborn-darkgrid')
        x = 1
        fig, ax = plt.subplots(nrows=4, ncols=3, figsize=(22, 15), constrained_layout=False)
        for mode in modes:
            if mode == 0:
                dcolor = "blue"
            else:
                dcolor = "red"
            chartcols = ['VRM_ADJ',
                         'FARE_per_UPT_2018',
                         'POP_EMP',
                         'TSD_POP_PCT',
                         'GAS_PRICE_2018',
                         'TOTAL_MED_INC_INDIV_2018',
                         # 'UPT_ADJ_Tot_NonUSA_POP_pct_FAC_cumsum',
                         'PCT_HH_NO_VEH',
                         'JTW_HOME_PCT',
                         'YEARS_SINCE_TNC_BUS2_HINY',
                         'YEARS_SINCE_TNC_BUS2_MIDLOW',
                         'YEARS_SINCE_TNC_RAIL2_HINY',
                         'YEARS_SINCE_TNC_RAIL2_MIDLOW',
                         'BIKE_SHARE',
                         'scooter_flag',
                         'UPT_ADJ']
            subplot_labels = ['Vehicle Revenue Miles',
                              'Average Fares (2018$)',
                              'Population + Employment',
                              '% of Population in Transit Supportive Density',
                              'Average Gas Price (2018$)',
                              'Median Per Capita Income (2018$)',
                              # 'Immigrant population',
                              '% of Households with 0 Vehicles',
                              '% Working at home',
                              'Years Since Ride-hail Start Bus HINY',
                              'Years Since Ride-hail Start Bus MIDLOW',
                              'Years Since Ride-hail Start Rail HINY',
                              'Years Since Ride-hail Start Rail MIDLOW',
                              'Bike Share',
                              'Electric Scooters',
                              'Ridership']

            remove_list = ['POP_EMP', 'GAS_PRICE_2018', 'TSD_POP_PCT', 'TOTAL_MED_INC_INDIV_2018', 'PCT_HH_NO_VEH',
                           'JTW_HOME_PCT', 'BIKE_SHARE', 'scooter_flag']

            if ((cluster == 1) or (cluster == 10)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                remove_list.append('YEARS_SINCE_TNC_BUS2_HINY')

                subplot_labels.remove('Years Since Ride-hail Start Bus MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Rail MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Rail HINY')

            if ((cluster == 1) or (cluster == 10)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_BUS2_HINY')

                subplot_labels.remove('Years Since Ride-hail Start Bus HINY')
                subplot_labels.remove('Years Since Ride-hail Start Bus MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Rail MIDLOW')

            if ((cluster == 2) or (cluster == 3)) and (mode == 0):
                mode_name = "BUS"
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                chartcols.remove('YEARS_SINCE_TNC_BUS2_HINY')
                remove_list.append('YEARS_SINCE_TNC_BUS2_MIDLOW')

                subplot_labels.remove('Years Since Ride-hail Start Rail MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Bus HINY')
                subplot_labels.remove('Years Since Ride-hail Start Rail HINY')

            if ((cluster == 2) or (cluster == 3)) and (mode == 1):
                mode_name = "RAIL"
                chartcols.remove('YEARS_SINCE_TNC_BUS2_MIDLOW')
                chartcols.remove('YEARS_SINCE_TNC_RAIL2_HINY')
                chartcols.remove('YEARS_SINCE_TNC_BUS2_HINY')

                subplot_labels.remove('Years Since Ride-hail Start Bus MIDLOW')
                subplot_labels.remove('Years Since Ride-hail Start Bus HINY')
                subplot_labels.remove('Years Since Ride-hail Start Rail HINY')

            df_fltr_mode = df_fltr_mod[df_fltr_mod.Mode == mode]
            col = 0
            row = 0
            num = 0

            # if ((cluster == 2) or (cluster == 3) or (cluster == 10)) and (mode == 0):
            for chartcol, subplotlable in zip(chartcols, subplot_labels):
                if cluster == 3:
                    if mode != 1:
                        if chartcol == 'TOTAL_MED_INC_INDIV_2018':
                            labeltext = (str(subplotlable[0:32]))
                        else:
                            labeltext = (str(subplotlable[0:27]))
                        df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                          label=(labeltext),
                                                          ax=ax[row][col], legend=True, fontsize=13,
                                                          linewidth=2.5, color=dcolor)
                        ax[row][col].set_xlabel(xlabel="Year", fontsize=15.5)
                        # ax[row][col].set_ylabel(ylabel=str(subplotlable), fontsize=15.5)
                        ax[row][col].tick_params(labelsize=15.5)
                        ax[row][col].legend(loc='best')
                        if "Ride-hail" not in subplotlable:
                            ax[row][col].set_title(str(subplotlable), fontsize=15.5)
                        else:
                            ax[row][col].set_title(str(subplotlable[:23]), fontsize=15.5)
                        ax[row][col].set_autoscaley_on(True)
                        try:
                            ax[row][col].grid(True)
                            ax[row][col].margins(0.20)
                            # ax[row][col].set_ylim(0, (df_fltr_mode[chartcols].max()) * 1.25)
                        except ValueError:
                            pass
                else:
                    if mode == 0 and (chartcol in remove_list):
                        pass
                    else:
                        if mode == 1 and (chartcol in remove_list):
                            if chartcol == 'TOTAL_MED_INC_INDIV_2018':
                                labeltext = (str(subplotlable[0:32]))
                            if chartcol == "PCT_HH_NO_VEH":
                                labeltext = (str(subplotlable[:31]))
                            else:
                                labeltext = (str(subplotlable[0:27]))
                        else:
                            if "Ride-hail" in subplotlable:
                                labeltext = (str(subplotlable[:27]))
                            else:
                                labeltext = (str(subplotlable[:31]) + ' - ' + mode_name)

                        df_fltr_mode.groupby('Mode').plot(x='Year', y=str(chartcol),
                                                          label=(labeltext),
                                                          ax=ax[row][col], legend=True, fontsize=11,
                                                          linewidth=2.4, color=dcolor)
                        ax[row][col].set_xlabel(xlabel="Year", fontsize=15.5)
                        ax[row][col].tick_params(labelsize=15.5)
                        ax[row][col].legend(loc='best')
                        if "Ride-hail" not in subplotlable:
                            ax[row][col].set_title(str(subplotlable), fontsize=15.5)
                        else:
                            ax[row][col].set_title(str(subplotlable[:27]), fontsize=15.5)
                        ax[row][col].set_autoscaley_on(True)
                        try:
                            ax[row][col].grid(True)
                            ax[row][col].margins(0.20)
                            # ax[row][col].set_ylim(0, (df_fltr_mode[chartcols].max()) * 1.25)
                        except ValueError:
                            pass
                if row >= 3:
                    row = 0
                    col += 1
                else:
                    row += 1

        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""
        fig.text(0.02, 0.5, figlabel, ha='center', va='baseline', rotation='vertical',
                 fontsize=16)
        figname = ("Est7 - (absolute)" + " Cluster " + str(cluster) + ".png")
        figcounter += 1
        figlabel = ""
        fig.savefig(figname)
        plt.suptitle(clustercolumn, fontsize=18)
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)


def get_cluster_file_raw(_filename, _clusterfile):
    filename = _filename
    clusterfile = _clusterfile
    try:
        chart_name = filename.split('.')[0]
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                get_cluster_chart_raw(df, filename, chart_name, clusterfile)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def get_clusterwise_UPTs(_df, _filename, _chart_name, _clusterfile, pct_change_value):
    try:
        df_org = _df
        filename = _filename
        chart_name = _chart_name
        clustercolumn = _clusterfile
        clusters = df_org[clustercolumn].unique()
        clusters.sort()
        df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
        modes = df_org['Mode'].unique()
        modes.sort()
        if "2002" in pct_change_value:
            b = 'b2002'
        if "2012" in pct_change_value:
            b = 'b2012'
        figcounter = 1
        clusternumber = 1
        x = 1
        col = 0
        row = 0
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 18), constrained_layout=False, squeeze=False)
        for mode in modes:
            df_fltr_mode = df_org[df_org.Mode == mode]
            mode_name = ""
            if mode == 0:
                mode_name = "BUS"
            else:
                mode_name = "RAIL"

            for cluster in clusters:
                if (mode == 1) and (cluster == 3):
                    pass
                else:
                    df_fltr = df_fltr_mode[df_fltr_mode[clustercolumn] == cluster]
                    col_index = df_fltr.columns.get_loc(clustercolumn)
                    cluster_code = str(df_fltr.iloc[0, col_index])
                    df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
                    # df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
                    chartcols = ['UPT_PCT_CHNGE']
                    if cluster == 1:
                        subplot_labels = ['High Op-Ex Group']
                        dcolor = "black"
                    elif cluster == 2:
                        subplot_labels = ['Mid Op-Ex Group']
                        dcolor = "green"
                    elif cluster == 3:
                        subplot_labels = ['Low Op-Ex Group']
                        dcolor = "blue"
                    else:
                        subplot_labels = ['New York']
                        dcolor = "red"

                    for chartcol, subplotlable in zip(chartcols, subplot_labels):
                        df_fltr.groupby('CLUSTER_APTA4').plot(x='Year', y=str(chartcol),
                                                              label=(str(subplotlable)), ax=ax[row][col],
                                                              legend=True, linewidth=3, color=dcolor)
                        ax[row][col].set_xlabel(xlabel="Year", fontsize=17)
                        ax[row][col].tick_params(labelsize=16)
                        ax[row][col].legend(loc='best', fontsize=18)
                        ax[row][col].set_title(str(mode_name), fontsize=20)
                        ax[row][col].set_autoscaley_on(True)
                        try:
                            ax[row][col].grid(True)
                            ax[row][col].margins(0.20)
                        except ValueError:
                            pass
            if row >= 1:
                row = 0
                col += 1
            else:
                row += 1

        for z in fig.get_axes():
            z.label_outer()

        fig.tight_layout(rect=[0.03, 0.02, 1, 1])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize='large')
        figlabel = ""
        fig.text(0.02, 0.4, ("Percent Change in Ridership from " + str(b)), ha='center', va='baseline',
                 rotation='vertical', fontsize=20)
        figname = ("Est7 - Percent Change in Ridership from " + b + ".png")
        figcounter += 1
        figlabel = ""
        fig.savefig(figname)
        plt.suptitle(("Percent Change in Ridership from " + str(b)), fontsize='large')
        plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98, wspace=0, hspace=0)
        plt.tight_layout()
        # plt.style.use('seaborn')
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)
    except SystemError:
        print("Functional error, in get_clusterwise_UPTs_function")


def get_clusterwise_only_UPTs(_filename, _clusterfile):
    filename = _filename
    clusterfile = _clusterfile
    try:
        chart_name = filename.split('.')[0]
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                get_clusterwise_UPTs(df, filename, chart_name, clusterfile)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def pct_change_2002(df):
    df['UPT_PCT_CHNGE'] = 100 * (1 - df.iloc[0].UPT_ADJ / df.UPT_ADJ)
    return df


def pct_change_2012(df):
    df['UPT_PCT_CHNGE'] = 100 * (1 - df.iloc[10].UPT_ADJ / df.UPT_ADJ)
    return df


def get_pct_change_clusterwise(_df, _chart_name, _clusterfile, _filename, _pct_change_value):
    df_org = _df
    chart_name = _chart_name
    clustercolumn = _clusterfile
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
    modes = df_org['Mode'].unique()
    modes.sort()
    if '2002' in _pct_change_value:
        df_org = df_org.groupby([chart_name, 'Mode']).apply(pct_change_2002)
    else:
        df_org = df_org.groupby([chart_name, 'Mode']).apply(pct_change_2012)
    get_clusterwise_UPTs(df_org, _filename, chart_name, clustercolumn, _pct_change_value)


def get_clusterwise_UPTs(_df, _filename, _chart_name, _clusterfile, pct_change_value):
    try:
        df_org = _df
        filename = _filename
        chart_name = _chart_name
        clustercolumn = _clusterfile
        clusters = df_org[clustercolumn].unique()
        clusters.sort()
        df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)
        modes = df_org['Mode'].unique()
        modes.sort()
        if "2002" in pct_change_value:
            b = 'b2002'
        if "2012" in pct_change_value:
            b = 'b2012'
        figcounter = 1
        clusternumber = 1
        x = 1
        col = 0
        row = 0
        # plt.style.use('seaborn-darkgrid')
        # custom_cycler = (cycler(color=['r', 'g', 'b', 'y']))

        # plt.rc('axes', prop_cycle=custom_cycler)
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 22), constrained_layout=False, squeeze=False)
        for mode in modes:
            df_fltr_mode = df_org[df_org.Mode == mode]
            mode_name = ""
            if mode == 0:
                mode_name = "BUS"
            else:
                mode_name = "RAIL"

            for cluster in clusters:
                if (mode == 1) and (cluster == 3):
                    pass
                else:
                    df_fltr = df_fltr_mode[df_fltr_mode[clustercolumn] == cluster]
                    col_index = df_fltr.columns.get_loc(clustercolumn)
                    cluster_code = str(df_fltr.iloc[0, col_index])
                    df_fltr['Year'] = pd.to_datetime(df_fltr['Year'].astype(str), format='%Y')
                    # df_fltr_mod = df_fltr.set_index(pd.DatetimeIndex(df_fltr['Year']).year)
                    chartcols = ['UPT_PCT_CHNGE']
                    if cluster == 1:
                        subplot_labels = ['High Op-Ex Group']
                    elif cluster == 2:
                        subplot_labels = ['Mid Op-Ex Group']
                    elif cluster == 3:
                        subplot_labels = ['Low Op-Ex Group']
                    else:
                        subplot_labels = ['New York']

                    for chartcol, subplotlable in zip(chartcols, subplot_labels):
                        df_fltr.groupby('CLUSTER_APTA4').plot(x='Year', y=str(chartcol),
                                                              label=(str(subplotlable)), ax=ax[row][col], legend=True, fontsize=12)
                        # ax[row][col].set_prop_cycle(custom_cycler)
                        plt.rc('lines', linewidth=3)
                        plt.rc('xtick', labelsize=16)
                        plt.rc('ytick', labelsize=16)
                        ax[row][col].legend(loc='best', fontsize=14)
                        ax[row][col].set_title(str(mode_name), fontsize=18)
                        ax[row][col].set_autoscaley_on(True)
                        # for tick in ax.xaxis.get_majorticklabels():  # example for xaxis
                        #     tick.set_fontsize(14)
                        # ax[row][col].xlabel(fontsize=12)
                        # ax[row][col].ylabel(fontsize=12)
                        try:
                            ax[row][col].grid(True)
                            ax[row][col].margins(0.20)
                        except ValueError:
                            pass
            if row >= 1:
                row = 0
                col += 1
            else:
                row += 1
        fig.tight_layout(rect=[0.02, 0.0, 1, 1])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""

        fig.text(0.02, 0.5, ("Percent Change in Ridership from " + str(b)), ha='center', va='baseline',
                 rotation='vertical', fontsize=18)
        figname = ("Est7 - Percent Change in Ridership from " + b + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle(("Percent Change in Ridership from " + str(b)), fontsize=18)
        plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98, wspace=0, hspace=0)
        plt.tight_layout()
        plt.style.use('seaborn')
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)
    except SystemError:
        print("Functional error, in get_clusterwise_UPTs_function")


def create_clusterwise_pct(_filename, _clusterfile, _pct_change_value):
    filename = _filename
    chart_name = clusterfile = _clusterfile
    try:
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                pct_change_value = _pct_change_value
                get_pct_change_clusterwise(df, chart_name, clusterfile, filename, pct_change_value)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def get_subclusterwise_charts(_df, _chart_name, _clusterfile, _filename, _subcluster, pct_change_value):
    df_org = _df
    chart_name = _chart_name
    clustercolumn = _clusterfile
    subcluster_field = _subcluster
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    filter_value = pct_change_value
    if "2002" in filter_value:
        b = 'b2002'
    if "2012" in filter_value:
        b = 'b2012'
    modes = df_org['Mode'].unique()
    modes.sort()
    # df_org.rename(columns={'RAIL_FLAG': 'Mode'}, inplace=True)

    # df_org = df_org.groupby([chart_name, 'Mode']).apply(pct_change)

    figcounter = 1
    clusternumber = 1
    x = 1

    plt.style.use('seaborn-darkgrid')
    for mode in modes:
        df_mode = df_org[df_org['Mode'] == mode]
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 18), constrained_layout=False, squeeze=False)
        # plt.rc('lines', linewidth=3)
        col = 0
        row = 0
        if mode == "Bus":
            mode_name = "BUS"
        else:
            mode_name = "RAIL"
        for cluster in clusters:
            df_cluster = df_mode[df_mode[clustercolumn] == cluster]
            if cluster == 1:
                sub_cluster_title = 'High Op-Ex Group'

            elif cluster == 2:
                sub_cluster_title = 'Mid Op-Ex Group'

            elif cluster == 3:
                sub_cluster_title = 'Low Op-Ex Group'

            else:
                sub_cluster_title = 'New York'

            subclusters = df_cluster[subcluster_field].unique()
            subclusters.sort()
            for subcluster in subclusters:
                if subcluster == 1:
                    sub_cluster_label = 'More Favorable External Factors, Stronger Competitiveness'
                    # dcolor = "black"
                elif subcluster == 2:
                    sub_cluster_label = 'More Favorable External Factors, Weaker Competitiveness'
                    # dcolor = "green"
                elif subcluster == 3:
                    sub_cluster_label = 'Less Favorable External Factors, Stronger Competitiveness'
                    # dcolor = "blue"
                elif subcluster == 0:
                    sub_cluster_label = 'New York'
                    # dcolor = "red"

                else:
                    sub_cluster_label = 'Less Favorable External Factors, Weaker Competitiveness'

                df_subcluster = df_cluster[df_cluster[subcluster_field] == subcluster]
                df_subcluster['Year'] = pd.to_datetime(df_subcluster['Year'].astype(str), format='%Y')
                df_subcluster.groupby('APTA4_SUBCLUSTER').plot(x='Year', y=pct_change_value, label=sub_cluster_label,
                                                               ax=ax[row][col], legend=True, linewidth=3)
                ax[row][col].set_xlabel(xlabel="Year", fontsize=18)
                ax[row][col].tick_params(labelsize=18)
                ax[row][col].legend(loc='best', fontsize=18)
                ax[row][col].set_title(str(mode_name), fontsize=22)
                ax[row][col].set_autoscaley_on(True)
                ax[row][col].grid(True)
                ax[row][col].margins(0.20)
            if row >= 1:
                row = 0
                col += 1
            else:
                row += 1
        for z in fig.get_axes():
            z.label_outer()
        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""

        fig.text(0.02, 0.4, ('Percent Change in Ridership from ' + str(b)), ha='center', va='baseline',
                 rotation='vertical', fontsize=20)
        figname = ("Est7 - (across Clusters) Percent Change in Ridership from " + str(b) + " " + mode_name + ".png")
        figcounter += 1
        figlabel = ""

        fig.savefig(figname)

        plt.suptitle("Percent Change in Ridership from 2002", fontsize=20)
        # plt.style.use('seaborn')
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)


def get_subclustercharts_clusterwise(_df, _chart_name, _clusterfile, _filename, _subcluster, pct_change_value):
    df_org = _df
    chart_name = _chart_name
    clustercolumn = _clusterfile
    subcluster_field = _subcluster
    # get unique values
    yrs = df_org['Year'].unique()
    yrs.sort()
    clusters = df_org[clustercolumn].unique()
    clusters.sort()
    filter_value = pct_change_value
    if "2002" in filter_value:
        b = 'b2002'
    if "2012" in filter_value:
        b = 'b2012'
    modes = df_org['Mode'].unique()
    modes.sort()

    figcounter = 1
    clusternumber = 1
    x = 1

    plt.style.use('seaborn-darkgrid')
    for cluster in clusters:
        df_cluster = df_org[df_org[clustercolumn] == cluster]
        if cluster != 3:
            fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 18), constrained_layout=False, squeeze=False)
        else:
            fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 18), constrained_layout=False, squeeze=False)
        col = 0
        row = 0
        if cluster == 1:
            cluster_title = 'High Op-Ex Group'
        if cluster == 2:
            cluster_title = 'Mid Op-Ex Group'
        if cluster == 3:
            cluster_title = 'Low Op-Ex Group'
        if cluster == 10:
            cluster_title = 'New York'
        for mode in modes:
            if mode == "Rail" and cluster == 3:
                pass
            else:
                df_mode = df_cluster[df_cluster['Mode'] == mode]
                if mode == "Bus":
                    mode_name = "BUS"
                else:
                    mode_name = "RAIL"
                subclusters = df_mode[subcluster_field].unique()
                subclusters.sort()
                for subcluster in subclusters:
                    if subcluster == 1:
                        sub_cluster_label = 'More Favorable External Factors, Stronger Competitiveness'
                        dcolor = "black"
                    elif subcluster == 2:
                        sub_cluster_label = 'More Favorable External Factors, Weaker Competitiveness'
                        dcolor = "green"
                    elif subcluster == 3:
                        sub_cluster_label = 'Less Favorable External Factors, Stronger Competitiveness'
                        dcolor = "blue"
                    elif subcluster == 0:
                        sub_cluster_label = 'New York'
                        dcolor = "red"
                    else:
                        sub_cluster_label = 'Less Favorable External Factors, Weaker Competitiveness'
                        dcolor = "red"

                    df_subcluster = df_mode[df_mode[subcluster_field] == subcluster]
                    df_subcluster['Year'] = pd.to_datetime(df_subcluster['Year'].astype(str), format='%Y')
                    # if mode == "Rail" and cluster == 3:
                    #     row = 0
                    #     col = 0
                    # else:
                    df_subcluster.groupby('APTA4_SUBCLUSTER').plot(x='Year', y=pct_change_value,
                                                                   label=sub_cluster_label, ax=ax[row][col],
                                                                   legend=True, linewidth=3, color=dcolor)
                    ax[row][col].set_autoscaley_on(True)
                    if sub_cluster_label == 'New York':
                        ax[row][col].set_autoscaley_on(False)
                        min_val = (df_subcluster[pct_change_value].min())
                        max_val = (df_subcluster[pct_change_value].max())
                        ax[row][col].set_ylim([min_val * 3, max_val * 3])
                    else:
                        pass
                    ax[row][col].set_xlabel(xlabel="Year", fontsize=18)
                    ax[row][col].tick_params(labelsize=18)
                    ax[row][col].legend(loc='best', fontsize=18)
                    ax[row][col].set_title(str(mode_name), fontsize=22)
                    ax[row][col].grid(True)
                    ax[row][col].margins(0.20)
                        # else:
                        #     pass
                if row >= 1:
                    row = 0
                    col += 1
                else:
                    row += 1
            # for z in fig.get_axes():
            #     z.label_outer()

        fig.tight_layout(rect=[0.03, 0.03, 1, 0.95])
        _figno = x
        # get the abs path of the directory of the code/script
        # Factors and Ridership Data\ code
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Change the directory
        # \Script Outputs
        # change the directory to where the file would be saved
        current_dir = current_dir.parents[0] / 'Script Outputs'
        os.chdir(str(current_dir))
        print("Current set directory: ", current_dir)
        outputdirectory = "Est7_Outputs"
        p = pathlib.Path(outputdirectory)
        p.mkdir(parents=True, exist_ok=True)
        current_dir = current_dir.parents[0] / 'Script Outputs' / outputdirectory
        os.chdir(str(current_dir))
        # Axis title
        # fig.text(0.5, 0.02, 'Year', ha='center', va='center', fontsize=16)
        figlabel = ""

        fig.text(0.02, 0.4, 'Percent Change in Ridership from ' + str(b), ha='center', va='baseline',
                 rotation='vertical', fontsize=20)
        figname = ("Est7 - Percent Change in Ridership from " + str(b) + " - " + cluster_title + ".png")
        figcounter += 1
        figlabel = ""
        fig.savefig(figname)
        plt.suptitle("Percent Change in Ridership from " + str(b), fontsize=22)
        # plt.style.use('seaborn')
        plt.close(fig)
        x += 1
        clusternumber += 1
        print("Successfully created " + figname)


def create_subclusterwise_pct(_filename, _clusterfile, _subcluster):
    filename = _filename
    chart_name = clusterfile = _clusterfile
    try:
        # get the absolute path of the script and then check if the csv file exists or not
        current_dir = pathlib.Path(__file__).parent.absolute()
        current_dir = current_dir.parents[0] / 'Model Estimation' / 'Est7'
        os.chdir(str(current_dir))
        try:
            if (current_dir / filename).is_file():
                df = pd.read_csv(filename)
                # mode wise
                pc_change_value = 'PCT_CHANGE_2002'
                get_subclusterwise_charts(df, chart_name, clusterfile, filename, _subcluster, pc_change_value)
                pc_change_value = 'PCT_CHANGE_2012'
                get_subclusterwise_charts(df, chart_name, clusterfile, filename, _subcluster, pc_change_value)
                # #
                # # # # Clusterwise
                pc_change_value = 'PCT_CHANGE_2002'
                get_subclustercharts_clusterwise(df, chart_name, clusterfile, filename, _subcluster, pc_change_value)
                pc_change_value = 'PCT_CHANGE_2012'
                get_subclustercharts_clusterwise(df, chart_name, clusterfile, filename, _subcluster, pc_change_value)
        except FileNotFoundError:
            print("File could not be found. Please check the file is placed in the folder path - Factors and Ridership "
                  "Data\Model Estimation\Est7")
    except FileNotFoundError:
        print("System error, in cluster_level_chart_function")


def main():
    # get the UPT_FAC files created according to the base year
    # base year 2002
    create_upt_fac_cluster_file("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4", 2002, 2018)
    # # # # # # # # # base year 2012
    create_upt_fac_cluster_file("FAC_totals_APTA4_CLUSTERS.csv", "CLUSTER_APTA4", 2012, 2018)
    # # # # # # # # get absolute charts
    get_cluster_file_raw("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4")
    # # #  # get pct change in core cluster
    create_clusterwise_pct("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4", "2002")
    create_clusterwise_pct("UPT_FAC_totals_APTA4_CLUSTERS_b2002.csv", "CLUSTER_APTA4", "2012")
    # create_clusterwise_pct("UPT_FAC_totals_APTA4_CLUSTERS_b2012.csv", "CLUSTER_APTA4", "2012")
    create_subclusterwise_pct("ridership_cluster.csv", "CLUSTER_APTA4", "APTA4_SUBCLUSTER")


if __name__ == "__main__":
    main()
