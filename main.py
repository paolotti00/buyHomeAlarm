from scrapes_functions import scrape_data

homes = scrape_data()
for home in homes:
    print(vars(home))
    print("---")
