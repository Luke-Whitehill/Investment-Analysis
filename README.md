
<h1 align="center">Investment Analysis</h1>

<h2 align = 'center'>
  Introduction
</h2>
<p>
  Scraping and downloading data from Yahoo! each time I made a slight change to some code started to get annoying but it worked for the basic financial analysis I was doing. Then, I wanted to make my own custom indicators and store daily scraping results. That worked for a little while until my computer was asleep when the crontab job was scheduled. I faced a problem; "How do I combine my own data and be able to run cronjobs whenever I liked?"
</p>
<p>
  Answer: Buy a Raspberry Pi and make a local server. I could have gone with a Virtual Private Server (VPS) to allow me to remotely work with my data, but a Raspberry Pi allowed me to be more flexible with any future projects. 
</p>
<p>
  Displaying insights and graphs via a terminal output and a matplotlib graph could be more appealing, so I have started to create a dashboard (which is in the gif below) to tastefully display the data I am collecting, the numbers I am calculating and the models I am fitting.
</p>
<h2>
  Dashboard
</h2>
<p align="center">
  <img src="https://github.com/Luke-Whitehill/Investment-Analysis/blob/master/src/gifs/dashboarddemo.gif" width="1242" height="300/>
</p>
<h3>
  Optimisation of Technical Indicators
</h3>
<p>
  What has not been added to the dashboard yet is optimisation graphs of select technical analysis indicators. Development on the slow stochastics optimisation function has recently begun. For visual aide, graphs have been included for a 3D dimension, two parameter optimisation. However, to tweak all the calculations for the slow stochastic indicator, around 6 variables (dimensions) need to be tested which cannot be shown. 
</p>
<p align="center">
  <img src="https://github.com/Luke-Whitehill/Investment-Analysis/blob/master/src/images/cbastochoptlarge.png" width="550" height="400"/>
</p>
<p>
  The image above shows that for ASX:CBA, if only slow stochastics was to be used as buying and selling signals, the optimum bounds are: buy at 39, sell at 77. This will yield a profit of 20.79 per share (not accounting for slippage or taxes). Whilst this is a strategy that does not beat the market, it is interesting to see that the 'textbook' buy at 20 and sell at 80 does not strictly apply for this equity, and a buy at 35, sell at 75 would be better.
</p>
<p align="center">
  <img src="https://github.com/Luke-Whitehill/Investment-Analysis/blob/master/src/images/cslstochoptlarge.png" width="550" height="400"/>
</p>
<p>
  The figure of ASX:CSL shows a similar story to ASX:CBA, the optimum buy and sell levels for a default slow stochatic indicator is around buying at 30 and selling at 85. Both graphs show that buying equities at a slow stochastic level of ~30 is better. This could be because of the underlying strategy - only have one open position at a time (i.e. not doubling down or short selling) as well as dip buying based on other indicators.
</p>
<p align="center">
  <img src="https://github.com/Luke-Whitehill/Investment-Analysis/blob/master/src/images/fmgstochoptlarge.png" width="550" height="400"/>
</p>
<p>
  ASX:FMG is similar to ASX:CSL and ASX:CBA in the sense that the buy level is around 33 and the sell level is a bit higher at 94. 
</p>
<p>
  Whilst these graphs are largely similar, they show the need for the optimisation of technical analysis indicators and hope that they apply to future results. A contributing factor to these graphs looking similar is that there could be a lot of institutional algorithms eliminating any TA opportunities in these blue chip stocks. Another reason could be that this TA indicator has been used on a medium-long term timeframe and daily data. Using intraday data could yield different results but this optimisation would be a more severe vitcim of overfitting strategies. 
</p>

