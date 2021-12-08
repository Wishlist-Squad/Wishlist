$(function () {
  // ****************************************
  //  U T I L I T Y   F U N C T I O N S
  // ****************************************

  // Updates the form with data from the response
  function update_form_data(res) {
    $('#wishlist_id').val(res.id)
    $('#wishlist_name').val(res.name)
    $('#wishlist_customer_id').val(res.customer_id)
  }

  function clear_data_fields() {
    $('#wishlist_name').val('')
    $('#wishlist_customer_id').val('')
  }

  function clear_id_field() {
    $('#wishlist_id').val('')
  }

  /// Clears all form fields
  function clear_form_data() {
    clear_data_fields()
    clear_id_field()
  }

  // Updates the flash message area
  function flash_message(message) {
    $('#flash_message').empty()
    $('#flash_message').append(message)
  }

  function isPositiveInteger(s) {
    return /^\+?[1-9][\d]*$/.test(s)
  }

  // ****************************************
  // Create a Wishlist
  // ****************************************

  $('#create-btn').click(function () {
    var name = $('#wishlist_name').val()
    var customer_id = $('#wishlist_customer_id').val()

    if (!isPositiveInteger(customer_id)) {
      flash_message(`Customer ID needs to be a positive integer`)
      return
    }

    var data = {
      name: name,
      customer_id: parseInt(customer_id),
      products: [],
    }

    var ajax = $.ajax({
      type: 'POST',
      url: '/wishlists',
      contentType: 'application/json',
      data: JSON.stringify(data),
    })

    ajax.done(function (res) {
      update_form_data(res)
      flash_message(`Success: wishlist ${res.id} has been created`)
    })

    ajax.fail(function (res) {
      var msg = 'A name and customer id needs to be provided, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  // Update a Wishlist
  // ****************************************

  $('#update-btn').click(function () {
    var wishlist_id = $('#wishlist_id').val()
    var name = $('#wishlist_name').val()
    var customer_id = $('#wishlist_customer_id').val()

    if (!isPositiveInteger(customer_id)) {
      flash_message(`Customer ID needs to be a positive integer`)
      return
    }

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    var data = {
      name: name,
      customer_id: parseInt(customer_id),
      products: [],
    }

    var ajax = $.ajax({
      type: 'PUT',
      url: '/wishlists/' + wishlist_id,
      contentType: 'application/json',
      data: JSON.stringify(data),
    })

    ajax.done(function (res) {
      update_form_data(res)
      flash_message(`Success: wishlist ${wishlist_id} has been updated`)
    })

    ajax.fail(function (res) {
      var msg = 'Make sure a valid wishlist id is given, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  // Retrieve a Wishlist
  // ****************************************

  $('#retrieve-btn').click(function () {
    var wishlist_id = $('#wishlist_id').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    var ajax = $.ajax({
      type: 'GET',
      url: '/wishlists/' + wishlist_id,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      //alert(res.toSource())
      update_form_data(res)
      flash_message(`Success: wishlist ${wishlist_id} has been retrieved`)
    })

    ajax.fail(function (res) {
      clear_data_fields()
      var msg = 'Make sure a valid wishlist id is given, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  // Delete a Wishlist
  // ****************************************

  $('#delete-btn').click(function () {
    var wishlist_id = $('#wishlist_id').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    var ajax = $.ajax({
      type: 'DELETE',
      url: '/wishlists/' + wishlist_id,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      clear_form_data()
      flash_message(
        `Success: Wishlist with id ${wishlist_id} has been Deleted!`
      )
    })

    ajax.fail(function (res) {
      flash_message('Server error!')
    })
  })

  // ****************************************
  // Clear the form
  // ****************************************

  $('#clear-btn').click(function () {
    clear_form_data()
  })

  // ****************************************
  // Search for a Wishlist
  // ****************************************

  $('#search-btn').click(function () {
    // var name = $("#wishlist_name").val();
    var customer_id = $('#wishlist_customer_id').val()

    var queryString = ''

    // if (name) {
    //     queryString += 'name=' + name
    // }
    if (customer_id) {
      if (!isPositiveInteger(customer_id)) {
        flash_message(`Customer ID needs to be a positive integer`)
        return
      }
      if (queryString.length > 0) {
        queryString += '&customer_id=' + customer_id
      } else {
        queryString += 'customer_id=' + customer_id
      }
    }

    var ajax = $.ajax({
      type: 'GET',
      url: '/wishlists?' + queryString,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      //alert(res.toSource())
      console.log(res)
      $('#search_results').empty()
      var table = '<table class="table-striped">'
      var header = `
                <thead>
                    <tr>
                        <th class="col-md-1">ID</th>
                        <th class="col-md-2">Customer ID</th>
                        <th class="col-md-3">Name</th>
                        <th class="col-md-1">Item ID</th>
                        <th class="col-md-2">Product ID</th>
                        <th class="col-md-2">Product Name</th>
                        <th class="col-md-1">Purchased</th>
                    </tr>
                </thead>
            `
      table += header
      body = '<tbody>'
      var firstWishlist = ''
      for (var i = 0; i < res.length; i += 1) {
        var wishlist = res[i]
        var row = '<tr>'
        // append wishlist data
        row += `<td class="col-md-1">${wishlist.id}</td>`
        row += `<td class="col-md-2">${wishlist.customer_id}</td>`
        row += `<td class="col-md-3">${wishlist.name}</td>`
        // append product data
        var padding = ''
        for (var j = 1; j <= 3; ++j) padding += `<td class="col-md-${j}"></td>`
        if (wishlist.products.length === 0) {
          row += padding
          row += `</tr>`
        } else {
          for (var k = 0; k < wishlist.products.length; ++k) {
            if (k > 0) row += `<tr>` + padding
            var product = wishlist.products[k]
            row += `<td class="col-md-1">${product.id}</td>`
            row += `<td class="col-md-2">${product.item_id}</td>`
            row += `<td class="col-md-2">${product.name}</td>`
            row += `<td class="col-md-1">${product.purchased}</td>`
            row += `</tr>`
          }
        }

        body += row
        if (i == 0) {
          firstWishlist = wishlist
        }
      }

      body += '</tbody>'
      table += body
      $('#search_results').append(table)

      // copy the first result to the form
      if (firstWishlist != '') {
        update_form_data(firstWishlist)
      }

      flash_message('Success: searched wishlists')
    })

    ajax.fail(function (res) {
      var msg = 'Make sure a valid customer id is given, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  //  ITEM FUNCTIONS
  // ****************************************

  // ****************************************
  //  U T I L I T Y   F U N C T I O N S
  // ****************************************

  function update_item_form_data(res) {
    $('#item_id').val(res.id)
    $('#item_wishlist_id').val(res.wishlist_id)
    $('#item_item_id').val(res.item_id)
    $('#item_product_name').val(res.name)
    $('#item_purchased').val(res.purchased)
  }

  function clear_item_data_fields() {
    $('#item_wishlist_id').val('')
    $('#item_item_id').val('')
    $('#item_product_name').val('')
    $('#item_purchased').val('')
  }

  function clear_item_id_field() {
    $('#item_id').val('')
  }

  /// Clears all form fields
  function clear_item_form_data() {
    clear_item_data_fields()
    clear_item_id_field()
  }

  // ****************************************
  // Clear the item form
  // ****************************************

  $('#clear-item-btn').click(function () {
    clear_item_form_data()
  })

  // ****************************************
  // Add an Item to a wishlist
  // ****************************************

  $('#create-item-btn').click(function () {
    var wishlist_id = $('#item_wishlist_id').val()
    var item_id = $('#item_item_id').val()
    var name = $('#item_product_name').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    if (!isPositiveInteger(item_id)) {
      flash_message(`Item ID needs to be a positive integer`)
      return
    }
    console.log(`item_id: ${item_id}`)

    var data = {
      wishlist_id: parseInt(wishlist_id),
      item_id: parseInt(item_id),
      name,
      purchased: false,
    }

    var ajax = $.ajax({
      type: 'POST',
      url: `/wishlists/${wishlist_id}/items`,
      contentType: 'application/json',
      data: JSON.stringify(data),
    })

    ajax.done(function (res) {
      update_item_form_data(res)
      flash_message(
        `Success: created a item with id ${res.id} in wishlist ${wishlist_id}`
      )
    })

    ajax.fail(function (res) {
      var msg =
        'You need an item id, product name and valid wishlsit id, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  // Retrieve an Item from a Wishlist
  // ****************************************

  $('#retrieve-item-btn').click(function () {
    var item_id = $('#item_id').val()
    var wishlist_id = $('#item_wishlist_id').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    if (!isPositiveInteger(item_id)) {
      flash_message(`Item ID needs to be a positive integer`)
      return
    }

    var ajax = $.ajax({
      type: 'GET',
      url: `/wishlists/${wishlist_id}/items/${item_id}`,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      //alert(res.toSource())
      update_item_form_data(res)
      flash_message(
        `Success: found item with id ${item_id} in wishlist ${wishlist_id}`
      )
    })

    ajax.fail(function (res) {
      clear_item_data_fields()
      var msg =
        'Make sure you are inputting the item id AND the wishlist id, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  // Search (list) Items in a Wishlist
  // ****************************************

  $('#search-item-btn').click(function () {
    // var name = $("#wishlist_name").val();
    var wishlist_id = $('#item_wishlist_id').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    var ajax = $.ajax({
      type: 'GET',
      url: `/wishlists/${wishlist_id}/items`,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      //alert(res.toSource())
      console.log(res)
      $('#search_results').empty()
      $('#search_results').append(
        '<table class="table-striped" cellpadding="10">'
      )
      var header = '<tr>'
      header += '<th style="width:10%">Item ID</th>'
      header += '<th style="width:30%">Product ID</th>'
      header += '<th style="width:40%">Name</th>'
      header += '<th style="width:20%">Purchased</th>'
      header += '</tr>'
      $('#search_results').append(header)
      var firstItem = ''
      for (var i = 0; i < res.length; i++) {
        var product = res[i]
        var row =
          '<tr><td>' +
          product.id +
          '</td><td>' +
          product.item_id +
          '</td><td>' +
          product.name +
          '</td><td>' +
          product.purchased +
          '</td></tr>'
        $('#search_results').append(row)
        if (i == 0) {
          firstItem = product
        }
      }

      $('#search_results').append('</table>')

      // copy the first result to the form
      if (firstItem != '') {
        update_item_form_data(firstItem)
      }

      flash_message(`Success: found items in wishlist ${wishlist_id}`)
    })

    ajax.fail(function (res) {
      var msg =
        ' A valid wishlist id in the item form needs to be given, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })

  // ****************************************
  // Delete a Item from a Wishlist
  // ****************************************

  $('#delete-item-btn').click(function () {
    var item_id = $('#item_id').val()
    var wishlist_id = $('#item_wishlist_id').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    if (!isPositiveInteger(item_id)) {
      flash_message(`Item ID needs to be a positive integer`)
      return
    }

    var ajax = $.ajax({
      type: 'DELETE',
      url: `/wishlists/${wishlist_id}/items/${item_id}`,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      clear_item_form_data()
      flash_message(
        `Success: Item with ID ${item_id} has been Deleted from Wishlist ${wishlist_id}!`
      )
    })

    ajax.fail(function (res) {
      flash_message('Server error!')
    })
  })

  // ****************************************
  // Purchase an Item in a Wishlist
  // ****************************************

  $('#purchase-item-btn').click(function () {
    var item_id = $('#item_id').val()
    var wishlist_id = $('#item_wishlist_id').val()

    if (!isPositiveInteger(wishlist_id)) {
      flash_message(`Wishlist ID needs to be a positive integer`)
      return
    }

    if (!isPositiveInteger(item_id)) {
      flash_message(`Item ID needs to be a positive integer`)
      return
    }

    var ajax = $.ajax({
      type: 'PUT',
      url: `/wishlists/${wishlist_id}/items/${item_id}/purchase`,
      contentType: 'application/json',
      data: '',
    })

    ajax.done(function (res) {
      update_item_form_data(res)
      flash_message(
        `Success: Item with ID ${item_id} has been Deleted from Wishlist ${wishlist_id}!`
      )
    })

    ajax.fail(function (res) {
      var msg =
        'Make sure you are inputting the item id AND the wishlist id, ERROR: '
      flash_message(msg + res.responseJSON.message)
    })
  })
})
