   

let mobilePlusListTrigger = document.getElementById('mobile-list-trigger');
let mobileListItem = document.getElementById('mobile-list-item');
mobilePlusListTrigger.addEventListener('click', () => {
    mobileListItem.classList.toggle('mobile-list-active');
})


const openSearch = document.getElementById('openSearch');
const closeSearch = document.getElementById('closeSearch');
const mobileInput = document.getElementById('mobileInput');


openSearch.addEventListener('click', () => {
    mobileInput.classList.toggle('search-input');
    // console.log('clicked')
})
closeSearch.addEventListener('click', () => {
    mobileInput.classList.toggle('search-input');
    // console.log('clicked')
})


const userBtn = document.getElementById('userBtn');
const userContainer = document.getElementById('userContainer'); 

userBtn.addEventListener('click', () =>{
    // console.log('clicked user')
    userContainer.classList.toggle('mobileUserActive');
})


const productBtn = document.getElementById('productBtn');
const productItems = document.getElementById('productItem');
const productBtn1 = document.getElementById('productBtn1');
const productItems1 = document.getElementById('productItem1');

    productBtn.addEventListener('click', () => {
        //console.log('clicked productItem')
        productItems.classList.toggle('product-active')
    });
    productBtn1.addEventListener('click', () => {
        //console.log('clicked productItem')
        productItems1.classList.toggle('product-active')
    });




    //  // AJAX for Add to Cart
    //  document.querySelectorAll('.add-to-cart-form').forEach(form => {
    //     form.addEventListener('submit', function(event) {
    //         event.preventDefault();
    //         const url = this.action;
    //         const formData = new FormData(this);

    //         fetch(url, {
    //             method: 'POST',
    //             body: formData,
    //             headers: {
    //                 'X-Requested-With': 'XMLHttpRequest',
    //                 'X-CSRFToken': formData.get('csrfmiddlewaretoken')
    //             }
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.success) {
    //                 // Display success message
    //                 const messagesDiv = document.getElementById('messages');
    //                 const message = document.createElement('div');
    //                 message.className = 'bg-green-500 text-white p-2 rounded mb-2 flex items-center justify-between';
    //                 message.innerHTML = 'Product added to cart successfully! <i class="fa fa-solid fa-close text-[18px] text-white close-message cursor-pointer ml-2"></i>';
    //                 messagesDiv.appendChild(message);

    //                 // Optionally update the cart summary or other parts of the page
    //             } else {
    //                 alert('Failed to add product to cart.');
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred. Please try again.');
    //         });
    //     });
    // });
    // // Close message
    // document.addEventListener('click', function(event) {
    //     if (event.target.classList.contains('close-message')) {
    //         event.target.parentElement.remove();
    //         // Clear messages from session storage
    //         sessionStorage.removeItem('messages');
    //     }
    // });

    //  // Clear messages on page load
    // window.addEventListener('load', function() {
    //     sessionStorage.removeItem('messages');
    // });


    //   // AJAX for Add to Cart
    //   document.querySelectorAll('.add-to-cart-form').forEach(form => {
    //     form.addEventListener('submit', function(event) {
    //         event.preventDefault();
    //         const url = this.action;
    //         const formData = new FormData(this);

    //         fetch(url, {
    //             method: 'POST',
    //             body: formData,
    //             headers: {
    //                 'X-Requested-With': 'XMLHttpRequest',
    //                 'X-CSRFToken': formData.get('csrfmiddlewaretoken')
    //             }
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.success) {
    //                 // Display success message
    //                 const messagesDiv = document.getElementById('messages');
    //                 const message = document.createElement('div');
    //                 message.className = 'bg-green-500 text-white p-2 rounded mb-2 flex items-center justify-between';
    //                 message.innerHTML = 'Product added to cart successfully! <i class="fa fa-solid fa-close text-[18px] text-white close-message cursor-pointer ml-2"></i>';
    //                 messagesDiv.appendChild(message);

    //                 // Optionally update the cart summary or other parts of the page
    //             } else {
    //                 alert('Failed to add product to cart.');
    //             }
    //         })
    //         .catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred. Please try again.');
    //         });
    //     });
    // });
   

    //  // Clear messages on page load
    // window.addEventListener('load', function() {
    //     sessionStorage.removeItem('messages');
    // });

     // AJAX for updating quantity
    //  document.querySelectorAll('.update-quantity').forEach(button => {
    //     button.addEventListener('click', function(event) {
    //         event.preventDefault();
    //         const url = this.getAttribute('data-url');

    //         fetch(url, {
    //             method: 'POST',
    //             headers: {
    //                 'X-Requested-With': 'XMLHttpRequest',
    //                 'X-CSRFToken': '{{ csrf_token }}'
    //             }
    //         })
    //         .then(response => response.json())
    //         .then(data => {
    //             if (data.success) {
    //                 // Update the quantity
    //                 const quantityElement = this.parentElement.querySelector('p');
    //                 quantityElement.innerText = data.quantity;
                   
    //                 // Update the total price
    //                 document.getElementById('cart-total-price').innerText = `GHS ${data.total_price}`;
    //             } else {
    //                 alert('Failed to update quantity.');
    //             }
    //         })
           
    //         .catch(error => {
    //             console.error('Error:', error);
    //             alert('An error occurred. Please try again.');
    //         });
    //     });
    // });


    // document.addEventListener('DOMContentLoaded', () => {
    //     const addSpecButton = document.createElement('button');
    //     addSpecButton.textContent = 'Add Another Specification';
    //     addSpecButton.type = 'button';
    //     addSpecButton.className = 'add-spec';
        
    //     addSpecButton.addEventListener('click', () => {
    //         const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    //         const currentFormCount = parseInt(totalForms.value);
            
    //         const newForm = document.querySelector('.spec-form').cloneNode(true);
    //         newForm.innerHTML = newForm.innerHTML.replace(/form-(\d+)-/g, `form-${currentFormCount}-`);
    //         document.querySelector('.specifications').appendChild(newForm);
            
    //         totalForms.value = currentFormCount + 1;
    //     });
        
    //     document.querySelector('.specifications').appendChild(addSpecButton);
    // });