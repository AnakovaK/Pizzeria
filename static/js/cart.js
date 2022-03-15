var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function(){
  var pizzaId = this.dataset.pizza
  var action = this.dataset.action

  if (user === 'AnonymousUser') {
      addCookieItem(pizzaId, action)
  }else{
      updateUserOrder(pizzaId, action)
    }
  })
}

function addCookieItem(pizzaId, action) {
  if (action == 'add') {
    if (cart[pizzaId] == undefined) {
      cart[pizzaId] = {'quantity': 1}
  } else {
    cart[pizzaId]['quantity'] += 1
  }
}
  if (action == 'remove') {
    cart[pizzaId]['quantity'] -= 1
    if (cart[pizzaId]['quantity'] <= 0) {
      delete cart[pizzaId]
    }
  }
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}

function updateUserOrder(pizzaId, action) {
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'pizzaId': pizzaId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })
}
