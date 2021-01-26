import datetime
import json
import logging
import views

from dateutil import relativedelta
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--start_date", default="2020-09")
parser.add_argument("--end_date", default="2023-10")
parser.add_argument("--country", default="All", help="country name")
parser.add_argument("--gdp_pcap", default="0")
parser.add_argument("--infant_mortality", default="0")
parser.add_argument("--liberalDemocracyIndex", default="0")
parser.add_argument("--foodProdIndex", default="0")
args = parser.parse_args()
print(
    "start_date",
    args.start_date,
    "end_date",
    args.end_date,
    "country",
    type(args.country),
    "gdp",
    float(args.gdp_pcap),
    "inf",
    float(args.infant_mortality),
    "lib",
    args.liberalDemocracyIndex,
    "food",
    args.foodProdIndex,
)


# DATASETS is a dictionary of Dataset objects.
from views import DATASETS

# These are the building blocks of the modelling interface
from views import Ensemble, Model, Downsampling, Period

# These are model specifications from the specfiles
from views.specs.models import cm as model_specs_cm, pgm as model_specs_pgm
from views.specs.periods import get_periods, get_periods_by_name

# Utils
# These are the building blocks of the modelling interface
from views import Ensemble, Model, Downsampling, Period

# These are model specifications from the specfiles
from views.specs.models import cm as model_specs_cm, pgm as model_specs_pgm
from views.specs.periods import get_periods, get_periods_by_name

# Utils
# from views.utils import db, io, data as datautils
from views.utils.data import assign_into_df
from views.apps.pipeline.models_cm import all_cm_models_by_name
from views.apps.pipeline.models_pgm import all_pgm_models_by_name
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# logging errors

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO, # uncomment this and comment debug above for less yelling in red
    format=views.config.LOGFMT,
)

# covert times
date1 = datetime.datetime.strptime(str("1980-01"), "%Y-%m")
start_str = datetime.datetime.strptime(str(args.start_date), "%Y-%m")
end_str = datetime.datetime.strptime(str(args.end_date), "%Y-%m")


def convertDate(date1980, date2):
    r = relativedelta.relativedelta(date2, date1980)
    print(r.years * 12)
    print(r.months)
    final_date = r.years * 12 + r.months + 1
    return final_date


start_date = convertDate(date1, start_str)
end_date = convertDate(date1, end_str)
print("start", start_date)
print("end", end_date)

# get periods
run_id = "d_2020_09_01_prelim"
periods = get_periods(run_id)  # as a list
periods_by_name = get_periods_by_name(run_id)  # as a dict
period_a = periods_by_name["A"]
period_b = periods_by_name["B"]
period_c = periods_by_name["C"]
print(period_c)

# bring in dataset
dataset = views.DATASETS["cm_africa_imp_0"]
df = dataset.df

# array of prediction times
arrayOfPrediction = [*range(period_c.train_start, period_c.predict_end, 1)]
arrayOfPredictionSum = [*range(period_c.predict_start, period_c.predict_end, 1)]
print("arrayOfPrediction", arrayOfPrediction)

# country perturb


Countries = [
    {"Cote d'Ivoire": 40},
    {"Ghana": 41},
    {"Liberia": 42},
    {"Morocco": 43},
    {"Burkina Faso": 46},
    {"Guinea": 47},
    {"Guinea-Bissau": 48},
    {"Mali": 49},
    {"Mauritania": 50},
    {"Senegal": 51},
    {"Sierra Leone": 52},
    {"The Gambia": 53},
    {"Djibouti": 54},
    {"Eritrea": 55},
    {"Ethiopia": 56},
    {"Sudan": 58},
    {"Israel": 61},
    {"Jordan": 62},
    {"Algeria": 67},
    {"Cameroon": 69},
    {"Central African Republic": 70},
    {"Libya": 71},
    {"Tunisia": 73},
    {"Benin": 74},
    {"Chad": 75},
    {"Equatorial Guinea": 76},
    {"Niger": 78},
    {"Nigeria": 79},
    {"Sao Tome and Principe": 80},
    {"Togo": 81},
    {"Egypt": 92},
    {"Oman": 120},
    {"Somalia": 121},
    {"Yemen": 125},
    {"Bahrain": 128},
    {"Kuwait": 130},
    {"Qatar": 131},
    {"Saudi Arabia": 132},
    {"United Arab Emirates": 133},
    {"Botswana": 155},
    {"Burundi": 156},
    {"Rwanda": 158},
    {"Zambia": 160},
    {"Zimbabwe": 161},
    {"Comoros": 162},
    {"Lesotho": 163},
    {"Malawi": 164},
    {"Mozambique": 165},
    {"South Africa": 166},
    {"Swaziland": 167},
    {"Angola": 168},
    {"Congo": 169},
    {"Congo, DRC": 170},
    {"Gabon": 172},
    {"Namibia": 173},
    {"Madagascar": 175},
    {"Seychelles": 177},
    {"Zanzibar": 194},
    {"Ethiopia": 195},
    {"South Africa": 196},
    {"Egypt": 197},
    {"Egypt (United Arab Republic)": 199},
    {"Yemen Arab Republic": 200},
    {"Yemen People's Republic": 201},
    {"Mali Federation": 214},
    {"Cameroon": 215},
    {"Nigeria": 216},
    {"Libya": 217},
    {"Chad": 218},
    {"Morocco": 219},
    {"Morocco": 220},
    {"Mauritania": 221},
    {"Israel": 222},
    {"Israel": 223},
    {"Egypt": 225},
    {"Egypt": 226},
    {"Uganda": 59},
    {"Tanzania": 159},
    {"Kenya": 157},
    {"Tanzania": 193},
    {"Saudi Arabia": 239},
    {"Yemen": 240},
    {"Tanzania": 242},
    {"Morocco": 243},
    {"Mauritania": 244},
    {"Sudan": 245},
    {"South Sudan": 246},
]

# All features that have 0.8 or greater correlation with the primary features to perturb (abs value of corr coefficient)
param_mapping = {
    "wdi_sp_dyn_imrt_in": [
        "wdi_sp_dyn_imrt_ma_in",
        "wdi_sp_dyn_le00_fe_in",
        "wdi_sp_dyn_le00_in",
        "wdi_sp_dyn_le00_ma_in",
        "wdi_sp_dyn_to65_fe_zs",
        "wdi_sp_dyn_tfrt_in",
    ],
    "wdi_ny_gdp_pcap_pp_kd": [
        "wdi_ny_gnp_pcap_pp_cd",
        "wdi_ny_gnp_pcap_pp_kd",
        "wdi_sl_gdp_pcap_em_kd",
        "wdi_ny_gnp_pcap_cd",
        "wdi_ny_gnp_pcap_kd",
        "wdi_sh_xpd_chex_pp_cd",
        "wdi_sh_xpd_pvtd_pp_cd",
        "wdi_sh_xpd_oopc_pc_cd",
        "wdi_sh_xpd_ghed_pp_cd",
        "wdi_sh_xpd_pvtd_pc_cd",
        "wdi_si_pov_umic",
        "wdi_sh_xpd_chex_pc_cd",
        "wdi_sh_xpd_oopc_pp_cd",
    ],
    "wdi_ag_prd_food_xd": ["wdi_ag_prd_lvsk_xd"],
    "vdem_v2x_libdem": [
        "vdem_v2x_mpi",
        "vdem_v2x_polyarchy",
        "vdem_v2x_partipdem",
        "vdem_v2x_liberal",
        "vdem_v2xel_frefair",
        "vdem_v2xnp_pres",
        "vdem_v2x_neopat",
        "vdem_v2x_regime_amb",
        "vdem_v2xcl_rol",
        "vdem_v2x_veracc",
        "vdem_v2x_regime",
        "vdem_v2x_rule",
        "vdem_v2xcl_disc",
        "vdem_v2xlg_legcon",
        "vdem_v2xdl_delib",
    ],
}


def perturb_col(
    cshapeArray, arrayOfPrediction, param_mapping, df, columnPerturb, percentIncrease
):
    """
    Increase by column by percentage
    """
    features = param_mapping[columnPerturb]
    for feat_to_perturb in features:
        try:
            for country in cshapeArray:
                for date in arrayOfPrediction:
                    df.loc[(date, country), feat_to_perturb] = (
                        df.loc[(date, country)][feat_to_perturb] * percentIncrease
                        + df.loc[(date, country)][feat_to_perturb]
                    )
        except:
            print("error")
    return df


if args.country != "All":
    filterCounties = []
    filterCounties.append(eval(args.country))
    print("c:", filterCounties)

    cshapeArray = []
    for filteredCounty in filterCounties:

        for country in Countries:
            for (
                country,
                cshape,
            ) in (
                country.items()
            ):  # for name, age in dictionary.iteritems():  (for Python 2.x)

                if country == filteredCounty:
                    cshapeArray.append(cshape)
                    print(cshapeArray)

    # mutate df gdp
    if float(args.gdp_pcap) != 0:
        print("gdp not none")

        # perform perturbations of all relevant columns
        percentIncrease = float(args.gdp_pcap)
        columnPerturb = "wdi_ny_gdp_pcap_pp_kd"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

    if float(args.infant_mortality) != 0:
        # perform perturbations of all relevant columns
        percentIncrease = float(args.infant_mortality)
        columnPerturb = "wdi_sp_dyn_imrt_in"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

    if float(args.liberalDemocracyIndex) != 0:
        print("lib", args.liberalDemocracyIndex)
        # perform perturbations of all relevant columns
        percentIncrease = float(args.liberalDemocracyIndex)
        columnPerturb = "vdem_v2x_libdem"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

    if float(args.foodProdIndex) != 0:
        print("food", args.foodProdIndex)
        # perform perturbations of all relevant columns
        percentIncrease = float(args.foodProdIndex)
        columnPerturb = "wdi_ag_prd_food_xd"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

elif args.country == "All":
    # array of all countries
    cshapeArray = []
    for country in Countries:
        for (
            country,
            cshape,
        ) in (
            country.items()
        ):  # for name, age in dictionary.iteritems():  (for Python 2.x)
            cshapeArray.append(cshape)
            print(cshapeArray)
    if float(args.gdp_pcap) != 0:
        print("gdp not none")

        percentIncrease = float(args.gdp_pcap)
        columnPerturb = "wdi_ny_gdp_pcap_pp_kd"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

    if float(args.infant_mortality) != 0:

        percentIncrease = float(args.infant_mortality)
        columnPerturb = "wdi_sp_dyn_imrt_in"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

    if float(args.liberalDemocracyIndex) != 0:
        print("lib", args.liberalDemocracyIndex)
        percentIncrease = float(args.liberalDemocracyIndex)
        columnPerturb = "vdem_v2x_libdem"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )

    if float(args.foodProdIndex) != 0:
        print("food", args.foodProdIndex)
        percentIncrease = float(args.foodProdIndex)
        columnPerturb = "wdi_ag_prd_food_xd"
        df = perturb_col(
            cshapeArray,
            arrayOfPrediction,
            param_mapping,
            df,
            columnPerturb,
            percentIncrease,
        )


# get models
model_from_pipeline_spec = all_cm_models_by_name["cm_sb_acled_violence"]
model_from_pipeline_spec1 = all_cm_models_by_name["cm_sb_cflong"]
model_from_pipeline_spec2 = all_cm_models_by_name["cm_sb_neibhist"]
model_from_pipeline_spec3 = all_cm_models_by_name["cm_sb_cdummies"]
model_from_pipeline_spec4 = all_cm_models_by_name["cm_sb_acled_protest"]
model_from_pipeline_spec5 = all_cm_models_by_name["cm_sb_reign_coups"]
model_from_pipeline_spec6 = all_cm_models_by_name["cm_sb_icgcw"]
model_from_pipeline_spec7 = all_cm_models_by_name["cm_sb_reign_drought"]
model_from_pipeline_spec8 = all_cm_models_by_name["cm_sb_reign_global"]
model_from_pipeline_spec9 = all_cm_models_by_name["cm_sb_vdem_global"]
model_from_pipeline_spec10 = all_cm_models_by_name["cm_sb_demog"]
model_from_pipeline_spec11 = all_cm_models_by_name["cm_sb_wdi_global"]
model_from_pipeline_spec12 = all_cm_models_by_name["cm_sb_all_global"]
model_from_pipeline_spec13 = all_cm_models_by_name["cm_sbonset24_25_all"]


# create array of models
models = [
    model_from_pipeline_spec,
    model_from_pipeline_spec1,
    model_from_pipeline_spec2,
    model_from_pipeline_spec3,
    model_from_pipeline_spec4,
    model_from_pipeline_spec5,
    model_from_pipeline_spec6,
    model_from_pipeline_spec7,
    model_from_pipeline_spec8,
    model_from_pipeline_spec9,
    model_from_pipeline_spec10,
    model_from_pipeline_spec11,
    model_from_pipeline_spec12,
    model_from_pipeline_spec13,
]

# update the periods for each of the models
for model in models:
    model.periods = periods

# Build ensemble
cflong_acled_violence_ensemble = Ensemble(
    name="cflong_acled_violence_ensemble",
    models=models,
    outcome_type="prob",
    col_outcome="greq_25_ged_best_sb",
    method="average",
    periods=periods,
)
ensembles = [cflong_acled_violence_ensemble]

for model in models:
    # Uncalibrated predictions
    df_pred = model.predict(df)
    df = assign_into_df(df_to=df, df_from=df_pred)

    df_pred = model.predict_calibrated(
        df=df.fillna(0),
        period_calib=period_b,
        period_test=period_c,
    )
    df = assign_into_df(df_to=df, df_from=df_pred)

for ensemble in ensembles:
    df_pred = ensemble.predict(
        df=df.fillna(0),
        period_calib=period_b,
        period_test=period_c,
    )
    df = assign_into_df(df_to=df, df_from=df_pred)


cols_predict = [ensemble.col_sc_calibrated for ensemble in ensembles]
df_results = df.loc[period_c.times_predict, cols_predict]


def createList(r1, r2):
    return list(range(r1, r2 + 1))


if int(start_date) < int(period_c.times_predict[0]):
    start_date = period_c.times_predict[0]
elif int(start_date) > int(max(period_c.times_predict)):
    start_date = int(max(period_c.times_predict))

if int(end_date) < int(start_date):
    end_date = int(start_date) + 1
if int(end_date) > int(max(period_c.times_predict)):
    end_date = max(period_c.times_predict)


time_p = createList(int(start_date), int(end_date))
print(time_p)
results = df_results.loc[time_p]

nameofcsv = (
    "/usr/local/src/Views_dir/storage/predictions/views_sb_ensemble_script_start="
    + str(args.start_date)
    + "_end="
    + str(args.end_date)
    + "_countries:"
    + str(args.country)
    + "_gdpChange="
    + str(args.gdp_pcap)
    + "_infantMortChange="
    + str(args.infant_mortality)
    + "_liberalDemcChange="
    + str(args.liberalDemocracyIndex)
    + "_foodProdIndChange="
    + str(args.foodProdIndex)
    + ".csv"
)


results.to_csv(nameofcsv)


if __name__ == "__main__":
    print("running")
