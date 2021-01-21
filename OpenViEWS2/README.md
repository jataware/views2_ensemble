# ViEWS2

Getting started

Download and install miniconda3: https://docs.conda.io/en/latest/miniconda.html
After you have conda installed, in your terminal run

    ./install_views2.sh

This will create a conda environment called views2 and install the views package there.
To fetch the latest public data run

    conda activate views2
    python runners/import_data.py --fetch

To start using ViEWS code simply run

    conda activate views2
    jupyter notebook

A web browser should open with the jupyter notebook browser.
If you wish to take part in the prediction competition, see projects/prediction_competition/
An example notebook to get you started modelling is in projects/model_development/examply.ipynb.

We develop ViEWS on Mac and Linux computers, the procedure is slightly different for Windows and we haven't developed a streamlined process for it yet.

To open the HTML documentation from here on MacOS run

    ./run_tools.sh
    open docs/_build/html/index.html

And it will take you to the locally built html documementation in your default browser.

To view .pdf documentation (a work in progress) see https://views.pcr.uu.se/download/docs/views.pdf


# Views2 

## **Instructions for building and pushing the data and models to S3**

 1. First clone the repo:

  
		git clone https://github.com/jataware/views2_ensemble.git 

       
2. Make sure you have miniconda installed on your computer. This was tested on linux ubuntu 18.04. Download and install miniconda3: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
3. One conda is installed and the repo is downloaded it's time to set up the views2 environment. You can do this by navigating to the OpenViEWS2 folder and running a bash script.
			 

       cd OpenViEWS2/
       ./install_views2.sh

4. You should see all dependencies downloaded and installed and at this point the views2 environment should be able to be activated.

		conda activate views2
 **

 **Get the latest data**

  

5. To get the latest data from ViEWS run this command:

    
		 python runners/import_data.py --fetch


6. This takes a while but it should work and will populate a storage folder with data.
7. If this fails go to the views site and download the data manually as a zip. You can see the zip files here [https://views.pcr.uu.se/download/datasets/](https://views.pcr.uu.se/download/datasets/).  Download the latest version of views_tables_and_geoms_*.zip. 
8. Something like this could work:


		cd OpenViEWS2/
		wget “https://views.pcr.uu.se/download/datasets/views_tables_and_geoms_20200923.zip”


9. This should download the data. Next you have to unzip and organize the tables and data. The easiest way to do this is to go to the OpenViEWS2 directory and start a python session. *make sure views2 conda environment is active.
			  

    python
    ">>>
	
	  
		import views
		def run_import_tables_and_geoms(path_zip):
			views.apps.data.public.import_tables_and_geoms(
			tables=views.TABLES, geometries=views.GEOMETRIES, path_zip=path_zip,
			)

		def refresh_datasets():

		datasets_to_update = [
		"cm_global_imp_0",
		"cm_africa_imp_0",
		"pgm_global_imp_0",
		"pgm_africa_imp_0",
		]
		for dataset_name in datasets_to_update:
			views.DATASETS[dataset_name].refresh()
		Path_zip = ‘'./storage/scratch/views_tables_and_geoms_20200923.zip'
		#run the functions
		run_import_tables_and_geoms(path_zip)
		refresh_datasets()

10. Now you should have access to the data!

## Build the models

11. Now to build the models with the new data.
12. The first step is setting up the periods to train and test the models on. This will be done by navigating to the periods.yaml file:

		cd ~/views2_ensemble/OpenViEWS2/views/specs/periods/
		nano periods.yaml
			

13. Create a new period: ViEWS works primariliy at the monthly temporal resolution, they use an id system where month_id=1 corresponds to 1980.01, January 1980.  
so :
		

	    490  = 2020.10  
	    527   = 2023.11
		
An example of a period is:

	  d_2020_09_01_prelim:
		A: # Calibration period for B
			train:
				start: 121 # 1990.01
				end: 396 # 2012.12
			predict:
				start: 397 # 2013.01
				end: 432 # 2015.12,
		B: # Evaluation period. Calibration for C.
			train:
				start: 121 # 1990.01
				end: 432 # 2015.12
			predict:
				start: 433 # 2016.01,
				end: 480 # 2019.12, last month yearly data
		C:
			train:
				start: 121 # 1990.01
				end: 489 # 2020.9
			predict:
				start: 490 # 2020.10
				end: 527 # 2023.10


a. The period dicts are defined by three periods that span the dataset. 	
b. Period A can always be the same
c. Period B predicts up to the last month of yearly data. Since we downloaded data that went up to 09 that is as far as we can go.
d. Period C trains on all data up to last month of data. Then it predicts from the next month to three years in the future. 

14. After you save this in the runs: section we can update our python script to build models. build_models.py

	  

		#On line 27 change this id to the new period you created in the yaml file.
		run_id = "d_2020_09_01_prelim"
15. This script should now be using the latest data along with an updated period to reflect the new data.
			

		cd /views2_ensemble/OpenViEWS2/
		Python projects/model_development/build_models.py

16. This will build the models. It will take a long time because there are 14 models to build and there is a lot of data. Once the models have been built we can zip up the storage folder and push it to s3.

## Upload models and new data to s3
	
This part is pretty simple. 
1. Zip all files in the storage folder.
	

	    cd /OpenViEWS2/storage/
		zip -r ../storage.zip .
2. Now we have our zipped data and models. We can use the upload_to_s3.py script for that.
				

		   python ~/views2_ensemble_updated/OpenViEWS2/projects/model_development/upload_to_s3.py
		
