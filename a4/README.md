# a4

Summary:

Interested in how NLP on social network conveys customer feedback and supports decision-making, I signed up for Online Social Network Analysis, a graduate course at Illinois Tech. For my final project, I wanted to know the topical opinions toward the iPhone X, so I extracted and evaluated different groups of people’s comments on Twitter. However, there is rate limiting in Twitter so I first designed a method to handle this. If a Twitter request failed, the program would sleep for 15 minutes. Then, I utilized Twitter API to collect Twitter data with the keyword “iPhone X” from some tech people and their friends (i.e., the users they follow). With those data, I generated a NetworkX undirected graph with 2045 nodes and 2128 edges. To prune the unqualified vertices and reduce clutter, I eliminated those nodes that have less than 2 degrees. I got a subgraph with 83 nodes and 167 edges. An effective way of finding communities of vertices in a network is to look for the edges that lie between communities. And removing those edges that exist most frequently between other pairs of nodes contributed to isolated communities. Since the size of the network was relatively small, I decided to use the edge betweenness centrality (Girvan–Newman) algorithm to partition the network into 2 communities, which indicated the affinity of the users. Then, I classified the data along the dimension of sentiment. Due to the previous analysis on the Yelp’s review, initially I would like to use some statistical methods leveraging elements from machine learning like Latent Semantic Analysis, Support Vector Machines or BOW. However, these methods rely on large-scale context and even grammatical dependency. When applied to tweets, which are usually short and riddled with internet slang and emojis, they performed poorly. So, I switched to a dictionary-based sentiment analysis and calculated the score of every single tweet against the AFINN lexicon. The result showed that 48% of the twitters expressed positive emotion, 66% expressed neutral emotion, and 4% expressed negative emotion, meaning, iPhone X's reputation was still very good! I also chose the CEOs of top tech companies like FLAG. Results indicated that 51% of the twitters expressed good emotion, 57% expressed neutral emotion, and 1% expressed bad emotion. The reason why there were fewer negative comments was that the influential people might use some vague words of criticism that could not be detected by our simple sentiment dictionary. Thus, the iPhone advertisement could use social recommendation with a strong tie, according to the community detection result. Moreover, creating the customer profiles with their information and review, especially for certain groups of target consumers, could improve the marketing effectiveness and provide a better experience for consumers.

Description:

This assignment will allow you to do a more open-ended exploration of online social networking. The goal is to let you use some of the tools we've learned in class on your own. There are some requirements to constrain your work, defined below.

To grade your project, I will run the following commands:
```
python collect.py
python cluster.py
python classify.py
python summarize.py
```
So, your a4 folder should have (at least) those four files. **Please check that your files are named correctly, including using lower case letters!!!**

Here is what each script should do:

- `collect.py`: This should collect data used in your analysis. This may mean submitting queries to Twitter or Facebook API, or scraping webpages. The data should be raw and come directly from the original source -- that is, you may not use data that others have already collected and processed for you (e.g., you may not use [SNAP](http://snap.stanford.edu/data/index.html) datasets). Running this script should create a file or files containing the data that you need for the subsequent phases of analysis.
- `cluster.py`: This should read the data collected in the previous steps and use any community detection algorithm to cluster users into communities. You may write any files you need to save the results.
- `classify.py`: This should classify your data along any dimension of your choosing (e.g., sentiment, gender, spam, etc.). You may write any files you need to save the results.
- `summarize.py`: This should read the output of the previous methods to write a textfile called `summary.txt` containing the following entries:
  - Number of users collected:
  - Number of messages collected:
  - Number of communities discovered:
  - Average number of users per community:
  - Number of instances per class found:
  - One example from each class:

Additionally, you should create a plain text file called 'description.txt' that contains a brief summary of what your code does and any conclusions you have made from the analysis (3-5 paragraphs).

Other notes:

- You may use any of the algorithms in scikit-learn, networkx, scipy, numpy, nltk to perform your analysis. You do not need to implement the methods from scratch.
- It is expected that when I run your `collect.py` script, I may get different data than you collected when you tested your code. While the final results of the analysis may differ, your scripts should still work on new datasets.
- You may checkin to Github any configuration or data files that your code needs. For example, if you've used manually annotated training data to fit a classifier, you may store that in Github. However, you should not store large data files (e.g., >50Mb). However, please ensure that your code will run using the commands above. Ensure that you use *relative*, not *absolute* paths when needed. (E.g., don't put "C:/Aron/data" as a path.) I recommend checking that your code works on another system prior to submission.
