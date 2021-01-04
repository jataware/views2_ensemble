# ViEWS2 Ensemble

 **Overview**  This repo provides a machine learning ensemble to predict state based violence throughout Africa. The ensemble uses data from a variety of open sources that has been organized into a large dataframe provided by the ViEWS team. The model predicts probability of violence 3 years into the future and should be retrained about very few months for the most accurate predictions. 
 
This ensemble is exposed by a command line interface which allows users to manipulate  input data before running the pre-trained ensemble to predict future violence in a given country.

 **Citation**: 
ViEWS:
Hegre, Håvard, Marie Allansson, Matthias Basedau, Michael Colaresi, Mihai Croicu, Hanne Fjelde, Frederick Hoyles, Lisa Hultman, Stina Högbladh, Naima Mouhleb, Sayeed Auwn Muhammad, Desiree Nilsson, Håvard Mokleiv Nygård, Gudlaug Olafsdottir, Kristina Petrova, David Randahl, Espen Geelmuyden Rød, Nina von Uexkull, Jonas Vestby (2019) ‘ViEWS: A political violence early-warning system’, _Journal of Peace Research_, 56(2), pp. 155–174. doi: [10.1177/0022343319823860](https://doi.org/10.1177/0022343319823860).

Github: https://github.com/UppsalaConflictDataProgram/OpenViEWS2

# **I. Ensemble Inputs**
 **Open Source Data**:
 The data used in the models can be found at these databases:

All columns or features in the dataframe are prefaced by which database they originally came from. Below are the prefix and associated data sources for all the features used in this ensemble.
  
Fvp:
Columns prefixed prop_ are from EPR, see [https://icr.ethz.ch/data/epr](https://icr.ethz.ch/data/epr/)/
Columns prefix ssp2 are from SSP, see [https://tntcat.iiasa.ac.at/SspDb/](https://tntcat.iiasa.ac.at/SspDb/)
Auto, demo, electoral, etc are from VDEM, see [https://www.v-dem.net/en/](https://www.v-dem.net/en/)

Reign:
[https://oefdatascience.github.io/REIGN.github.io/menu/REIGN_CODEBOOK.html](https://oefdatascience.github.io/REIGN.github.io/menu/REIGN_CODEBOOK.html)

Acled_:
[https://acleddata.com/resources/general-guides/#1603120929158-3f359ee4-4726](https://acleddata.com/resources/general-guides/#1603120929158-3f359ee4-4726)

Ged_:
[https://ucdp.uu.se/downloads/](https://ucdp.uu.se/downloads/)

Icgcw:
[https://www.crisisgroup.org/crisiswatch](https://www.crisisgroup.org/crisiswatch)

vdem_:
[https://www.v-dem.net/media/filer_public/28/14/28140582-43d6-4940-948f-a2df84a31893/v-dem_codebook_v10.pdf](https://www.v-dem.net/media/filer_public/28/14/28140582-43d6-4940-948f-a2df84a31893/v-dem_codebook_v10.pdf)

Wdi_:
[https://databank.worldbank.org/source/world-development-indicators](https://databank.worldbank.org/source/world-development-indicators)

 **The Models**:
 There are 14 models used in this ensemble. They all predict state based violence for a given country month. The cm stands for country month, the sb stands for state based violence. Each model has its own feature with a few features overlapping between models. 

 1. "cm_sb_acled_violence"
 2. "cm_sb_cflong"
 3.  "cm_sb_neibhist"
 4. "cm_sb_cdummies"
 5. "cm_sb_acled_protest"
 6.  "cm_sb_reign_coups"
 7. "cm_sb_icgcw"
 8. "cm_sb_reign_drought"
 9.  "cm_sb_reign_global"
 10. "cm_sb_vdem_global"
 11.  "cm_sb_demog"
 12. "cm_sb_wdi_global"
 13. "cm_sb_all_global" 
 14.  "cm_sbonset24_25_all"

## Getting to know the ViEWS framework
The ViEWS framework can be found on github and downloaded [here](https://github.com/UppsalaConflictDataProgram/OpenViEWS2). The views team are experts on predicting violence using machine learning and have put together this framework for anybody to use.  

For more information on how the ViEWS framework is set up and how to get started you can see the additional documentation [here](https://views.pcr.uu.se/download/docs/views.pdf).

Even with the option of creating our own models, we decided to rebuild their standard models that are used in their monthly predictions for areas around the world. An example of one of these monthly predictions can be send here.

## How the ensemble works

To make a prediction with the ensemble each model needs to make it's own prediction. 

## Jataware's Workflow
The workflow for this ensemble is not quick or simple due to the requirements of all 14 models. In total all the data and saved models add up to around 70GB. Our goal was to dockerize the ensemble and expose parameters so the user can perturb the data to create novel scenarios and see how predictions of state based violence might change. 

**Dockerization:** 
We started with trying to save the models in the docker image so it could be always their when the user run the ensemble. This didn't work however due to the large size of the image at 83GB. To get around this problem we decided to store the pre-trained models and data in an Amazon S3 Bucket which we download before each run. 

After the models/data are downloaded we activate the views2 environment in our docker container and run our script to run the ensemble.

**Exposed Parameters:** 
The script looks for any parameters passed by the user to determine if the dataframe needs to be perturbed before a prediction is made. The parameters we exposed are:
-   --start_date: prediction start.
-   --end_date: prediction end.
- --gdp_pcap: a percentage perturbation against gpd per capita (wdi_ny_gdp_pcap_pp_kd) where 0 is baseline (no perturbation)
- --infant_mortality: a percentage perturbation against annual infant mortality rate (wdi_sp_dyn_imrt_in) where 0 is baseline (no perturbation)
- -Liberal Democracy Index:  



Countries you can select to perturb: 

| Country |  
|--|--|
| Algeria |
| Angola |
| Bahrain |
| Benin |
| Botswana |
| Burkina Faso |
| Burundi |
| Cameroon |
| Central African Republic |
| Chad |
| Comoros |
| Congo |
| Congo, DRC |
| Cote d'Ivoire |
| Djibouti |
| Egypt |
| Egypt (United Arab Republic) |
| Equatorial Guinea |
| Eritrea |
| Ethiopia |
| Gabon |
| Ghana |
| Guinea |
| Guinea-Bissau |
| Israel |
| Jordan |
| Kenya |
| Kuwait |
| Lesotho |
| Liberia |
| Libya 
| Madagascar |
| Malawi |
| Mali |
| Mali Federation |
| Mauritania |
| Morocco |
| Mozambique |
| Namibia |
| Niger |
| Nigeria |
| Oman |
| Qatar |
| Rwanda |
| Sao Tome and Principe |
| Saudi Arabia |
| Senegal |
| Seychelles |
| Sierra Leone |
| Somalia |
| South Africa |
| South Sudan |
| Sudan |
| Swaziland |
| Tanzania |
| The Gambia |
| Togo |
| Tunisia |
| Uganda |
| United Arab Emirates |
| Yemen |
| Yemen Arab Republic |
| Yemen People's Republic |
| Zambia |
| Zanzibar |
| Zimbabwe |


