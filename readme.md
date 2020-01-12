# IKEA Scraper

## Easily scrape the stock level's of your favourite IKEA Products, all from the comfort of your python shell

### Table of Contents

- [A guide to adding to stores.json](#a-guide-to-adding-to-storesjson)

## A guide to adding to stores.json

1. Go to the website of the IKEA Region of your choice. In this case, [IKEA UK](https://ikea.com/gb/en/)
2. Find a random item. In this case, [BLÅHAJ Soft toy, shark, 100 cm](https://www.ikea.com/gb/en/p/blahaj-soft-toy-shark-30373588/)
3. Find the Stock Checker, this should be a Drop Down box, enter Inspect Element on this Element.
4. Copy the inner data from that Element. It should look something like:

     ```html
         <select class="range-dropdown range-dropdown--with-label" id="new-stockcheck-dropdown">
            <option class="range-dropdown__option--disabled" value="" disabled="">Select a store</option>
            <option value="113">Belfast</option>
            <option value="142">Birmingham</option>
         ...
     </select>
     ```

5. Remove the `<select class="range-dropdown range-dropdown--with-label" id="new-stockcheck-dropdown">
       <option class="range-dropdown__option--disabled">...</option>` and the remaining `</select>` from your copied HTML
6. From here you can manually convert the HTML in to a JSON array by using a tool like Find and Replace in your editor of choice.
    1. Substitute `</option>` for `","`
    2. Substitute `">` for `": "IKEA`
    3. Substitute `<option value="` for nothing.
    4. Make sure to remove the trailing comma from the last entry in your newly converted JSON.
    5. Create a new entry in the `stores.json` file with the country code of the stores country you have just converted.
    6. Paste your converted code in to the new entry. It should look something like this:

        ```json
        {
          "gb": {
              "113": "IKEA Belfast",
              "142": "IKEA Birmingham",
              ...
          },
          ...
        }
        ```

7. Create a new pull request with your updated `stores.json` file.
