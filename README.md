# ViEWS2 Ensemble

## Overview
This repo implements a version of the [Violence Early-Warning System (ViEWS)](https://www.pcr.uu.se/research/views/), developed by [Uppsala University's Department of Peace and Conflict Research](https://www.pcr.uu.se/?languageId=1). Building on the [open source work](https://github.com/UppsalaConflictDataProgram/OpenViEWS2) of the ViEWS team, we provide a machine learning based ensemble model to predict state based violence throughout Africa. The ensemble uses a variety of open source data that has been organized collated by the ViEWS team into a single, large data frame. The model predicts probability of violence 3 years into the future and should be retrained using updated data every few months to ensure the most accurate predictions. 
 
This ensemble model is exposed via a command line interface (CLI) which allows a modeler to perturb key model parameters prior to executing the pre-trained ensemble to predict future violence in a given country.

> **Citation**: 
ViEWS:
Hegre, Håvard, Marie Allansson, Matthias Basedau, Michael Colaresi, Mihai Croicu, Hanne Fjelde, Frederick Hoyles, Lisa Hultman, Stina Högbladh, Naima Mouhleb, Sayeed Auwn Muhammad, Desiree Nilsson, Håvard Mokleiv Nygård, Gudlaug Olafsdottir, Kristina Petrova, David Randahl, Espen Geelmuyden Rød, Nina von Uexkull, Jonas Vestby (2019) ‘ViEWS: A political violence early-warning system’, _Journal of Peace Research_, 56(2), pp. 155–174. doi: [10.1177/0022343319823860](https://doi.org/10.1177/0022343319823860).

> **Github**: [https://github.com/UppsalaConflictDataProgram/OpenViEWS2](https://github.com/UppsalaConflictDataProgram/OpenViEWS2)


# **Usage**

 **Options**:
 There are three different ways to run this ensemble. 
 
  **I**: The first method is locally, which is explained in detail [here (readme)](https://github.com/jataware/views2_ensemble/blob/main/OpenViEWS2/README.md). 
 
 Process:
 
1. Clone git repo

2. Pull docker image

3. Fetch pretrained models and data

4. Run docker image with parameters perturbed or not.

5. See results from model in results folder. 

 **II**: The second method is also run locally, but you build the models yourself with the latest data available. explained in detail after the first method [here (readme)](https://github.com/jataware/views2_ensemble/blob/main/OpenViEWS2/README.md). 

Process:

 1. Clone git repo

 2. Pull docker image

 3. Fetch latest data from source

 4. Build the models locally

 5. Run docker image with parameters perturbed or not.

 6. See results from model in results folder. 
 

 **III**: The third method is through the world modeler's supermaas framework. That process is not available to the public yet so I will not explain that process here. To learn more about world modelers you can read the summary here:  https://www.darpa.mil/program/world-modelers.


## Inputs

The data used in the ensemble model is open source and can be found in the following databases:

> **Note:** all columns or features in the dataframe expected by the ensemble model are prefixed by their source database. For example `Acled_` prefixed columns indicate data that is from [ACLED](https://acleddata.com/resources/general-guides/#1603120929158-3f359ee4-4726). Below are the prefix and associated data sources for all the features used in this ensemble.
  
1. **Fvp**:
This combines multiple databases; columns prefixed `prop_` are from [EPR](https://icr.ethz.ch/data/epr). Columns prefixed `ssp2` are from [SSP](https://tntcat.iiasa.ac.at/SspDb/) and auto, demo, electoral, etc are from [VDEM](https://www.v-dem.net/en/)
2. **Reign**:
[Rulers, Elections, and Irregular Governance dataset](https://oefdatascience.github.io/REIGN.github.io/menu/REIGN_CODEBOOK.html)
3. **Acled_**:
[The Armed Conflict Location & Event Data Project](https://acleddata.com/resources/general-guides/#1603120929158-3f359ee4-4726)
4. **Ged_**:
[UCDP Georeferenced Event Dataset](https://ucdp.uu.se/downloads/)
5. **Icgcw**:
[CrisisWatch](https://www.crisisgroup.org/crisiswatch)
6. **vdem_**:
[Varieties of Democracy](https://www.v-dem.net/media/filer_public/28/14/28140582-43d6-4940-948f-a2df84a31893/v-dem_codebook_v10.pdf)
7. **Wdi_**:
[World Development Indicators](https://databank.worldbank.org/source/world-development-indicators)

## Models
There are 14 models used in this ensemble. They all predict state based violence for a given country month. The `cm` stands for country month, the `sb` stands for state based violence. Each model has its own feature with some overlapping features between models within the ensemble. 

 1. `cm_sb_acled_violence`
 2. `cm_sb_cflong`
 3. `cm_sb_neibhist`
 4. `cm_sb_cdummies`
 5. `cm_sb_acled_protest`
 6. `cm_sb_reign_coups`
 7. `cm_sb_icgcw`
 8. `cm_sb_reign_drought`
 9. `cm_sb_reign_global`
 10. `cm_sb_vdem_global`
 11. `cm_sb_demog`
 12. `cm_sb_wdi_global`
 13. `cm_sb_all_global`
 14. `cm_sbonset24_25_all`

## The ViEWS framework
The ViEWS framework can be found on [Github](https://github.com/UppsalaConflictDataProgram/OpenViEWS2). The ViEWS team are experts on predicting violence using machine learning and open sourced this framework for anyone to use for modeling state based conflict.  

For more information on how the ViEWS framework is set up and how to get started, refer to their [detailed documenation](https://views.pcr.uu.se/download/docs/views.pdf).

Though the ViEWS framework allows modelers to generate their own models, we decided to implement an ensemble of the ViEWS' team standard models which are used for their monthly, public predictions for areas around the world. An example of monthly prediction report can be found [here](http://files.webb.uu.se/uploader/1576/ViEWS-Reports--53-.pdf).

## The ensemble workflow
In our workflow, each of the 14 models within the ensemble runs indepdently to generate its own prediction. These predictions are combined to generate a composite prediction. 

The workflow for training this ensemble is neither quick nor simple due to large space and memory requirements needed to run all 14 models. In total, all the data and cached models are ~70GB. Our goal was to Dockerize a pre-trained version of this ensemble to minimize end-user effort and computation, while offering a reasonable degree of flexibility around perturbing a key set of input parameters. 

### Dockerization
Originally we attempted to save the 14 pre-trained models directly in the Docker image so they would always be available for any user who `docker pulls` the container. Unfortunately, the Docker image including all models and data is 83GB and is impractical for storage on a common Docker registry such as DockerHub. To mitigate this issue we store the pre-trained models and data in an Amazon S3 Bucket; these are copied to the ready Docker container prior to each model run. 

After the models/data are downloaded we activate the `views2` environment in our Docker container and run the `sb_ensemble.py` script to run the ensemble model.

### Model parameters
The model allows the user to make parameter selections prior to the model run. These are:

looks for any parameters passed by the user to determine if the dataframe needs to be perturbed before a prediction is made. The parameters we exposed are:

- `--start_date`: prediction start.
- `--end_date`: prediction end.
- `--country`: if country is defined only the country passed to the ensemble will be perturbed before prediction, otherwise all countries are modeled.
- `--gdp_pcap`: a percentage perturbation against gpd per capita (`wdi_ny_gdp_pcap_pp_kd`) where 0 is baseline (no perturbation)
- `--infant_mortality`: a percentage perturbation against annual infant mortality rate (`wdi_sp_dyn_imrt_in`) where 0 is baseline (no perturbation)
- `--liberalDemocracyIndex`: a percentage perturbation against liberal democracy index where 0 is baseline (no perturbation)
- `--foodProdIndex`: a percentage perturbation against the food production index where 0 is baseline (no perturbation).

#### Parameterization by country

Only a subset of countries may have their parameters perturbed. They are:

* Ethiopia
* Sudan
* South Sudan
* Kenya
* Egypt
* Libya
* Saudi Arabia
* Somalia
* Eritrea
* Chad
* Central African Republic
* Uganda
