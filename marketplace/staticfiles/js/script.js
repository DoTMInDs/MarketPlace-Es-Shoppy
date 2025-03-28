   

const productBtn = document.getElementById('productBtn');
const productItems = document.getElementById('productItem');
const productBtn1 = document.getElementById('productBtn1');
const productItems1 = document.getElementById('productItem1');

productBtn.addEventListener('click', () => {
    productItems.classList.toggle('product-active')
});
productBtn1.addEventListener('click', () => {
    productItems1.classList.toggle('product-active')
});

