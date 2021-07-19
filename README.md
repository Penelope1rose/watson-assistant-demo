
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

![cloudant diagram](/images/image9.png)

## 6. Create Actions with Cloud Functions
To integrate Watson Assistant to the Cloudant databases, we use cloud function actions. Watson Assistant's webhook feature will call to this action that will be able to call the Cloudant API and access the database.

This is a more complex way of using Cloud Functions. To learn more about IBM Cloud Functions, follow this [link](https://cloud.ibm.com/functions/).

#### Configure the Cloud CLI
- Open your command prompt and navigate to the clone repo directory into the `Watson-Assistant` folder.
```
cd /<path-to-clone-repo>/Watson-Assistant/
```

- Login in to your account (follow the prompts)

```
ibmcloud login -sso
```

- Target a resource group. 

```
ibmcloud target -g default
```

> If you do not have a resource group, do the following:
> ```ibmcloud resource group create default``` 
> 
> Then try the above step again

- Target the organization and space that contains your services (follow the prompts)

```
ibmcloud target --cf
```

#### Create the action

Make sure you are in the  `Watson-Assistant`  directory.

- Run the following commands to create and target a namespace.

```
ibmcloud fn namespace create <yourname>-fn
ibmcloud fn namespace target <yourname>-fn
```

- Run the commands below to create an action in Cloud Functions.
```
ibmcloud fn action create wafnaction  --kind python:3 --main main cloud-fn.zip
```

- To see the created action, type the command below:
```
ibmcloud fn action list
```

- Now go to your IBM Cloud Console. Click on the navigation menu on the top left corner, hover over **Functions** and click on `Actions`

![cloud functions action diagram](/images/image10.png)

- On your action, click on `Not enabled` button under `Web action`

![cloud functions action diagram](/images/image11.png)

- Check the `Enable as Web action` box and click **Save**.
- Copy the web action URL. This will be used in Watson Assistant. 

![cloud functions action diagram](/images/image12.png)

### Add URL to Watson Assistant for webhook
> **What is a webhook?**
> Webhook **sends a POST request callout to an external application that performs a programmatic function**. When used in a dialog skill, a webhook is triggered when the assistant processes a node that has a webhook enabled. 
>
We are using webhooks with Cloud Functions for this demo. 

- Go back to your Watson Assistant tooling and click on your dialog skill.
- Click on `Options` > `Webhooks`.
- Paste the web action URL you had copied from Cloud Function and add a `.json` at the end of the URL. 

![cloud functions action diagram](/images/image13.png)

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



<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAxODc2MTMzOCwtMzMxNDE5NzkxLC0xNT
cwNjQxMTA5LC0xNzQxMDgzOTcyLDE1MDM2MzI0NzYsMTY4OTE4
MzI5NiwtMTQwNDYxNDk0NCwtMzE1MjYzMTEwLC0xMDMyMzg0OD
k2LDIwMTA4NjU5MjIsLTExODE4ODQ3ODIsLTc0NzA3NTYxMCwy
MDc3OTA5MjUsLTQ3MjkwOTQ4NV19
-->