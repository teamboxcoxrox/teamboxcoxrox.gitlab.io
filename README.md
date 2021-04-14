# A Multifaceted Product Recommendation System
Visualization Link: https://teamboxcoxrox.github.io/teamboxcoxrox.gitlab.io/
## DESCRIPTION

This repository contains the visualization component and codebase used for all the analytical modelling performed for the team project for Team #017 Boxcoxrox for Georgia Tech CSE 6242 Spring 2021.

The final deliverable of this project is an interactive web-based application that allows users to search for pet
products that have been organized and prioritized based on extensive analytical techniques applied to customer product
reviews.  This approach differs from Amazon search interface, which is largely driven by seller. For more information
about this project, please refer to the complete project report and supporting documents in the DOCS folder.

## INSTALLATION - How to install and setup your code

To install this code, clone this github repository:  
https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io

Data required for the visualization component has been included with the code.

The following instructions are intended for anyone wishing to attempt to recreate out work.  Please note several things:
1.  This project involves several large files that are downloaded from the internet.
2.  This project involves multiple data analytics models that are part of a larger pipeline and can take hours, and in
    some cases days, to complete.
3.  This project requires Python 3.7, and numerous libraries.


https://pip.pypa.io/en/stable/reference/pip_install/

Recreating the work described in the project report consists of the following steps:

### 1.  Prerequisite python version and required libraries.

Required libraries are listed in the [requirements.txt](https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io/tree/refactor-codebase/CODE) file in the project repository.  The following command can be used in order to install the required libraries:
1.  Go into the CODE folder:
``` bash
cd CODE
```
2.  Run pip install using requirements.txt
``` bash
pip install -r requirements.txt
```
Any further missing packages can be installed following instructions found [here](https://pip.pypa.io/en/stable/reference/pip_install/)

Jupyter is required to run some of the ipynb used in the pipeline. Please refer to https://jupyter.org/install to install it on your computer.

Note: Separate javascript libraries are required for the visualization part of this application.  Those libraries are
contained in the visualization folder in the project repository.

### 2.  Download and preprocess source data.
Data for this project can be downloaded with the [Pet_Reviews_Data_Import_Pipeline.ipynb](https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io/tree/refactor-codebase/CODE/preprocess). This notebook contains code that downloads data from the source data repository, pre-processes and restructures that data  and then creates pets.db, which is a Sqlite3 databased used by the data analytics pipeline components described in the next section. 

The pets.db database contains 2 tables that hold product information for 205,999 amazon products, and 6,542,483 product recommendations. The overall size of the pets.db database is:  4.7GB

### 3.  Run the components of the analytic pipeline. This includes running the following analytic models (See EXECUTION section for further details):
*  Direct Frequency Topic Identification (DFTI)
*  Sentiment Analysis
*  Product Ranking Analysis
*  Latent Dirichlet Allocation (LDA) Topic Analysis
*  Link Validation

### 4.  Final Data Aggregation - Aggregate the output of the analytic pipeline by running the recommendation builder notebook (See EXECUTION section for further details).

### 5.  Execute the visualization user interface (See EXECUTION section for further details)

In general, this is a large and complex visualization.  If you experience difficulty in getting this code to work,
please reach out to the BOXCOXROX contact person for installation and implementation questions:

Miles Porter
(mporter45 at gatech dot com)

Thanks for your interest in our project!

## EXECUTION - How to run a demo on your code

Clone this repo git  https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io

### Direct Frequency Topic Identification (DFTI)
DFTI is a new approach that the team developed to provide an initial top level categorization of the products based on product reviews.  This approach is described in the python notebook [Product_Categorization_Script_DFTI.ipynb](https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io/tree/refactor-codebase/CODE/DFTI_categorization).  

To execute this notebook, ensure that a copy of the pets.db is in the same directory as the script.  
Note:  The script may contain reference to a file pets_all.db.  This is the same SqlLite database, except metadata for the original products are included. For development purposes, we used the smaller pets.db file based on its smaller size. Again, the only difference between pets.db and pets_all.db is that pets_all.db contains a table called products that has metadata about the original amazon products.

1.  Go into the CODE/DFTI_categorization folder:
``` bash
cd CODE/DFTI_categorization
```
2.  Run jupyter notebook
``` bash
jupyter notebook
```
3. A webpage pointing to http://localhost:8888/tree will pop-up on your server
4. Click on Product_Categorization_Script_DFTI.ipynb which will redirect you to the notebook hosted at http://localhost:8888/notebooks/Product_Categorization_Script_DFTI.ipynb

The output of the DFTI process is a single file, category.csv.  This file should be copied to the LDA_Sklearn as it is
required as part of the LDA process for reviews in each of the product categories. The LDA_Sklearn process will be
discussed later in this document.

### Sentiment Analysis
This analysis uses the Vader sentiment analysis tool, which evaluates text and returns a sentiment score from -1 to 1.  For more information on Vader, please refer to the complete project report.  Code that runs Vader on the pet reviews is contained in the sentiment directory and is called [sentiment_calculation.py](https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io/tree/refactor-codebase/CODE/sentiment).  This is a python script (not a jupyter notebook) and can be run from the command line.  The program can be executed like so:
1.  Go into the CODE/sentiment folder:
``` bash
cd CODE/sentiment
```
2.  Run python script
``` bash
python sentiment_calculation.py
```
Note:  Sentiment on 6,542,483 reviews took 0:36:53.268296 running on a Intel® Core™ i5-7600K CPU @ 3.80GHz × 4  with 32
GB of ram running Ubuntu 20.04.

### Product Ranking Analysis
The goal of product ranking analysis is to rank the products based on the number of stars customers reported as part of their reviews.  The raking is done by the [quantiles.py](https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io/tree/refactor-codebase/CODE/quantiles) file in the quantiles directory of the code.  This python file loads all of the reviews, and then aggregates them by product (asin).  Next, the code
calculates the mean, median and standard deviation of the stars.  The code also calculates the average lenth of review text.  More information about how these statistics are used to compute a complete product ranking can be found in the project report.  To calculate product ranking scores, make sure that the pets_all.db file is in the /quantiles directory. (Both the 6,542,483 reviews and the 205,999 product metadata records are required for this calculation.)
Product ranking results can be calculated with the following command:

1.  Go into the CODE/quantiles folder:
``` bash
cd CODE/quantiles
```
2. Ensure the pets_all.db file is in the directory
3.  Run python script
``` bash
python quantiles.py
```

The result of this python script is a csv file named ranking.csv that will be used by the recommendations builder
which is described later in this document.

Note:  Quantiles on 6,542,483 reviews took 0:01:46.475446 running on a Intel® Core™ i5-7600K CPU @ 3.80GHz × 4  with 32
GB of ram running Ubuntu 20.04.

### Latent Dirichlet Allocation (LDA) Topic Analysis
We initially used Spark LDA for the LDA topic analysis but after we developed using our DTFI approach described above, we found that Spark was no longer necessary.  This resulted in a new approach which leveraged Sklearn LDA, which is contained in the LDA_Sklearn directory.  The code for the LDA process is contained in the bcr_LDA.py file in the /LDA_Sklearn directory. The LDA process requires the pets_all.db database, and the categories.csv file described in the DFTI section above. The program retrieves all reviews in a given category, and then performs LDA topic extraction on those documents. Seven topic clusters are defined for each category.

1.  Go into the CODE/LDA_Sklearn folder:
``` bash
cd CODE/LDA_Sklearn
```
2. Ensure the pets_all.db database and file categories.csv are in the directory
3.  Run python script
``` bash
python bcr_LDA.py
```

This command will create the csv file LDA_Category_Topic.csv which will be used in the final aggregation below. Since LDA is an unsupervised algorithm, the clusters identified are not known beforehand.  As a result, png files and a separate LDA visualization is generated as part of the algorithm as well.  These artifacts are then included in the final visualization for the project.

Note:  Quantiles on 6,542,483 reviews took 0:01:46.475446 running on a Intel® Core™ i5-7600K CPU @ 3.80GHz × 4  with 32
GB of ram running Ubuntu 20.04.

### Link Validation
Due to the dynamic nature of Amazon, some of the products that are included in the dataset are no longer active on the platform.  Link validation aims to improve the user experience by not posting links to deactivated products.  Link validation is a batch process similar to the other data processing steps in our pipeline.  The code for link validation is in the /link_validator [directory](https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io/tree/refactor-codebase/CODE/link_validator).  This code can be run with the following command:

1.  Go into the CODE/link_validator folder:
``` bash
cd CODE/link_validator
```
2. Ensure the pets_all.db database and file categories.csv are in the directory
3.  Run python script
``` bash
python link_validation.py
```

Note:  The link validation uses Selenium and the Firefox Geckodriver.  The code included in this repo is designed to
be run on Linux, but could be modified to run on windows or a Mac.  The code attempts to valid Amazon ASINs by
hitting the amazon website product link.  For example:  https://www.amazon.com/dp/B01HGX59I6  The results of this script
is a .csv file that is used in the aggregation process covered in the next section.

Note:  We performed link validation only for the top ranked products.  Link validation take approximately 2.7 seconds
per product.  To validate all products, it would take around 150 hours, or 6.25 24-hour days.

### Final Data Aggregation
Final data aggregation is performed by the [Recommendations_builder.ipynb](https://github.com/fractalbass/boxcoxrox/tree/main/pets/CODE/aggregator) in the /aggregator directory. This jupyter notebook generates a final CSV file that is used in the visualization. Instructions for running the recommendation builder are included as part of the notebook.  The final results of this notebook are saved in a CSV file called products_prepped.csv that is used as part of the product visualization.

1.  Go into the CODE/aggregator folder:
``` bash
cd CODE/aggregator
```
2.  Run jupyter notebook
``` bash
jupyter notebook
```
3. A webpage pointing to http://localhost:8888/tree will pop-up on your server
4. Click on Recommendations_builder.ipynb which will redirect you to the notebook hosted at http://localhost:8888/notebooks/Recommendations_builder.ipynb

Note: The source data for this project included products that were duplicated while others were not related to pets.  We believe that this is due to the fact that occasionally some ASINs get "hijacked" by other products.  In order to address these issues prior to visualization, we have removed duplicated ASINs, and have manually verified that the products that are in our visualization dataset are actually related to pets.  It is highly likely that we have missed some products.


### Visualization User Interface
Hosted application https://teamboxcoxrox.github.io/teamboxcoxrox.gitlab.io/

To run this code locally, make sure that you have python 3.7 or later. Follow the following steps to deploy the visualization locally:
1.  Go into the /docs folder:
``` bash
cd docs
```
2.  Run the following command:
``` bash
python -m http.server
```
3.  Point your browser at  http://localhost:8000 or http://0.0.0.0:8000/


## [Optional, but recommended] DEMO VIDEO -



====================== LICENSE ======================

MIT License

Copyright (c) 2021 Georgia Institute of Technology CSE 6242 Spring Semester Team 017 Team BoxCoxRox
N. Abramson, M. Kunnen, K. Matisko, K. McCanless, M. Porter and S. Tay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
