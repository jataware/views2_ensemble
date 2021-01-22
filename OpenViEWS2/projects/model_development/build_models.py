import json
import logging
import views

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

dataset = views.DATASETS["cm_africa_imp_0"]
df = dataset.df

run_id = "d_2020_09_01_prelim"
periods = get_periods(run_id) # as a list
periods_by_name = get_periods_by_name(run_id)# as a dict

period_a = periods_by_name["A"]

period_b = periods_by_name["B"]
period_c = periods_by_name["C"]


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
for model in models:
    model.periods = periods

for model in models:
    model.fit_estimators(df, populate_extras = False)

print('finish')
