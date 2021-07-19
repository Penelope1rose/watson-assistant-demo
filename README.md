
# Watson Assistant Demo

In this sample application, you're engaging with a banking virtual assistant. The assistant simulates a few scenarios, such as reporting a missing debit card, increasing credit card limit, enquire on service request details and asking FAQs. Watson can understand your entries and respond accordingly.

This app demonstrates the Watson Assistant and Watson Discovery service via a complete, complex interface which engages in simulated banking tasks. It utilises features such as:

* Cloud Functions
* Disambiguations
* Digression
* Webhooks
* Slots
* Multi-Conditional Responses
* Search Skill

## Architecture

![Cooperation architecture diagram](/images/architecture-diagram.png)

This solution combines a chat interface (Watson Assistant), data storage (Core Banking System) to store the credit limit update, a database (CRM System) that holds service request information and Watson Discovery services with documents to get users the information they need.

1. The Recipient launches the chatbot from the bank's website.
2. The Recipient can ask questions to Watson Assistant and get answers on travel tips/credit card questions.
3. The Recipient can report for a missing debit card and get the card blocked through the chatbot.
4. The Recipient can obtain service request details on cases logged by recipient in the CRM System through the chatbot.

## Prerequisites
1. Sign up for an [IBM Cloud account](https://cloud.ibm.com/registration)
2. Download and install the following:
	*  [IBM Cloud CLI](https://cloud.ibm.com/docs/cli/index.html#overview)
	*  [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads)
	*  [Git](https://git-scm.com/downloads)
	*  [Python](https://www.python.org/downloads/)

## Steps
 1. [Clone this repo](#1.-clone-this-repository)
 2. [Create an instance of the required services](#2.-create-an-instance-of-the-required-services)
 3. [Set up Watson Assistant](#3.-set-up-watson-assistant)
 4. [Set up Watson Discovery](#4.-set-up-watson-discovery)
 5. [Set up Cloudant database](#5.-set-up-cloudant-database)
 6. [Using Cloud Functions](#6.-using-cloud-functions)
 7. [Run your application](#7.-run-your-application)

## 1. Clone this repo
Clone the repo and change to the directory to where the sample app is located.

```
git clone https://github.com/Penelope1rose/watson-assistant-demo.git

cd watson-assistant-demo 
```

Peruse the files in the *watson-assistant-demo* directory to familiarize yourself with the contents.

## 2. Create an instance of the required services
Please log in to your [IBM Cloud account](https://cloud.ibm.com/login) to do the following.

### Provision a Watson Assistant instance
-   Click  [here](https://cloud.ibm.com/catalog/services/watson-assistant)  to find  **Watson Assistant**  in the IBM Cloud catalog.
- `Select a location`.
-   `Select a pricing plan`. Select  `Trial`.
-   Set your  `Service name`  or use the generated one.
-   Click  **Create**.

### Provision a Watson Discovery instance

-   Click  [here](https://cloud.ibm.com/catalog/services/watson-discovery)  to find  **Watson Discovery**  in the IBM Cloud catalog.
-   Log in to your IBM Cloud account.
- Select the **same location** as your Watson Assistant instance.
-   `Select a pricing plan`. Select  `Lite`.
-   Set your  `Service name`  or use the generated one.
-   Click  **Create**.

### Provision a Cloudant database instance

-   Click  [here](https://cloud.ibm.com/catalog/services/cloudant)  to find  **Cloudant**  in the IBM Cloud catalog.
- Select the **same location** as your Watson Assistant instance.
-   Set your  `Service name`  or use the generated one.
- `Select an authentication method`. Select  `IAM`.
- `Select an environment`. Select  `Multitenant`.
- `Select a pricing plan`. Select  `Lite`.
-   Click  **Create**.

## 3. Set up Watson Assistant
### Create an assistant

- Go to your dashboard and select `Services and software`.

	![dashboard diagram](/images/image1.png)
	
- Find your Watson Assistant service and click on it.
- Click on  `Launch Watson Assistant`.

	![launch service diagram](/images/image2.png)

- Click the  `Assistants`  icon in the left sidebar and then click  `Create assistant`.

	![create assistant diagram](/images/image3.png)

-   Give your assistant a unique name then click  `Create assistant`.

### Add a dialog skill

Import the watson assistant demo skill from a JSON file in your cloned repo. From your Assistant panel:

-   Click on  `Add an action or dialog skill`.
-   Click the  `Upload skill`  tab.
-   Click  `Drag and drop file here or click to select a file`, go to your cloned repo dir, and  `Open`  the JSON file in  `resources/Watson Assistant/watson-assistant-demo-skill.json`.
-   Click the  `Upload`  button.

The newly created dialog skill should now be shown in your Assistant panel:

![assistant diagram](/images/image4.png)

## 4. Set up Watson Discovery

### Add a search skill

> #### What is an Assistant Search Skill?
> 
> An Assistant search skill is a mechanism that allows you to directly query a Watson Discovery collection from your Assistant dialog. A search skill is triggered when the dialog reaches a node that has a search skill enabled. The user query is then passed to the Watson Discovery collection via the search skill, and the results are returned to the dialog for display to the user.
> 
> Click  [here](https://cloud.ibm.com/docs/services/assistant?topic=assistant-skill-search-add)  for more information about the Watson Assistant search skill.

Adding a search skill is optional. Our application uses Watson discovery to query existing company documents or data to see whether any useful information can be found and shared. Using a search skill is preferred because it allows full use of the Assistant preview and WebChat UI.

From your Assistant panel:

-   Click on  `Add search skill`.
-   Give your search skill a unique name, then click  `Continue`.
-   From the search skill panel, select the Discovery service instance.
- Here we have no collections yet. So select `Create new collection`.

	![create collection diagram](/images/image5.png)

- You will be redirected to your Watson Discovery service. Click  `Let's get started`  to continue.

### Upload documents
You have the option to connect to multiple data sources. In this demo, we upload our own documents. 
- Scroll down and select `Upload document(s)`.
- Set your `collection name` and click **Create**.

	![create collection diagram](/images/image6.png)

- Go to your cloned repo directory, and  select all the PDF files in  `resources/Watson Discovery`.
- **Drag and drop** the files into Watson Discovery for ingestion.

This ingestion process will take some time. Once you have uploaded the screen looks like this:

![discovery diagram](/images/image7.png)

### Train documents with SDU
For this step, you can follow this [link](https://www.ibm.com/cloud/garage/dte/tutorial/create-custom-ui-your-watson-assistant/) at _Step 6: Train documents with SDU_.

## 5. Set up Cloudant database
We need to create 2 databases, the **CRM System** and the **Core Banking System** as seen in the architecture flow. For this demo, we will be using Cloudant databases. 

> Note:
> We will be updating information such as credit card limit increase to the Core Banking System database while we will be pulling data from the CRM System of service request details. 

- Go to your IBM Cloud Console resource list, find your Cloudant instance and Launch the dashboard.
- Click on **Create database** on the top right corner

	![create database diagram](/images/image8.png)

- Then create 2 databases as the following:

	|Database Name |Partitioning |
	|:----------------|:---------------|
	| abc-cloudant-db |Non-partitioned |
	| ticket-system |Non-partitioned |

#### Create document in CRM
For this demo, we are going to populate the `ticket-system` database to contain a document. 

- Click on `ticket-system`.
- Click on `Create document`.
- **Copy and paste** the following code into the document.
```
{
  "_id": "cb357405004bb3b92c344c8a85684441",
  "_rev": "3-85ecea3dbc0849a0dc53d0215067bf5b",
  "doc": {
    "caseID": "SR132",
    "name": "Debit Card Stuck In ATM",
    "text": "----- Original message -----\nFrom: banking.support@abc.com\nTo: karen.lim@hotmail.com\nSubject: Debit Card Stuck in ATM\nDate: Thu, Jun 24, 2021 15:29\n\nDear Client,\n\nThe debit card you used to withdraw cash from the ATM machine at Tampines Street 42 has expired. We will send you a replacement card to your registered address in our records through a DHL Courier 233434343. You should receive it within 7-10 working days.\n\nThank you.\n\nShould you require further assistance, kindly contact us at email at banking.support@abc.com\nThank you.\n\n\nBest Regards,\n\nMeera\nCustomer Service Manager\nABC Bank Pte Ltd\n\n----- Original message -----\nFrom: karen.lim@hotmail.com\nTo: banking.support@abc.com\nSubject: Debit Card Stuck in ATM\nDate: Thu, Jun 24, 2021 15:29\n\nHi support,\n\nI have a small problem. I went to an ATM machine at Tampines Street 42 to withdraw money. After a while, the ATM swallowed my debit card. So, my card is stuck in there and I cannot retrieve my card anymore. What happened? Can you please advise on what steps I need to take to resolve this? Thank you.\n\nRegards,\nKaren\n\n\n"
  }
}
```

> This will be the document that Watson Assistant will read from when the user asks about service request details. 

Once this is all done, your cloudant should look like this:

![discovery diagram](/images/image9png)

## 6. Create Actions with Cloud Functions
To integrate Watson Assistant to the Cloudant databases, we use cloud function actions. Watson Assistant's webhook feature will call to this action that will be able to call the Cloudant API and access the database.

This is a more complex way of using Cloud Functions. To learn more about IBM Cloud Functions, follow this [link](https://cloud.ibm.com/functions/).

#### Configure the Cloud CLI
Open your command prompt and navigate to the clone repo directory into the `Watson-Assistant` folder.
```
cd /<path-to-clone-repo>/Watson-Assistant/
```

Login in to your account (follow the prompts)

```
ibmcloud login -sso
```

Target the resource group. 

```
ibmcloud target -g default
```

> If you do not have a resource group, do the following:
> ```ibmcloud resource group create default``` 
> 
> Then try the above step again

Target the organization and space that contains your services (follow the prompts)

```
ibmcloud target --cf
```

#### Deploy the action

Make sure you are in the  `Watson-Assistant`  directory.

Run the following code to create and target a namespace

```
ibmcloud fn namespace create <yourname>-fn
ibmcloud fn namespace target <yourname>-fn
```



## 7. Run the app locally
Install the dependencies listed in the [requirements.txt](https://pip.readthedocs.io/en/stable/user_guide/#requirements-files) file to be able to run the app locally.

  

You can optionally use a [virtual environment](https://packaging.python.org/installing/#creating-and-using-virtual-environments) to avoid having these dependencies clash with those of other Python projects or your operating system.

```

pip install -r requirements.txt

```

  

Run the app.

```

python hello.py

```

  

View your app at: http://localhost:8000

  

## 3. Prepare the app for deployment

  

To deploy to IBM Cloud, it can be helpful to set up a manifest.yml file. One is provided for you with the sample. Take a moment to look at it.

  

The manifest.yml includes basic information about your app, such as the name, how much memory to allocate for each instance and the route. In this manifest.yml **random-route: true** generates a random route for your app to prevent your route from colliding with others. You can replace **random-route: true** with **host: myChosenHostName**, supplying a host name of your choice. [Learn more...](https://console.bluemix.net/docs/manageapps/depapps.html#appmanifest)

```

applications:

- name: GetStartedPython

random-route: true

memory: 128M

```

  

## 4. Deploy the app

  

You can use the Cloud Foundry CLI to deploy apps.

  

Choose your API endpoint

```

cf api <API-endpoint>

```

  

Replace the *API-endpoint* in the command with an API endpoint from the following list.

  

|URL |Region |

|:-------------------------------|:---------------|

| https://api.ng.bluemix.net | US South |

| https://api.eu-de.bluemix.net | Germany |

| https://api.eu-gb.bluemix.net | United Kingdom |

| https://api.au-syd.bluemix.net | Sydney |

  

Login to your IBM Cloud account

  

```

cf login

```

  

From within the *get-started-python* directory push your app to IBM Cloud

```

cf push

```

  

This can take a minute. If there is an error in the deployment process you can use the command `cf logs <Your-App-Name> --recent` to troubleshoot.

  

When deployment completes you should see a message indicating that your app is running. View your app at the URL listed in the output of the push command. You can also issue the

```

cf apps

```

command to view your apps status and see the URL.

  

## 5. Add a database

  

Next, we'll add a NoSQL database to this application and set up the application so that it can run locally and on IBM Cloud.

  

1. Log in to IBM Cloud in your Browser. Browse to the `Dashboard`. Select your application by clicking on its name in the `Name` column.

2. Click on `Connections` then `Connect new`.

2. In the `Data & Analytics` section, select `Cloudant NoSQL DB` and `Create` the service.

3. Select `Restage` when prompted. IBM Cloud will restart your application and provide the database credentials to your application using the `VCAP_SERVICES` environment variable. This environment variable is only available to the application when it is running on IBM Cloud.

  

Environment variables enable you to separate deployment settings from your source code. For example, instead of hardcoding a database password, you can store this in an environment variable which you reference in your source code. [Learn more...](/docs/manageapps/depapps.html#app_env)

  

## 6. Use the database

  

We're now going to update your local code to point to this database. We'll create a json file that will store the credentials for the services the application will use. This file will get used ONLY when the application is running locally. When running in IBM Cloud, the credentials will be read from the VCAP_SERVICES environment variable.

  

1. Create a file called `vcap-local.json` in the `get-started-python` directory with the following content:

```

{

"services": {

"cloudantNoSQLDB": [

{

"credentials": {

"username":"CLOUDANT_DATABASE_USERNAME",

"password":"CLOUDANT_DATABASE_PASSWORD",

"host":"CLOUDANT_DATABASE_HOST"

},

"label": "cloudantNoSQLDB"

}

]

}

}

```

```

  

2. Back in the IBM Cloud UI, select your App -> Connections -> Cloudant -> View Credentials

  

3. Copy and paste the `username`, `password`, and `host` from the credentials to the same fields of the `vcap-local.json` file replacing **CLOUDANT_DATABASE_USERNAME**, **CLOUDANT_DATABASE_PASSWORD**, and **CLOUDANT_DATABASE_URL**.

  

4. Run your application locally.
```
python main.py
```

  

View your app at: http://localhost:8000. Any names you enter into the app will now get added to the database.

  

5. Make any changes you want and re-deploy to IBM Cloud!

```
cf push
```

  

View your app at the URL listed in the output of the push command, for example, *myUrl.mybluemix.net*.

## Run the application

You can either run the notebooks locally or in  [IBM Watson Studio](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/notebooks-parent.html).

-   **Run locally**
    
    1.  Install Jupyter Notebook, see  [Jupyter/IPython Notebook Quick Start Guide](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/install.html)  for more details.
    2.  Download the Jupyter notebooks available in this repository's  [notebook](https://github.com/watson-developer-cloud/assistant-improve-recommendations-notebook/tree/master/notebook)  directory.  **Note: These notebook files are not designed for Watson Studio environment**
    3.  Start jupyter server  `jupyter notebook`
    4.  Follow the instructions in each of the notebooks. Be sure to add your Watson Assistant credentials if necessary.
-   **Run in Watson Studio**
    
    1.  Create a Watson Studio account.  
        Sign up in  [Watson Studio](https://www.ibm.com/cloud/watson-studio), or use an existing account. Lite plan is free to use.
    2.  Create a new project and add a Cloud Object Storage (COS) account.  
        For more information regarding COS plans, see  [Pricing]
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTU2MTcwOTIzOCwxNTAzNjMyNDc2LDE2OD
kxODMyOTYsLTE0MDQ2MTQ5NDQsLTMxNTI2MzExMCwtMTAzMjM4
NDg5NiwyMDEwODY1OTIyLC0xMTgxODg0NzgyLC03NDcwNzU2MT
AsMjA3NzkwOTI1LC00NzI5MDk0ODVdfQ==
-->