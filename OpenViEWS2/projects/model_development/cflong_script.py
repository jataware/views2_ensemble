import json
import logging
import views
import datetime
logging.basicConfig(
    level=logging.DEBUG,
    #level=logging.INFO, # uncomment this and comment debug above for less yelling in red
    format=views.config.LOGFMT,
)

# DATASETS is a dictionary of Dataset objects.
from views import DATASETS
# These are the building blocks of the modelling interface
from views import Ensemble, Model, Downsampling, Period
# These are model specifications from the specfiles
from views.specs.models import cm as model_specs_cm, pgm as model_specs_pgm
from views.specs.periods import get_periods, get_periods_by_name
# Utils
from views.utils import db, io, data as datautils
from views.utils.data import assign_into_df

from views.apps.pipeline.models_cm import all_cm_models_by_name
from views.apps.pipeline.models_pgm import all_pgm_models_by_name

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
for name, dataset in DATASETS.items():
    print(name)

dataset = views.DATASETS["cm_africa_imp_0"]
df = dataset.df

run_id = "r_2020_07_01"

periods = get_periods(run_id) # as a list
periods_by_name = get_periods_by_name(run_id) # as a dict

period_b = periods_by_name["B"]
period_c = periods_by_name["C"]

#get model
model_from_pipeline_spec = all_cm_models_by_name["cm_sb_cflong"]

df_pred = model_from_pipeline_spec.predict(df)
    # assign_into_df takes care to only overwrite rows with actual values
    # This way we can keep all periods in the same df
    # It's also idempotent, no joining, so run as many times as you like. 
df = assign_into_df(df_to=df, df_from=df_pred)
df_pred = model_from_pipeline_spec.predict_calibrated(
        df=df, 
        period_calib=period_b,
        period_test=period_c,
    )
df = assign_into_df(df_to=df, df_from=df_pred)

models=[model_from_pipeline_spec]
cols_predict = [model_from_pipeline_spec.col_sc_calibrated for model in models]
df_results=df.loc[period_c.times_predict, cols_predict]

nameofcsv = "cflong_results_script" + str(datetime.datetime.now()) +".csv"
df_results.to_csv(nameofcsv)
    
if __name__ == "__main__":
    print("running")