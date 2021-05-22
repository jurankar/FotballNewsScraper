# FotballNewsScraper
Scraping football news and see the corelation with odds.

This projects checks the news regarding football. Currentley only for premier league. When it recieves the news it than compares 
how do these news impact the odds on betting exchanges.


## Guide
1. Algorith will prompt the first question. If we input number 1 in the terminal, we will start capturing data. If we input number 2, we
will analyse all the news and odds, that we already captured.<br><br>
   
2. If we enter number 1, we choose to capture data. A google chrome window will open and the webpage, where we capture the news, 
will load. On that page we use selenium to scrape all the news from the website and store them. We refresh the page every 30 minutes and 
   store any news that we haven't already stored.<br>After we scan the news, we than make an API call to get the current odds for all 
   the matches we are observing and store them. The API call we also make every 30 minutes.<br><br>
   
3. If we enter number 2, we will start analysing news. The algorithm will ask us to input "min-max odds quotient", and from the question it 
is not apparent what does that mean. For each match, we capture odds every 30 minutes for 3 possible outcomes: Team 1 win, draw, Team 2 win. The 
   "min-max odds quotient" tells us, how much did odds change over time for certain outcome for certain match. We get the quotient by dividing the 
   lowest odds we captured with biggest odds we captured. For example if the odds we captured for Manchester United winning on 
   next match are: [1.6, 1.65, 1.8, 1.62, 1.4], we would get a quotient by dividing 1.4/1.8=0.778. <br>
   TIP: If you are not sure what quotient to put, we advise 0.85.<br><br>
   
4. After that the algorithm asks us, if we wish to print every or only key news. If we decide to print only key news, only news that are important 
will be printed, however it is likely that not all important news will be printed.<br><br>
   
5. The algorithm will find the matches, that had "min-max odds quotient" lower or equal to the one we provided. For each match it will draw a graph, 
that shows us the odds for each possible outcome over time. At the same time, we will print all the relevant news to this match in the terminal. 
   After we have examined the graph, we input a character in the console and press enter to show us the graph and the news for the next match.<br><br>
      
6. When we cover all the matches, the algorithm will exit.