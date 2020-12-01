import datetime
import json
import logging
import views
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--start_date', default="483")
parser.add_argument('--end_date', default="520")
args = parser.parse_args()
print("start_date", args.start_date, "end_date", args.end_date)


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
#from views.utils import db, io, data as datautils
from views.utils.data import assign_into_df
from views.apps.pipeline.models_cm import all_cm_models_by_name
from views.apps.pipeline.models_pgm import all_pgm_models_by_name
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

#logging errors
logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO, # uncomment this and comment debug above for less yelling in red
    format=views.config.LOGFMT,
)


#get periods
run_id = "d_2020_10_01_prelim"
periods = get_periods(run_id) # as a list
periods_by_name = get_periods_by_name(run_id)# as a dict
period_a = periods_by_name["A"]
period_b = periods_by_name["B"]
period_c = periods_by_name["C"]


#bring in dataset
dataset = views.DATASETS["cm_africa_imp_0"]
df = dataset.df


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
model_from_pipeline_spec11= all_cm_models_by_name["cm_sb_wdi_global"]
model_from_pipeline_spec12 = all_cm_models_by_name["cm_sb_all_global"]
model_from_pipeline_spec13 = all_cm_models_by_name["cm_sbonset24_25_all"]


#create array of models
models=[
        model_from_pipeline_spec ,
        model_from_pipeline_spec1,
        model_from_pipeline_spec2,
        model_from_pipeline_spec3 ,
        model_from_pipeline_spec4,
        model_from_pipeline_spec5,
        model_from_pipeline_spec6 ,
        model_from_pipeline_spec7,
        model_from_pipeline_spec8,
        model_from_pipeline_spec9 ,
        model_from_pipeline_spec10,
        model_from_pipeline_spec11,
        model_from_pipeline_spec12,
        model_from_pipeline_spec13
       ]

#update the periods for each of the models
for model in models:
    model.periods = periods

#Build ensemble
cflong_acled_violence_ensemble = Ensemble(
    name="cflong_acled_violence_ensemble",
    models=models,
    outcome_type="prob",
    col_outcome="greq_25_ged_best_sb",
    method="average",
    periods=periods
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
    return list(range(r1, r2+1))


if int(args.start_date) < int(period_c.times_predict[0]):
    args.start_date = period_c.times_predict[0]
elif int(args.start_date) > int(max(period_c.times_predict)):
    args.start_date = int(max(period_c.times_predict))

if int(args.end_date) < int(args.start_date):
    args.end_date = int(args.start_date) + 1
if int(args.end_date) > int(max(period_c.times_predict)):
    args.end_date = max(period_c.times_predict)



time_p = createList(int(args.start_date), int(args.end_date))

results = df_results.loc[time_p]

nameofcsv_test = "storage/predictions/views_sb_ensemble_script_start=" + str(args.start_date) +"_end="+str(args.end_date) +"_currentTime="+ str(datetime.datetime.now()) + ".csv"
results.to_csv(nameofcsv_test)


if __name__ == "__main__":
    print("running")
