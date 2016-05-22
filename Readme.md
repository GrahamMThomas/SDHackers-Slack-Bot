###Slack bot used in SDHackers Slack Channel.###

A Slack Bot with a couple of interesting functions,
as well as some useful ones.

####Installation####
1. Git clone/fork this repo
2. Open SDHackers-Slack-Bot/Txts/magical.txt
3. Enter the correct link
4. cd SDHackers-Slack-Bot
5. Then open hackerbot.js
6. Change main channel variable to your channel id
7. Save and exit
8. Run these commands:

  `nohup python Python/getHackComment.py &`
  
  `nohup python Python/getHackInsult.py &`
  
  `nohup node hackerbot.js <ENTER TOKEN HERE> &`
