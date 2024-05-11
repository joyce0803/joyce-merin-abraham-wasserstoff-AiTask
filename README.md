## RAG-based Query Suggestion Chatbot with Chain of Thought for WordPress Sites 

### Setup Guidlines

1) Access to Wordpress site deployed on Netlify : ( https://663f5b939f93dbd6ae3e237a--musical-concha-221011.netlify.app/ )
   
### OR

2) Access to my WordPress Site on Local : ( https://typical-hands.localsite.io/)
3) Access to Username and Password  when Local Wordpress site is accessed:
 Username : ground
 Password : protective


4) The Wordpress site  and the Chatbot (Flask app)  takes some seconds to load properly.
5) Link to the backend Flask Application hosted on render 
URL : ( https://joyce-merin-abraham-wasserstoff-aitask.onrender.com/ )
NOTE : Only use the WP site to interact with the chatbot. The response to a query will only be displayed if the WP site is accessed as this sends data to the backend. Directly interacting with the flask application will not generate response.

6) Once the Wordpress Site is accessed click on the bottom right chatbot button to trigger the chatbot interface from the Flask API.
7) Users can now ask any question related to the Website.

### Document structure

- faiss_index : Directory to store the vector embeddings

- static : Directory that consists of the static css files (style.css)

- templates : Directory that consists of web pages (chat.html)

- text_data : Directory that store the real time data received from WP Rest APIs (data.json)


- wordpress_plugin/ai-chatbot : Directory that consists of WP plugin files (ai-chatbot.php, ai-chatbot.css, ai-chatbot.js)

- app.py : Main python file that contains all the routes and other chat logic

- generate_embeddings.py : python file that contains functions to create vector embeddings and vector store

- reAct_and_rag.py : python file that contains the functions to create a Reasoning Agent with the help of Google’s Gemini Model and context from the RAG tool.

- requirements.txt  : list of all libraries used in this file.

- text_preprocessing.py : Functions that preprocess the data crawled from WP site.

