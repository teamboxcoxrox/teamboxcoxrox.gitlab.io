# A Multifaceted Product Recommendation System
Link: https://teamboxcoxrox.github.io/teamboxcoxrox.gitlab.io/
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

## 1.  Prerequisite python version and required libraries.

Required libraries are listed in the requirements.txt file in the project repository.  The following command can be used in order to install the required libraries:
``` bash
pip install -r requirements.txt
```
Any further missing packages can be installed following instructions found [here](https://pip.pypa.io/en/stable/reference/pip_install/)

Note separate javascript libraries are required for the visualization part of this application.  Those libraries are
contained in the visualization folder in the project repository.

## 2.  Download and preprocess source data.
Data for this project can be downloaded with the Pet_Reviews_Data_Import_Pipeline.ipynb.  This notebook contains code
that downloads data from the source data repository, pre-processes and restructures that data  and then creates pets.db,
which is a Sqlite3 databased used by the data analytics pipeline components described in the next section.  The pets.db
database contains 2 tables that hold product information for 205,999 amazon products, and 6,542,483 product
recommendations.  The overall size of the pets.db database is:  4.7G

## 3.  Run the components of the analytic pipeline. This includes running the following analytic models (See EXECUTION section for further details):
a.  DFTI - Direct Frequency Topic Identification
b.  Sentiment Analysis
c.  Product Ranking Analysis
d.  Latent Dirichlet Allocation (LDA) Topic Analysis
e.  Link Validation
## 4.  Aggregate the output of the analytic pipeline by running the recommendation builder notebook.
## 5.  Execute the user interface.

In general, this is a large and complex visualization.  If you experience difficulty in getting this code to work,
please reach out to the BOXCOXROX contact person for installation and implementation questions:

Miles Porter
(mporter45 at gatech dot com)

Thanks for your interest in our project!

## EXECUTION - How to run a demo on your code

To run this code locally, make sure that you have python 3.7 or later.  Then following the 
follow the following steps:

1.  Clone this repo git  https://github.com/teamboxcoxrox/teamboxcoxrox.gitlab.io
2.  Go into the /docs folder:
``` bash
cd docs
```
3.  Run the following command:
``` bash
python -m http.server
```
4.  Point your browser at  http://localhost:8000 or http://0.0.0.0:8000/

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
