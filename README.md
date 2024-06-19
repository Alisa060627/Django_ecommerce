
## E-commerse website for a makeup store
Created e-commerse website is a platform for customers that want to purchase makeup products online. The website offers a wide range of makeup, skincare products, and perfumes.


## How to run my project

Clone the project

```bash
  git clone https://github.com/Alisa060627/Assignment2_Beztsinna.git 
```
Create virtual environment 

```bash
   python -m venv venv    
```

Start virtual environment

```bash
   .\venv\Scripts\activate    
```

Install dependencies

```bash
  pip install -r requirements.txt 
```
Run server
```bash
  python manage.py runserver
```
Go to

- [http://127.0.0.1:8000/]( http://127.0.0.1:8000/)
To stop the server 
```bash
  'Ctrl+C'
```

## Implemented features

- Search by category 

Once you follow the link in the terminal, you will arrive at the home page of the e-commerce website. Here, you'll find all products listed in the web shop along with two navigation bars. To search products by category, simply click on the name of the desired category located on the bottom navigation bar. This action will direct you to a page displaying items that belong to the selected category.

- Search by the name of the product 

You can perform this search either on the homepage or on the category page. In the top-right corner of the second navigation bar from the top, you will find a search input field. Enter the name of the product you wish to find and click on the magnifier icon. A small window will then appear displaying products that match your search input.

- Investigating product details and adding it to the cart

To view product details, click on the product image or name. This action will redirect you to a page containing all the details about the product. From there, you can add the product to your cart by simply clicking the "Add to cart" button. If you are not logged in, the application will prompt you to go through the authorization process before proceeding further.

- Authorization as admin

For better testing of the application, you should authorize as an admin user with the following credentials:
-  Username: admin
- Password: 19455427

The application will ask you to verify the email. Click on the link that appears in the terminal to verify. Then, press the "Confirm" button to complete the verification process. After this, you will be logged in as an admin user, allowing you to access administrative features of the application.

- Authorization as a simple user

You can also sign up as a new user, but you won't have access to the administration module.

- Shopping cart

After logging in, you can navigate to the product details again and add desired product to your cart. It will redirect you to your cart, but you can also view it by clicking on the cart image in the top right corner of every page on the website. In the shopping cart, you can adjust the quantity of products and proceed to checkout or continue shopping.

- Checkout

If you press the "Move to checkout" button, you will be directed to a form where you need to fill in your details and choose the payment method. Afterward, you can proceed by clicking the "Continue to checkout" button.

- Stripe

Stripe integrations in this application use test keys, ensuring that no actual charges or payments will be processed. For testing purposes, you can use the test card number: 4242 4242 4242 4242, any future expiration date, and any CVC. After completing a simulated transaction, you will receive a message confirming that the order was successful.

- PayPal

PayPal integration are set to Sandbox mode for testing, so no real transactions or payments will be processed. After completing a simulated transaction, you will receive a message confirming that the order was successful.

- Admin features 

To access the Django administration panel, follow this link: http://127.0.0.1:8000/admin/. Once logged in with appropriate credentials, you can perform administrative tasks such as adding new products to the store inventory, managing orders and payments received for orders.
## Testing
I have implemented tests to ensure the correctness of my application's logic. To run these tests, simply execute the following command:
```bash
   pytest   
```





