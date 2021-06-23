var updateBtns = document.getElementsByClassName('update-cart')

for (var i=0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productoId = this.dataset.product
        var action = this.dataset.action
        console.log('productoId: ', productoId, ' action: ', action)

        console.log("Usuario: ", user)
        if(user== 'AnonymousUser'){
            addCookieItem(productoId,action)
        } else {
            updateOrderUser(productoId, action)
        }
    })
}

function updateOrderUser(productoId, action){
    console.log('Usuario loggeado, enviando información...')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productoId': productoId,'action':action})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data: ', data)
        location.reload()
    })
}
function addCookieItem(productoId, action){
    console.log('no esta loggeado')

    if (action == 'add'){
        if(cart[productoId] == undefined){
            cart[productoId] = {'cantidad':1}
        } else {
            cart[productoId]['cantidad'] += 1
        }
    }
    if (action == 'remove'){
        cart[productoId]['cantidad'] -=1

        if(cart[productoId]['cantidad'] <= 0){
            console.log('Articulo eliminado')
            delete cart[productoId]
        }
    }
    console.log('Carrito: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}
