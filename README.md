# LeetCode Scraper & Displayer

## Scrape
You can join [this discord](https://discord.gg/cscareers) and then go to the `leetcode-bot` channel and type `!problems <company>` for a particular company, or `!problem companies` to see which companies have available data.

Grab the entry and add it as a text file to the `inputs/` folder. Then, it will use Selenium to scrape through LeetCode.

### NOTE:
If you want to run additional problems through the scraper, you need to set up a web-driver. Personally, I just do `brew install chromedriver` and `brew upgrade chromedriver` when my browser doesn't match the current version. You can use Mozilla's [geckodriver](https://github.com/mozilla/geckodriver/releases). There are lots of online resources for doing web-scraping, so don't post an issue here.

## Display
```
> ./leetcode.py --help
usage: leetcode.py [-h] [-c {amazon,google,twitch,salesforce,facebook,microsoft}] [-d {any,easy,medium,hard}] [-n NUM]

optional arguments:
  -h, --help            show this help message and exit
  -c {amazon,google,twitch,salesforce,facebook,microsoft}, --company {amazon,google,twitch,salesforce,facebook,microsoft}
  -d {any,easy,medium,hard}, --difficulty {any,easy,medium,hard}
  -n NUM, --num NUM     show at most this many problems


> ./leetcode.py -c microsoft -d easy -n 5
                              title difficulty  times                                                            link
1   Sign of the Product of an Array       easy     76  https://leetcode.com/problems/sign-of-the-product-of-an-array/
9                    Design HashMap       easy     18                   https://leetcode.com/problems/design-hashmap/
12                 Maximum Subarray       easy     13                 https://leetcode.com/problems/maximum-subarray/
17                        Min Stack       easy     11                        https://leetcode.com/problems/min-stack/
21               Merge Sorted Array       easy     11               https://leetcode.com/problems/merge-sorted-array/
 ```
