# <p align="center">Node-red flows crawler and database</p>
<p align="center">This is a tutorial on using Octoparse to crawl Node-RED flows and store them in SQLite.</p>  
<p align="center">For any questions, ask yukunzou@kth.se</p>  

## 1: Crawling Node-red flows: [Octoparse](https://www.octoparse.com/)
### 1.1: Why Octoparse?
-Simple to use  
-Visualization of crawling process  
-Fully qualified for the task of crawling Node-RED flows
### 1.2: Download Octoparse application
**Steps:**  
-Open [Octoparse](https://www.octoparse.com/) website  
-Click "Start a free trial"
-[Sign up](https://identity.octoparse.com/IntersignUp?lang=en-US&returnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DOctoparse%26scope%3Dopenid%2520profile%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.octoparse.com%252Flogin-callback%26nonce%3De_dXVyIm2p5yQoqLf92nUPzxF3TrG3EwLafMkj2KylE%26state%3D1y7e2NScSy855S7oGSe1VincQ-3qvZ-JuYzPoB-TVGI%26registry%3Dtrue%26language%3Den-US%26origin%3Den-US%26language%3Den-US%26client_id%3DOctoparse) for free(Using Google, Microsoft or email)  
-[Download](https://www.octoparse.com/download) for Windows or Mac  
-Open Octoparse application and log in (After opening the app, you need to follow the tutorial and click on a few buttons, then you can enter the Octoparse main interface.)
### 1.3: Import existing crawling task
**General Information:**  
-Configuration file of the crawler task: "Library - Node-RED.otd" located in /Octoparse  
-All problems have been fixed and the crawler task is currently running perfectly  
-You can import this file and run it directly

**Import Steps:**  
-Click "New" on the left side of the Octoparse interface  
-Select "Import Tasks"  
-Click "+ Add File" and select "Library - Node-RED.otd"  
-Click "Confirm", Then open this task and run it by following Section 1.5
### 1.4: A tutorial for creating the crawling task(Reproduce the given task)

Below is some text you will use during the configuration process.  
```
https://flows.nodered.org/search?type=flow&page=1

https://flows.nodered.org/flow/701452d1839b7e433e9eae171113ae35

//ul[@class="nodeTypeList"]

//div[@class="grid thing-list-section main-content"]/div[2]/div[1]/div[4]/a[1]
```

Below is demo gif for tutorial. This gif is even bigger than the video(100MB exceeds the upper limit of compressible gif files), It will take a while to load, if you want to watch the video, check out /lib/tutorial.mp4   

![image](https://github.com/792445363/flow_crawl/blob/main/lib/865652-video1139592532-20230928-183830.gif)  

If you want to learn more, search in [Octoparse's tutorials](https://helpcenter.octoparse.com/hc/en-us).  

### 1.5: Run crawling task and export data to database
**Running Steps:**  
-Open your task from the "Dashboard" interface  
-Select Standard Mode
-Now there is no automatic stop function set for this task. When the number of flows exceeded (this takes about half an hour), click "Stop" 
-Click "Export Data"  
-It will prompt you that there is duplicate data. Click to remove duplicate data. After deduplication, the number of data should be equal to the number of flows on Node-Red  
-Select the export method. I choose to firstly export it to a locally running [MySQL server](https://dev.mysql.com/downloads/mysql/): set the server name to localhost, the port to 3306, and the data encoding to latin1 which is default encoding method in MySQL. After testing the connection, import the specified "source data field" into the corresponding fields in the database. See Section 2 for database field settings.  
-Export data configuration figure:  

![export data](https://github.com/792445363/flow_crawl/blob/main/lib/export%20data.png)  

-Create [SQLite database](https://www.sqlite.org/download.html)  
-Copy the flows table in MySQL to a table in SQLite using [SQLite3 CLI](https://linux.die.net/man/1/sqlite3) or [Navicat free trial](https://www.navicat.com/en/download/navicat-premium)  
-Check data in the table
## 2: Database  
### 2.1: General Information  
-SQLite file locates in /Database  
-There are currently 2566 flows in it. 20230926 20:42 (GMT+2)  
-Data structure:  

| Name        | Type | Size |
|:------------|:----:|-----:|
| name        | TEXT |  254 |
| json        | TEXT |      |  
| github      | TEXT |  254 |
| core_nodes  | TEXT |      |
| other_nodes | TEXT |      |
| tags        | TEXT |  254 |

-Web page issues of several flows:  
In the table, you can see that several flow fields are empty. This is because their web pages are problematic pages, as shown in the figure below. At present, these problem flows have not been dealt with.  

![problem](https://github.com/792445363/flow_crawl/blob/main/lib/problem.png)

The following is a list of flows with problems on the web page.

| Name    |
|:--------|
| uibuilder, VueJS and SVG: Quick floorplan IoT example        |
|    uibuilder dynamic SVG example - no framework needed     |
|    React Node-RED dashboard     |
|     Node Maker    |
|     url-monitoring-probing    |
|      tester-code   |
  
### 2.2: Query for database(About core nodes)  
**Demand 1**: Given core nodes S = {A, B, C} it should return all flows F such that ∀C ∈ F then C ∈ core and C ∈ S.  

**Solution 1**(In Python for example):  
-One example code "flows_query.py" can be found in /Database  
-Connect to SQLite and create cursor object to execute SQL commands:  
```Python
import sqlite3

connection = sqlite3.connect('flows.db')
cursor = connection.cursor()
```
-Query name of flows F
```Python
S = {'debug', 'function', 'mqtt in', 'mqtt out', 'mqtt-broker'}

query = f"SELECT DISTINCT flows.name FROM flows WHERE"
for node in S:
    query += f" core_nodes LIKE '%{node}%' AND"
query = query.rstrip('AND')

cursor.execute(query)
flows = cursor.fetchall()
```  

**Demand 2**:Given a flow F, returns the list of nodes it uses. The returned
information should contain if the node is core or external.  

**Solution 2**(In Python for example):  
-One example code "nodes_query.py" can be found in /Database  
-Connect to SQLite and create cursor object to execute SQL commands as solution 1  
-Query nodes  
```Python
F = "Decimal to Dash"

query = f"SELECT core_nodes, other_nodes FROM flows WHERE name = ?"
cursor.execute(query, (F,))
result = cursor.fetchone()

if result:
    core_nodes = result[0]
    other_nodes = result[1]
```






