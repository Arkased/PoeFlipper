# PoeFlipper
Collection of scripts to calculate profit in buying/turning in div cards and selling the products in Path of Exile.

Horribly outdated, probably doesn't work.

Open the output (out.csv) file in a csv reader (Excel, Google Sheets, etc.).

The two most important numbers to look at are "profitPerTrade" and "yield", as they represent the effective chaos/hour made using this method and the investment capital required respectively. The entries are sorted by a product of these two quantities, though the best options to flip will depend on the specific user.

For those confused by the column headers, I'll breifly explain what they mean. "mean" is the mean price of the div card (in chaos), which wil increase as you buy more cards. "cost" is an estimate of the amount of chaos needed to buy 1 set. "returnId" is the API id of the item yielded by the div card set (you can ignore this). "revenue" is the average cost of the item yielded by the div card set. "profitPerTrade" is the amount of chaos profitted per trade assuming 1 card is purchased at a time, formally defined as "profit" / ("stackSize" + 1). The columns are self-explanatory.

For those not playing softcore on the current challenge league (Blight at the time of writing), you'll need to configure the league name in __utils__.py. You'll need the API name of the league (the "name" field from here https://api.poe.watch/leagues).
