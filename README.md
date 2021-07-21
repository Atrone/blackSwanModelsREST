# cryptoInvestmentAdvisor

Now an async aiohttp rest API with one endpoint.

This service was originally made to test and advertise the Google trends crypto investing strategy (total trend / individual trend is proportionate to performace of individual crypto).

So far, it's proven that in a hype market, this strategy beats the simplest one (just buying Bitcoin) by 60% over 3 months.

See: https://cdn.discordapp.com/attachments/692030404248731753/866141098523361310/unknown.png

Now, you can use this service for many things.

It creates trendBuysXXXX.csv that has the amounts (according to trends) of individual cryptos you chose to buy (top 10, bottom 10, etc). (investment advisor)

This also does historical, meaning you can model how well this strategy would've done if you invested every, say, 2 weeks, with it over the past, say, year.

This also compares using trends to not using trends.

This creates csvs of the trends for a given date, the prices for a given date, the hypothetical trend buys on a given date (trendBuysXXXX.csv), and the hypothetical non trend buys on some date
