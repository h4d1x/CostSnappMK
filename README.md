```plaintext
                                 |\    /|
                              ___| \,,/_/
                           ---__/ \/    \
                          __--/     (D)  \
                          _ -/    (_      \
                         // /       \_ /  -\
   __-------_____--___--/           / \_ O o)
  /                                 /   \__/
 /                                 /
||          )                   \_/\
||         /              _      /  |
| |      /--______      ___\    /\  :
| /   __-  - _/   ------    |  |   \ \
 |   -  -   /                | |     \ )
 |  |   -  |                 | )     | |
  | |    | |                 | |    | |
  | |    < |                 | |   |_/
  < |    /__\                <  \
  /__\                       /___\
Boj4ckHoor3man 🐴 
```
🛒 Repository (for now ) : DrinksCost in a Area SnappMK
🚀 What It Does
This Python script uses Selenium to:

Access SnappMarket Express

Select your city and neighborhood

Scrape a list of supermarkets in that area

Crawl each market's Drinks section

Extract product info (name, price, discount, image, etc.)

Save everything to a CSV! ✔️

⚙️ First-Time Setup
1. Install Requirements
```
pip install selenium pandas openpyxl

```

🌐 Browser Setup
✔ Install Microsoft Edge
If not already installed, run this in PowerShell:

```
cd ~\Downloads; Start-BitsTransfer "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?platform=Default&source=EdgeStablePage&Channel=Stable&language=en&brand=M100" .\MicrosoftEdgeSetup.exe; Invoke-Expression .\MicrosoftEdgeSetup.exe

```

✔ Install Microsoft Edge WebDriver
Find your Edge version

Go to:
🔗 WebDriver Downloads

Download & extract the right version


📤 Output
After running, you get:

supermarket_data.xlsx: full product data by sheet

supermarket_data.csv: merged, simplified table for analysis

▶️ Run Example

```
city_name = "تهران"
mahale_name = "محله شهرک اکباتان تهران"
listexcelpath = r"C:\Users\BojackHors3man\...\Supermarkets_list.xlsx"
marketlinks = marketlist2marketlinks(listexcelpath)

extract_supermarket_data(driver, scroll_to_bottom, marketlinks, 'supermarket_data.xlsx', r'C:\Users\BojackHors3man\...\supermarket_data.csv')

```

Boj4ckHoor3man 🐴 — because scraping should be badass, not boring.

