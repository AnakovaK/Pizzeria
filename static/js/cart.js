var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function(){
  var pizzaId = this.dataset.pizza
  var action = this.dataset.action
  console.log('pizzaId: ', pizzaId, 'action: ', action)
  console.log('USER:', user)

  if (user==='AnonymousUser') {
    console.log('Not logged in')
  }else{
      updateUserOrder(pizzaId, action)
    }
  })
}

function updateUserOrder(pizzaId, action) {
    console.log('User is logged in, sending info...')

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
