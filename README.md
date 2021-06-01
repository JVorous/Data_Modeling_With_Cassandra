# Data_Modeling_With_Cassandra
<h1>Required libraries</h1>
<ul><li>os</li><li>glob</li><li>csv</li><li>Cassandra Clusters</li><li>prettytable</li><li>cql_queries</li></ul>

<h1>Project</h1>
In this project, you'll apply what you've learned on data 
modeling with Apache Cassandra and complete an ETL pipeline using 
Python. To complete the project, you will need to model your data by 
creating tables in Apache Cassandra to run queries. 

Provide results for the following queries:
<ol>
    <li> Give me the artist, song title and song's length in the music app
          history that was heard during sessionId = 338, and 
          itemInSession = 4</li>
    <li>Give me only the following: name of artist, song 
        (sorted by itemInSession) and user (first and last name) for 
        userid = 10, sessionid = 182</li>
    <li>Give me every user name (first and last) in my music app history 
        who listened to the song 'All Hands Against His Own'</li>
</ol>
<h1>Steps</h1>
<ol>
    <li>Unzip the data.rar file into your project's root directory</li>
    <li>Run main.py -- preps raw .csv files and uses statements from cql_queries.py to create appropriate tables</li>
</ol>

<h1>Notes</h1>
<ul>
  <li>Data files are expected to be in an '/event_data/' sub-folder 
      of your root directory</li>
  <li>This project was set up using a locally installed version of Cassandra</li>
</ul>
