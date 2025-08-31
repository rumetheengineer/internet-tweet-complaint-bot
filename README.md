# internet-tweet-complaint-bot
Automated python script to tweet a complaint at my service provider whenever my internet speed drops below a predetermined threshold

Uses [SpeedTest](https://www.speedtest.net/) to check the speed of the internet the system is connected to at the time of execution and compares against a threshold. If the upload or download speed is below the threshold specified in main.py, it will immediately log in to Twitter (the website currently known as X) (sorry to Elon Musk, I am used to calling it twitter already, as such, for a majority of the code I referred to it as twitter as well —feel free to refactor the occurences to X when running the script). If the internet speed is above the threshold it would terminate the code with a print statement.

The Twitter(X) web layout may update so multiple webdriver selectors were used for the tweet box. The thresholds were declared before the class so the values can be changed based on the expected speed of the script runner. My expected speed was 20mbps anything below that and I get noticable lags.

The twitter account to be used and the service provider to be tagged are both declared in the environment file. An environment example has beeen added for clarity. 
