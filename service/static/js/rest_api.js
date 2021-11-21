$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#wishlist_id").val(res.id);
        $("#wishlist_name").val(res.name);
        $("#wishlist_customer_id").val(res.customer_id);
    }

    function clear_data_fields() {
        $("#wishlist_name").val("");
        $("#wishlist_customer_id").val("");
    }

    function clear_id_field() {
        $("#wishlist_id").val("");
    }

    /// Clears all form fields
    function clear_form_data() {
        clear_data_fields();
        clear_id_field();
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Wishlist
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#wishlist_name").val();
        var customer_id = $("#wishlist_customer_id").val();

        var data = {
            "name": name,
            "customer_id": customer_id,
            "products": []
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/wishlists",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Wishlist
    // ****************************************

    $("#update-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();
        var name = $("#wishlist_name").val();
        var customer_id = $("#wishlist_customer_id").val();

        var data = {
            "name": name,
            "customer_id": customer_id,
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/wishlists/" + wishlist_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Wishlist
    // ****************************************

    $("#retrieve-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists/" + wishlist_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_data_fields();
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Wishlist
    // ****************************************

    $("#delete-btn").click(function () {

        var wishlist_id = $("#wishlist_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/wishlists/" + wishlist_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Wishlist has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data()
    });

    // ****************************************
    // Search for a Wishlist
    // ****************************************

    $("#search-btn").click(function () {

        // var name = $("#wishlist_name").val();
        var customer_id = $("#wishlist_customer_id").val();

        var queryString = ""

        // if (name) {
        //     queryString += 'name=' + name
        // }
        if (customer_id) {
            if (queryString.length > 0) {
                queryString += '&customer_id=' + customer_id
            } else {
                queryString += 'customer_id=' + customer_id
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/wishlists?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            console.log(res)
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Customer ID</th>'
            header += '</tr>'
            $("#search_results").append(header);
            var firstWishlist = "";
            for(var i = 0; i < res.length; i++) {
                var wishlist = res[i];
                var row = "<tr><td>"+wishlist.id+"</td><td>"+wishlist.name+"</td><td>"+wishlist.customer_id+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstWishlist = wishlist;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstWishlist != "") {
                update_form_data(firstWishlist)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    //  ITEM FUNCTIONS
    // ****************************************

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    function update_item_form_data(res) {
        $("#item_id").val(res.id);
        $("#item_wishlist_id").val(res.wishlist_id);
        $("#product_id").val(res.product_id);
        $("#product_name").val(res.name);
    }

    function clear_item_data_fields() {
        $("#item_wishlist_id").val("");
        $("#product_id").val("");
        $("#product_name").val("");
    }

    function clear_item_id_field() {
        $("#item_id").val("");
    }

    /// Clears all form fields
    function clear_item_form_data() {
        clear_item_data_fields();
        clear_item_id_field();
    }

    // ****************************************
    // Clear the item form
    // ****************************************

    $("#clear-item-btn").click(function () {
        clear_item_form_data()
    });

    // ****************************************
    // Add an Item to a wishlist
    // ****************************************

    $("#create-item-btn").click(function () {
        console.log("adding an item")

        var wishlist_id = $("#item_wishlist_id").val();
        var product_id = $("#product_id").val();
        var name = $("#product_name").val();

        var data = {
            wishlist_id,
            product_id,
            name,
            purchased: false
        };

        var ajax = $.ajax({
            type: "POST",
            url: `/wishlists/${wishlist_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            var msg = "You need a product id, product name and valid wishlsit id, ERROR: "
            flash_message(msg + res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve an Item from a Wishlist
    // ****************************************

    $("#retrieve-item-btn").click(function () {

        var item_id = $("#item_id").val();
        var wishlist_id = $("#item_wishlist_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: `/wishlists/${wishlist_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_item_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_item_data_fields();
            var msg = "Make sure you are inputting the item id AND the wishlist id, ERROR: "
            flash_message(msg + res.responseJSON.message)
        });

    });

})
