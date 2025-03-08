   


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


// const staticBackdropbtn1 = document.getElementById('staticBackdropbtn1');
// const staticBackdropBtn = document.querySelector('.static-backdrop-btn');
// const staticBackdrop2 = document.getElementById('staticBackdrop2');
// const staticBackdrop4 = document.getElementById('staticBackdrop4');

// staticBackdropbtn1.addEventListener('click', () => {
//     // console.log('clicked user')
//     staticBackdrop2.classList.toggle('backdropActive1');
// });
// staticBackdropBtn.addEventListener('click', () => {
//     console.log('clicked user1')
//     staticBackdrop4.classList.toggle('backdropActive4');
// });
