Feature: The wishlist service back-end
    As an e-commerce site
    I need a RESTful catalog service
    So that my customers can keep track of the items they want to buy

    Background:
        Given the following wishlists
            | name      | customer_id |
            | christmas | 111         |
            | myself    | 222         |
            | Joey      | 111         |
        And the following items in the wishlists
            | wishlist_index | item_id | product_name  | purchased |
            | 0              | 1       | iphone        | False     |
            | 0              | 2       | Mac Pro       | False     |
            | 1              | 3       | Cat Bed       | False     |
            | 2              | 4       | Monopoly      | False     |
            | 2              | 5       | Ninja Turtles | True      |

    Scenario: The server is running
        When I visit the "Home Page"
        Then I should see "Wishlist RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: Deleting a wishlist
        When I visit the "Home Page"
        And I set "customer_id" to "222"
        And I press the "Search" button
        Then I should see the message "Success Search"
        And I should see "myself" in the "Name" field
        And I should see "222" in the "customer_id" field
        When I copy the "Id" field
        And I press the "Clear" button
        Then the "id" field should be empty
        And the "Name" field should be empty
        And the "customer_id" field should be empty
        When I paste the "Id" field
        And I press the "Delete" button
        Then I should see the message "Success Delete"
        When I paste the "Id" field
        And I press the "Retrieve" button
        Then the "Name" field should be empty

    Scenario: Retrieving a wishlist
        When I visit the "Home Page"
        And I set "customer_id" to "222"
        And I press the "Search" button
        Then I should see the message "Success Search"
        And I should see "myself" in the "Name" field
        When I copy the "Id" field
        And I press the "Clear" button
        Then the "id" field should be empty
        And the "Name" field should be empty
        And the "customer_id" field should be empty
        When I paste the "Id" field
        And I press the "Retrieve" button
        Then I should see the message "Success Retrieve"
        And I should see "222" in the "customer_id" field
        And I should see "myself" in the "name" field

    Scenario: Deleting an item
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see the message "Success Search"
        When I copy the "Id" field
        And I paste the "wishlist_id" field in the item form
        And I set "item_id" to "999" in the item form
        And I set "product_name" to "apple" in the item form
        And I press the "Create" button in the item form
        Then I should see the message "Success Create Item"
        When I store the item id
        And I copy the "wishlist_id" field in the item form
        And I press the "Clear" button in the item form
        Then the "Id" field should be empty in the item form
        And the "wishlist_id" field should be empty in the item form
        And the "item_id" field should be empty in the item form
        And the "product_name" field should be empty in the item form
        And the "purchased" field should be empty in the item form
        When I reference the item id
        And I paste the "wishlist_id" field in the item form
        And I press the "Delete" button in the item form
        Then I should see the message "Success Delete Item"
        When I reference the item id
        And I paste the "wishlist_id" field in the item form
        And I press the "Retrieve" button in the item form
        Then the "item_id" field should be empty in the item form
        And the "product_name" field should be empty in the item form

    Scenario: Adding an Item to a Wishlist
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see the message "Success Search"
        When I copy the "Id" field
        And I paste the "wishlist_id" field in the item form
        And I set "item_id" to "999" in the item form
        And I set "product_name" to "table" in the item form
        And I press the "Create" button in the item form
        Then I should see the message "Success Create Item"
        When I store the item id
        And I copy the "wishlist_id" field in the item form
        And I press the "Clear" button in the item form
        Then the "Id" field should be empty in the item form
        And the "wishlist_id" field should be empty in the item form
        And the "item_id" field should be empty in the item form
        And the "product_name" field should be empty in the item form
        And the "purchased" field should be empty in the item form
        When I reference the item id
        And I paste the "wishlist_id" field in the item form
        And I press the "Retrieve" button in the item form
        Then I should see the message "Success Retrieve Item"
        And I should see "999" in the "item_id" field in the item form
        And I should see "table" in the "product_name" field in the item form

    Scenario: List all wishlists
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see the message "Success Search"
        And I should see "christmas" in the results
        And I should see "Joey" in the results
        And I should see "myself" in the results
        And I should not see "television" in the results

    Scenario: Create a wishlist
        When I visit the "Home Page"
        And I set "Name" to "ThanksGiving"
        And I set "customer_id" to "222"
        And I press the "Create" button
        Then I should see the message "Success Create"
        When I copy the "Id" field
        And I press the "Clear" button
        Then the "Id" field should be empty
        And the "Name" field should be empty
        And the "customer_id" field should be empty
        When I paste the "Id" field
        And I press the "Retrieve" button
        Then I should see the message "Success Retrieve"
        And I should see "ThanksGiving" in the "Name" field

    Scenario: Listing all items in a Wishlist
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see the message "Success Search"
        When I copy the "Id" field
        And I paste the "wishlist_id" field in the item form
        And I press the "Search" button in the item form
        Then I should see the message "Success Search Item"
        Then I should see "1" in the "item_id" field in the item form
        And I should see "iphone" in the "product_name" field in the item form

    Scenario: Update a wishlist
        When I visit the "Home Page"
        And I set "customer_id" to "222"
        And I press the "Search" button
        Then I should see the message "Success Search"
        Then I should see "myself" in the "Name" field
        When I set "Name" to "mySelfnewName"
        And I copy the "Id" field
        And I press the "Update" button
        Then I should see the message "Success Update"
        When I press the "Clear" button
        Then the "Id" field should be empty
        And the "Name" field should be empty
        And the "customer_id" field should be empty
        When I paste the "Id" field
        And I press the "Retrieve" button
        Then I should see the message "Success Retrieve"
        And I should see "mySelfnewName" in the "Name" field

    Scenario: Purchasing an Item in a wishlist
        When I visit the "Home Page"
        And I press the "Search" button
        Then I should see the message "Success Search"
        When I copy the "Id" field
        And I paste the "wishlist_id" field in the item form
        And I press the "Search" button in the item form
        Then I should see the message "Success Search Item"
        And I should see "false" in the "purchased" field in the item form
        When I store the item id
        And I copy the "wishlist_id" field in the item form
        And I press the "Clear" button in the item form
        Then the "Id" field should be empty in the item form
        And the "wishlist_id" field should be empty in the item form
        And the "item_id" field should be empty in the item form
        And the "product_name" field should be empty in the item form
        And the "purchased" field should be empty in the item form
        When I paste the "wishlist_id" field in the item form
        And I reference the item id
        And I press the "Purchase" button in the item form
        Then I should see the message "Success Purchase Item"
        Then I should see "true" in the "purchased" field in the item form
