

## Sponsorship Checker App 

A app that checks if a company are registered sponsor in the UK. 

Currently, registered companies comes from a static csv file downloaded from UK government. This file is uploaded into gcloud big query.


Redeploy an app in host location use this command:

```sh
gcloud builds submit --tag eu.gcr.io/visa-sponsor-uk/checker-app .
```
This process manage docker seamlessly.

## Road map

There may need a seperate pipeline to update this dataset on a weekly basis. Example would be use web agency to click throw website, 
downlaod a api.