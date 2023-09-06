const updateButtons = document.querySelectorAll('.update-cart')

updateButtons.forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.dataset.product
        const action = button.dataset.action
        // console.log(productId, action)

        console.log(user)
        if (user === 'AnonymousUser') {
            console.log('User is not authenticated')
        } else {
            updateUserOrder(productId, action)
        }

    })
})

function updateUserOrder(productId, action) {
    console.log('User is authenticated')

    const url = '/update_item/'

    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log(data)
        })
        .catch((error) => {
            console.log(error)
        })
}