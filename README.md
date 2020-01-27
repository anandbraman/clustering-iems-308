# clustering-iems-308
Homework 1: Pose and solve a business problem with clustering using Medicare Physician and Other Supplier data.

## Running Scripts
First, create a folder titled **data**. Within the data folder create two folders, one called **processed** and one called 
**unprocessed**. Next, save the raw Medicare text data to the unprocessed folder. After saving the Medicare text data to this 
folders, run the **subsetting_and_cleaning.py** file, which generates the processed data used in the clustering script. After running 
**subsetting_and_cleaning.py**, it will be possible to run the **clustering.py** script, as dummy coded, subsetted data
will now exist in the processed data folder. **clustering.py** represents a pared down version of **clustering.ipynb**. 
The output is the means of the columns, grouped by cluster.

## Full Analyses
More detailed analyses can be found in **clustering.ipynb**. All inspection of the clusters occurred in this notebook
with the findings summarized in **medicareReport.docx**.

Enjoy!
