## HTML Validation

I used the [HTML W3C Validator](https://validator.w3.org) to validate my HTML files.

#### Template syntax:
- Some of the reported errors (“Bad value {% url ... %} for attribute href” or “Stray doctype”) are not actual code issues. They occur because the validator processes the raw Django template files, which include template tags such as {% load static %} or {% url '...' %}. These tags are not part of standard HTML, so the validator flags them as invalid. Once the templates are rendered by Django, they produce valid HTML output, and those errors disappear.

#### Stray elements:
- During validation I did notice one genuine issue - a stray <div> tag - which has now been corrected. After fixing this, no further structural issues were found in the rendered pages.

#### Warnings:
- Some additional warnings remain (such as the recommendation to add lang attributes or metadata improvements). These do not affect functionality but are good practice for accessibility and SEO.
Why the validator complains about Django
The W3C validator expects plain, static HTML. Django templates, however, contain server-side directives ({% ... %} and {{ ... }}) which are only resolved at runtime. To the validator, these look like “illegal characters” or “unknown tags.” For accurate validation, the check must be run on the rendered HTML (the source as delivered by the browser), not on the raw template files.

| Page | Screenshot | Notes |
| --- |--- | --- |
| 403 | ![screenshot](documentation/testing/HTML_VALIDATOR/403.png)| Pass: No Errors |
| 404 | ![screenshot](documentation/testing/HTML_VALIDATOR/404.png)| Pass: No Errors |
| 500 | ![screenshot](documentation/testing/HTML_VALIDATOR/500.png)| Pass: No Errors |
| Base | ![screenshot](documentation/testing/HTML_VALIDATOR/base.png)| Pass: No Errors |
| Checkout Buttons | ![screenshot](documentation/testing/HTML_VALIDATOR/checkout_buttons.png)| Pass: No Errors |
| Checkout Success| ![screenshot](documentation/testing/HTML_VALIDATOR/checkout_success.png)| Pass: No Errors |
| Checkout | ![screenshot](documentation/testing/HTML_VALIDATOR/checkout.png)| Pass: No Errors |
| Create Listing| ![screenshot](documentation/testing/HTML_VALIDATOR/create_listing.png)| Pass: No Errors |
| Delete Item | ![screenshot](documentation/testing/HTML_VALIDATOR/delete_item.png)| Pass: No Errors |
| Duration Form | ![screenshot](documentation/testing/HTML_VALIDATOR/duration_form.png)| Pass: No Errors |
| Edit Item | ![screenshot](documentation/testing/HTML_VALIDATOR/edit_item.png)| Pass: No Errors |
| Edit Profile | ![screenshot](documentation/testing/HTML_VALIDATOR/edit_profile.png)| Pass: No Errors |
| FAQ | ![screenshot](documentation/testing/HTML_VALIDATOR/faq.png)| Pass: No Errors |
| Footer | ![screenshot](documentation/testing/HTML_VALIDATOR/footer.png)| Pass: No Errors |
| Header | ![screenshot](documentation/testing/HTML_VALIDATOR/header.png)| Pass: No Errors |
| Index | ![screenshot](documentation/testing/HTML_VALIDATOR/index.png)| Pass: No Errors |
| Item Detail| ![screenshot](documentation/testing/HTML_VALIDATOR/item_detail.png)| Pass: No Errors |
| Items | ![screenshot](documentation/testing/HTML_VALIDATOR/items.png)| Pass: No Errors |
| Listed Items| ![screenshot](documentation/testing/HTML_VALIDATOR/listed_items.png)| Pass: No Errors |
| Listed Items Warn | ![screenshot](documentation/testing/HTML_VALIDATOR/listed_items1.png)| Continuation |
| Login | ![screenshot](documentation/testing/HTML_VALIDATOR/login.png)| Pass: No Errors |
| Logout | ![screenshot](documentation/testing/HTML_VALIDATOR/logout.png)| Pass: No Errors |
| Mobile Header| ![screenshot](documentation/testing/HTML_VALIDATOR/mobile_header.png)| Pass: No Errors |
| Privacy Policy | ![screenshot](documentation/testing/HTML_VALIDATOR/privacy_policy.png)| Pass: No Errors |
| Product Image | ![screenshot](documentation/testing/HTML_VALIDATOR/product_image.png)| Pass: No Errors |
| Product Info | ![screenshot](documentation/testing/HTML_VALIDATOR/product_info.png)| Pass: No Errors |
| Profile | ![screenshot](documentation/testing/HTML_VALIDATOR/profile.png)| Pass: No Errors |
| Rented Items | ![screenshot](documentation/testing/HTML_VALIDATOR/rented_items.png)| Pass: No Errors |
| Reservation Total| ![screenshot](documentation/testing/HTML_VALIDATOR/reservation_total.png)| Pass: No Errors |
| Reservation | ![screenshot](documentation/testing/HTML_VALIDATOR/reservation.png)| Pass: No Errors |
| Search Results | ![screenshot](documentation/testing/HTML_VALIDATOR/search_results.png)| Pass: No Errors |
| Sign Up | ![screenshot](documentation/testing/HTML_VALIDATOR/signup.png)| Pass: No Errors |
| Terms of Service| ![screenshot](documentation/testing/HTML_VALIDATOR/terms_of_service.png)| Pass: No Errors |

## CSS

I used the [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate my CSS files.

#### GENERAL CSS
![screenshot](documentation/testing/CSS_VALIDATOR/css_general.png)

#### CHECKOUT CSS
![screenshot](documentation/testing/CSS_VALIDATOR/css_checkout.png)

## JavaScript

I have used the [JS LINT](https://www.jslint.com/) to validate my JavaScript files.

### JavaScript - Linting (JSLint)
When running my files through JSLint, a few warnings appeared across files:

- “Expected '{' and instead saw 'return'”
Cause: I use single-line return statements (if (!errorDiv) return;).
Explanation: This is valid ES6 syntax but JSLint prefers full block statements ({}).
- “Expected ';' and instead saw ','”
Cause: I declare multiple variables in one line (let stripePublicKey, clientSecret;).
- Explanation: Valid in ES6+, but JSLint enforces one declaration per line.
“Unexpected ': style'”
- Cause: I pass an object property { style: style } to Stripe Elements.
Explanation: This is correct ES6 object property syntax, but JSLint sometimes flags it.

### Why I kept the code as it is? 
- These warnings are stylistic only, not runtime errors.
- The code executes correctly in all modern browsers.
- They appear because JSLint has stricter/older style rules and limited ES6+ support.

| File | Screenshot | Notes |
| --- | --- | --- |
| Card Index | ![screenshot](documentation/testing/JS_LINTER/card_index.png) | Pass: No Errors |
| Edit Profile | ![screenshot](documentation/testing/JS_LINTER/edit_profile.png) | Pass: No Errors |
| Image Preview | ![screenshot](documentation/testing/JS_LINTER/image_review.png) | Pass: No Errors |
| Item Removal | ![screenshot](documentation/testing/JS_LINTER/item_removal.png) | Pass: No Errors |
| Items List | ![screenshot](documentation/testing/JS_LINTER/items_list.png) | Pass: No Errors |
| Listed Items Toggle | ![screenshot](documentation/testing/JS_LINTER/listed_items_toggle.png) | Pass: No Errors |
| Price Calculator | ![screenshot](documentation/testing/JS_LINTER/price_calculator.png) | Pass: No Errors |
| Stripe | ![screenshot](documentation/testing/JS_LINTER/stripe.png) | Pass: No Errors |
| Tempus Dominus Init | ![screenshot](documentation/testing/JS_LINTER/tempus_dominus_init.png) | Pass: No Errors |
| Tempus Dominus Update | ![screenshot](documentation/testing/JS_LINTER/tempus_dominus_update.png) | Pass: No Errors |

## Python

I have used the [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate my Python files.

### Checkout

| File | Screenshot | Notes |
| --- | --- | --- |
| admin.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/admin.png) | Pass: No Errors |
| apps.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/apps.png) | Pass: No Errors |
| checkout_context.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/checkout_context.png) | Pass: No Errors |
| forms.py| ![screenshot](documentation/testing/PYTHON_LINTER/checkout/forms.png) | Pass: No Errors |
| models.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/models.png) | Pass: No Errors |
| signals.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/signals.png) | Pass: No Errors |
| tests.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/tests.png) | Pass: No Errors |
| urls.py| ![screenshot](documentation/testing/PYTHON_LINTER/checkout/urls.png) | Pass: No Errors |
| views.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/views.png) | Pass: No Errors |
| webhook_handler.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/webhook_handler.png) | Pass: No Errors |
| webhooks.py | ![screenshot](documentation/testing/PYTHON_LINTER/checkout/webhooks.png) | Pass: No Errors |

### Home

| File | Screenshot | Notes |
| --- | --- | --- |
| admin.py | ![screenshot](documentation/testing/PYTHON_LINTER/home/admin.png) | Pass: No Errors |
| apps.py | ![screenshot](documentation/testing/PYTHON_LINTER/home/apps.png) | Pass: No Errors |
| models.py | ![screenshot](documentation/testing/PYTHON_LINTER/home/models.png) | Pass: No Errors |
| tests.py | ![screenshot](documentation/testing/PYTHON_LINTER/home/tests.png) | Pass: No Errors |
| urls.py | ![screenshot](documentation/testing/PYTHON_LINTER/home/urls.png) | Pass: No Errors |
| views.py | ![screenshot](documentation/testing/PYTHON_LINTER/home/views.png) | Pass: No Errors |

### Items

| File | Screenshot | Notes |
| --- | --- | --- |
| admin.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/admin.png) | Pass: No Errors |
| apps.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/apps.png) | Pass: No Errors |
| forms.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/forms.png) | Pass: No Errors |
| models.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/models.png) | Pass: No Errors |
| tests.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/tests.png) | Pass: No Errors |
| urls.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/urls.png) | Pass: No Errors |
| views.py | ![screenshot](documentation/testing/PYTHON_LINTER/items/views.png) | Pass: No Errors |

### Reviews

| File | Screenshot | Notes |
| --- | --- | --- |
| admin.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/admin.png) | Pass: No Errors |
| apps.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/apps.png) | Pass: No Errors |
| forms.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/forms.png) | Pass: No Errors |
| models.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/models.png) | Pass: No Errors |
| testing.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/tests.png) | Pass: No Errors |
| urls.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/urls.png) | Pass: No Errors |
| utils.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/utils.png) | Pass: No Errors |
| views.py | ![screenshot](documentation/testing/PYTHON_LINTER/profiles/views.png) | Pass: No Errors |

### Rent-It

- I did not make any changes to settings.py because the warnings are only style related (long lines, whitespace, inline comment spacing) and do not affect functionality. Since this file controls critical project configuration (database, AWS, Stripe, etc.), modifying it only for PEP8 compliance could introduce unnecessary risks. It is safer to keep the file as it is, since it already works correctly in development and production.

| File | Screenshot | Notes |
| --- | --- | --- |
| asgi.py | ![screenshot](documentation/testing/PYTHON_LINTER/rent_it/asgi.png) | Pass: No Errors |
| settings.py | ![screenshot](documentation/testing/PYTHON_LINTER/rent_it/settings.png) | Pass: No Errors |
| urls.py | ![screenshot](documentation/testing/PYTHON_LINTER/rent_it/urls.png) | Pass: No Errors |
| wsgi.py | ![screenshot](documentation/testing/PYTHON_LINTER/rent_it/wsgi.png) | Pass: No Errors |

### Reservation

| File | Screenshot | Notes |
| --- | --- | --- |
| admin.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/admin.png) | Pass: No Errors |
| apps.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/apps.png) | Pass: No Errors |
| context_processors.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/contect_processors.png) | Pass: No Errors |
| models.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/models.png) | Pass: No Errors |
| tests.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/tests.png) | Pass: No Errors |
| urls.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/urls.png) | Pass: No Errors |
| views.py | ![screenshot](documentation/testing/PYTHON_LINTER/reservation/views.png) | Pass: No Errors |

## Browser Compatability

I have tested my site on different browsers to check for any compatability issues.

#### Firefox & Tor Browser Display Issues

- During testing, the site initially failed to load styles and scripts in Firefox and Tor. This was caused by incorrect Subresource Integrity (SRI) hashes on Bootstrap and Font Awesome CDN links, which Firefox strictly enforces, and by blocked telemetry requests from Stripe.

- Fix: Removed or replaced the broken integrity attributes with correct values, ensuring all resources load over HTTPS. Stripe telemetry errors were confirmed as non critical (payments still work) and documented. After these adjustments, the site displays consistently across Chrome, Safari, Firefox, and Tor.

| Browser | Screenshot | Notes |
| --- | --- | --- |
| Chrome | ![screenshot](documentation/testing/BROWSER_COMPATABILITY/chrome.png) | Works as expected |
| Safari | ![screenshot](documentation/testing/BROWSER_COMPATABILITY/safari.png) | Works as expected |

### ERRORS
| Browser | Screenshot | Notes |
| --- | --- | --- |
| Tor / Firefox | ![screenshot](documentation/testing/BROWSER_COMPATABILITY/tor_err.png) | DISPLAY ERROR |
| Tor / Firefox | ![screenshot](documentation/testing/BROWSER_COMPATABILITY/tor_err2.png) | DISPLAY ERROR |
| Firefox | ![screenshot](documentation/testing/BROWSER_COMPATABILITY/firefox.png) | Works as expected |
| Tor | ![screenshot](documentation/testing/BROWSER_COMPATABILITY/tor.png) | Works as expected |

## Responsiveness

I have tested my site on different devices and screen sizes to check for any responsiveness problems.

### GENERAL RESPONSIVENESS MOBILE (S) - 320px
| Device | Screen |Screenshot | Notes |
| --- | --- | --- | --- |
| Mobile (Devtools)| Home Page | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/home.png) | Works as expected |
| Mobile (Devtools)| Item Detail | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/item_detail.png) | Works as expected |
| Mobile (Devtools)| Rental Bag | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/rental_bag.png) | Works as expected |
| Mobile (Devtools)| Checkout | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/Checkout.png) | Works as expected |
| Mobile (Devtools)| Checkout lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/checkout_lower.png) | Works as expected |
| Mobile (Devtools)| Spinner | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/spinner.png) | Works as expected |
| Mobile (Devtools)| Confirmation | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/confirmation.png) | Works as expected |
| Mobile (Devtools)| Confirmation lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/confirmation_lower.png) | Works as expected |
| Mobile (Devtools)| Rented Items | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/rented_items.png) | Works as expected |
| Mobile (Devtools)| Your Listed Items | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/listed_items.png) | Works as expected |
| Mobile (Devtools)| Create Listing | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/create_listing.png) | Works as expected |
| Mobile (Devtools)| Edit Profile | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/edit_profile.png) | Works as expected |
| Mobile (Devtools)| Edit Profile lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/edit_profile_lower.png) | Works as expected |
| Mobile (Devtools)| Privacy Policy | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/pp.png) | Works as expected |
| Mobile (Devtools)| terms of Service | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/tos.png) | Works as expected |
| Mobile (Devtools)| FAQ | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/faq.png) | Works as expected |
| Mobile (Devtools)| Sign Out| ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/logout.png) | Works as expected |
| Mobile (Devtools)| Filtered Distance Items | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/items.png) | Works as expected |
| Mobile (Devtools)| Filtered Distence Items lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_mobile/items_lower.png) | Works as expected |


### GENERAL RESPONSIVENESS TABLET - 768px
| Device | Screen |Screenshot | Notes |
| --- | --- | --- | --- |
| Tablet (Devtools)| Home Page | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/home.png) | Works as expected |
| Tablet (Devtools)| Item Detail | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/item_detail.png) | Works as expected |
| Tablet (Devtools)| Item Detail Picker | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/item_detail_date.png) | Works as expected |
| Tablet (Devtools)| Item Detail Calc | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/item_detal_calc.png) | Works as expected |
| Tablet (Devtools)| Rental Bag | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/rental_bag.png) | Works as expected |
| Tablet (Devtools)| Checkout | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/checkout.png) | Works as expected |
| Tablet (Devtools)| Checkout lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/checkout_lower.png) | Works as expected |
| Tablet (Devtools)| Spinner | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/spinner.png) | Works as expected |
| Tablet (Devtools)| Confirmation | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/confirmation.png) | Works as expected |
| Tablet (Devtools)| Confirmation lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/confirmation_lower.png) | Works as expected |
| Tablet (Devtools)| Your Rentals | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/your_rentals.png) | Works as expected |
| Tablet (Devtools)| Edit Profile | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/edit_user.png) | Works as expected |
| Tablet (Devtools)| Edit Profile lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/edit_user_lower.png) | Works as expected |
| Tablet (Devtools)| Privacy Policy | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/pp.png) | Works as expected |
| Tablet (Devtools)| Terms of Service | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/tos.png) | Works as expected |
| Tablet (Devtools)| FAQ | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/faq.png) | Works as expected |
| Tablet (Devtools)| Sign Out| ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/logout.png) | Works as expected |
| Tablet (Devtools)| Users Profile | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/users_profile.png) | Works as expected |
| Tablet (Devtools)| Create Listing | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/create_listing.png) | Works as expected |
| Tablet (Devtools)| Create Listing lower | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/create_listing_lower.png) | Works as expected |
| Tablet (Devtools)| Your Listed Items | ![screenshot](documentation/testing/RESPONSIVENESS/general_tablet/your_listing.png) | Works as expected |

### Iphone 13 REAL DEVICE TESTING

| Device | Screen |Screenshot | Notes |
| --- | --- | --- | --- |
| Iphone 13 | Checkout | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/checkout.PNG) | Works as expected |
| Iphone 13| Checkout lower | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/checkout_lower.PNG) | Works as expected |
| Iphone 13| Confirmation | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/confirmation.jpg) | Works as expected |
| Iphone 13| Confirmation lower | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/confirmation_lower.PNG) | Works as expected |
| Iphone 13| Create listing | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/create_listing.PNG) | Works as expected |
| Iphone 13| Create listing lower | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/create_listing_lower.PNG) | Works as expected |
| Iphone 13| Edit profile | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/edit_profile.PNG) | Works as expected |
| Iphone 13| Edit profile lower | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/edit_profile_lower.PNG) | Works as expected |
| Iphone 13| FAQ | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/faq.PNG) | Works as expected |
| Iphone 13| Home | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/home.PNG) | Works as expected |
| Iphone 13| Item detail| ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/item_detail.PNG) | Works as expected |
| Iphone 13| Item detail picker | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/item_detail_picker.PNG) | Works as expected |
| Iphone 13| Item detail calc | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/item_detail_calc.PNG) | Works as expected |
| Iphone 13| Items | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/items.PNG) | Works as expected |
| Iphone 13| Listed Items | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/listed_items.PNG) | Works as expected |
| Iphone 13| Privacy Policy| ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/pp.PNG) | Works as expected |
| Iphone 13| Logout| ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/logout.PNG) | Works as expected |
| Iphone 13| Profile | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/profile.PNG) | Works as expected |
| Iphone 13| Rental bag | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/rental_bag.PNG) | Works as expected |
| Iphone 13| Rental bag lower | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/rental_bag_lower.PNG) | Works as expected |
| Iphone 13| Rented Items | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/rented_items.jpg) | Works as expected |
| Iphone 13| Rented Items | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/rented_items2.jpg) | Works as expected |
| Iphone 13| Spinner | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/spinner.PNG) | Works as expected |
| Iphone 13| Terms of Service | ![screenshot](documentation/testing/RESPONSIVENESS/iphone13/tos.PNG) | Works as expected |

### MACBOOK PRO M3 MAX 16"

| Device | Screen |Screenshot | Notes |
| --- | --- | --- | --- |
| MACBOOK PRO M3 MAX 16" | Checkout | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/checkout.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Checkout lower | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/checkout_lower.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Confirmation | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/confirmation.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Create Listing | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/create_listing.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16" | Delete Item | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/delete_item.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Edit Item | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/edit_item.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Edit Item lower | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/edit_item_lower.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Edit Profile | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/edit_profile.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16" | FAQ | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/faq.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Home | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/home.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Item Detail | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/item_detail.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Item Detail Picker | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/item_detail_picker.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16" | Item Detail Calc | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/item_detail_calc.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Items | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/items.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Listed Items | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/listed_items.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Privacy Policy | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/pp.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Profile | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/profile.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Rental Bag | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/rental_bag.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Rented Items | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/rented_items.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Search | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/search.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Spinner | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/spinner.JPG) | Works as expected |
| MACBOOK PRO M3 MAX 16"| Tos | ![screenshot](documentation/testing/RESPONSIVENESS/macbook_pro/tos.JPG) | Works as expected |

### SAMSUNG TAB A9+

| Device | Screen |Screenshot | Notes |
| --- | --- | --- | --- |
| SAMSUNG TAB A9+ | Checkout | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Checkout.jpg) | Works as expected |
| SAMSUNG TAB A9+| Checkout lower | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Checkout_lower.jpg) | Works as expected |
| SAMSUNG TAB A9+| Confirmation | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Confirmation.jpg) | Works as expected |
| SAMSUNG TAB A9+| Create Listing | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Create_LISTING.jpg) | Works as expected |
| SAMSUNG TAB A9+ | Delete Item | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Delete_item.jpg) | Works as expected |
| SAMSUNG TAB A9+| Edit Item | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Edit_item.jpg) | Works as expected |
| SAMSUNG TAB A9+| Edit Profile | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Edit_profile.jpg) | Works as expected |
| SAMSUNG TAB A9+| Edit Profile lower | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Edit_profile_lower.jpg) | Works as expected |
| SAMSUNG TAB A9+ | FAQ | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Faq.jpg) | Works as expected |
| SAMSUNG TAB A9+| Home | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Home.jpg) | Works as expected |
| SAMSUNG TAB A9+| Item Detail | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Item_detail.jpg) | Works as expected |
| SAMSUNG TAB A9+| Item Detail Picker | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Item_detail_picker.jpg) | Works as expected |
| SAMSUNG TAB A9+ | Item Detail Calc | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Item_detail_calc.jpg) | Works as expected |
| SAMSUNG TAB A9+| Items | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Items.jpg) | Works as expected |
| SAMSUNG TAB A9+| Listed Items | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Your_listing.jpg) | Works as expected |
| SAMSUNG TAB A9+| Privacy Policy | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Pp.jpg) | Works as expected |
| SAMSUNG TAB A9+| Profile | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Your_profile.jpg) | Works as expected |
| SAMSUNG TAB A9+| Rental Bag | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Remtal_bag.jpg) | Works as expected |
| SAMSUNG TAB A9+| Rented Items | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Rented_items.jpg) | Works as expected |
| SAMSUNG TAB A9+| Search | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Search.jpg) | Works as expected |
| SAMSUNG TAB A9+| Spinner | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Spinner.jpg) | Works as expected |
| SAMSUNG TAB A9+| Tos | ![screenshot](documentation/testing/RESPONSIVENESS/samsung_tab_a9_plus/Tos.jpg) | Works as expected |

### Real User Experience Testing. 

Real World Testing - Older User
-To complete real world testing, I shared the website with an older user who has only basic computer experience. Their assigned task was to:

- Create a new account
- Update their profile details
- Find a product to rent
- Proceed through the rental flow up to checkout
- Complete the payment step using a dummy card

### EXTRA – User Did Not Understand English

![photo](documentation/testing/REAL_USER_TESTING/person1/1.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/2.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/3.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/4.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/5.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/6.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/7.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/8.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/9.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/10.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/11.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/12.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person1/13.png)

### Second Tester

The second person who tested the website was my wife. I gave her a simple end-to-end task to verify the core rental flow:

- Find a product
- Select rental dates
- Confirm that the calculated price was correct
- Navigate to the checkout page
- Complete the payment process

- Next Task - Profile & Rentals

The next task for my wife was to log into her profile and test the user account features:

- Access the profile dashboard
- Manage her own product listing visibility (toggle between visible/hidden)
- Check her active rentals
- Verify the rental details, including the location where she would need to go to pick up the item.

![photo](documentation/testing/REAL_USER_TESTING/person2/1.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/2.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/3.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/4.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/5.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/6.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/7.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/8.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/9.JPG)
![photo](documentation/testing/REAL_USER_TESTING/person2/10.png)

## Lighthouse

I've tested my deployed project using the Lighthouse tool to check for issues.

- During testing with performance and best practice auditing tools the overall Best Practice score was slightly reduced across all pages. 
This is caused by third-party cookies automatically injected by Stripe.
These cookies are essential for secure payment functionality and are beyond the control of the application. 
No action is required on the project side, and this behaviour is expected when integrating Stripe.

- The performance score was slightly reduced across several pages due to the use of large image files (particularly product images). While these images display correctly and maintain good visual quality, they increase page load times and impact Lighthouse performance results.

| Page | Size | Screenshot | Notes |
| --- | --- | --- | --- |
| Home | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/home.png) | Lower performance due to large images |
| Items | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/item.png) | n/a |
| Item detail| Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/item_detail.png) | n/a |
| Rental bag | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/rental_bag.png) | n/a |
| Rented Items | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/rented_items.png) | n/a |
| Checkout | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/checkout.png) | n/a |
| Listed Items | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/listed_items.png) | n/a |
| Profile | Desktop | ![screenshot](documentation/testing/LIGHTHOUSE/profile.png) | n/a |



## WAVE EVALUATION

I tested my deployed project using the WAVE evaluation tool to assess accessibility.

- Accessibility testing flagged minor contrast issues in the footer links (FAQ, Privacy Policy, Terms of Service). 
While these links technically fall below the recommended WCAG contrast ratio, they remain legible due to the surrounding design, consistent font size, and clear spacing. As this colour scheme aligns with the established Rent-It branding, the decision was made to retain this styling.

#### On the positive side, Rent-It places a strong emphasis on inclusivity:

- The site is massively ARIA-labelled, ensuring screen readers can interpret and announce elements correctly.
Key interactive components (buttons, forms, navigation) have aria-labels and role attributes for improved accessibility.

#### This means that even users with disabilities can successfully navigate and benefit from the platform - from browsing items to listing items and completing the checkout flow, potentially improving their living standard due to extra income stream.

| TOOL | Screen |Screenshot | 
| --- | --- | --- | 
| WAVE | Home | ![screenshot](documentation/testing/WAVE_EVALUATION/home.png) |
| WAVE | Items | ![screenshot](documentation/testing/WAVE_EVALUATION/items.png) | 
| WAVE | Item detail | ![screenshot](documentation/testing/WAVE_EVALUATION/item_detail.png) | 
| WAVE | Rental bag | ![screenshot](documentation/testing/WAVE_EVALUATION/rental_bag.png) |
| WAVE | Checkout | ![screenshot](documentation/testing/WAVE_EVALUATION/checkout.png) |
| WAVE | Checkout error | ![screenshot](documentation/testing/WAVE_EVALUATION/checkout_err.png) | 
| WAVE | Confirmation| ![screenshot](documentation/testing/WAVE_EVALUATION/confirmation.png) |
| WAVE | Edit profile | ![screenshot](documentation/testing/WAVE_EVALUATION/edit_profile.png) |
| WAVE | Create listing | ![screenshot](documentation/testing/WAVE_EVALUATION/create_listing.png) |
| WAVE | Your listing | ![screenshot](documentation/testing/WAVE_EVALUATION/your_listing.png) | 
| WAVE | Your Rentals| ![screenshot](documentation/testing/WAVE_EVALUATION/your_rentals.png) |

## Manual Testing

| **Feature** | **User Action** | **Expected Result** | **Pass/Fail** | **Comments** |
|-------------|-----------------|---------------------|---------------|--------------|
| **Navbar – Home** | Click "Rent-It" logo or Home link | Redirects to home page | Pass | Works as expected |
| **Navbar – Browse Items** | Click link | Opens items listing page | Pass | Shows item cards with images, name, price |
| **Navbar – My Items** | Click link | Shows user’s listed items | Pass | Displays items with edit/delete options |
| **Navbar – My Reservations** | Click link | Shows user’s reservations | Pass | Displays bookings with correct details |
| **Navbar – Profile** | Click link | Opens profile page | Pass | Info editable |
| **Navbar – Logout** | Click logout | Logs out user | Pass | Redirects to homepage |
| **Footer Links** | Click Terms/Privacy/FAQ | Opens correct page | Pass | Minor contrast issues |
| **Home Page Load** | Visit | Hero with search form | Pass | Loads search fields for tool, location, date |
| **Search Tools** | Enter keyword and submit | Shows filtered results | Pass | Returns relevant items |
| **Filter by Category** | Select category | Results update | Pass | Items narrowed correctly |
| **Location Filter** | Search by location | Filters results nearby | Pass | Map pins correct |
| **Items Map** | View map on results | Pins show item locations | Pass | Clickable markers, works with Google Maps |
| **Item Detail** | Open an item page | Shows description, price, owner | Pass | Clean layout with details |
| **Date Picker** | Select start/end dates | Valid dates accepted | Pass | Prevents invalid ranges |
| **Reserve Item** | Click Reserve after dates | Goes to Stripe checkout | Pass | Stripe checkout loads securely |
| **Stripe Payment** | Pay with test card | Booking confirmed | Pass | Appears in My Reservations |
| **Profile – View/Edit** | Change name/address | Saves changes | Pass | Updates persist |
| **My Items – Edit** | Edit listing | Updates item | Pass | Reflected in listings |
| **My Items – Delete** | Delete listing | Should remove everywhere | Pass | Note: Remains in browse until refresh |
| **Add Item** | Submit new item with image | Creates listing | Pass | Tags worked |
| **Add Item – Validation** | Leave fields empty | Shows error | Pass | Proper error messages |
| **Contact Form** | Submit valid form | Sends message | Pass | Confirmation shown |
| **Contact Form – Validation** | Leave blank/invalid email | Shows error | Pass | Inline validation works |
| **Responsive Layout** | Test on mobile | Navbar collapses, no scroll | Pass | Works as expected |
| **Accessibility – Alt Text** | Inspect images/icons | All should have alt | Pass | Works as expected |
| **Accessibility – Form Labels** | Check login form | Inputs should be labeled | Pass | Works as expected |
| **Accessibility – Keyboard Nav** | Tab through site | All reachable | Pass | Focus visible, minor datepicker issue |
| **Auth – Register** | Sign up with email | Account created | Pass | Works, password rules enforced |
| **Auth – Duplicate** | Register same email | Should error | Pass | Shows “Email already registered” |
| **Auth – Login** | Valid credentials | Logs in | Pass | User greeted by name |
| **Auth – Wrong PW** | Invalid login | Error shown | Pass | Proper feedback |
| **Auth – Google Login** | OAuth with Google | Should log in | Pass | Works as expected |
| **Auth – GitHub Login** | OAuth with GitHub | Logs in | Pass | Worked as expected |

### Postcodes.io Testing
The Postcodes.io API powers the location based search in Rent-It. To ensure the feature worked correctly, I carried out the following manual and functional tests:

| **Test**                                     | **User Action**                                           | **Expected Result**                                                          | **Pass/Fail** | **Comments**                               |
| -------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------- | ------------------------------------------ |
| Enter a valid UK postcode (`SW1A 1AA`) | User searches for items with a valid postcode             | API returns correct latitude/longitude, items displayed within chosen radius | Pass          | Verified against Google Maps for accuracy  |
| Enter an invalid postcode (`ZZ99 9ZZ`) | User enters invalid postcode                              | API returns error, system displays validation message                        | Pass          | Error handled gracefully with feedback     |
| Leave postcode field empty                   | User submits search without postcode                      | No API call is made, system prompts for valid postcode                       | Pass          | Prevented unnecessary API calls            |
| Change search radius (5, 10, 25 km)       | User adjusts distance filter                              | Items displayed update correctly based on Haversine calculation              | Pass          | Checked against known distances            |
| Compare distance results manually            | Measured distance between two postcodes using Google Maps | Distances calculated by Rent-It closely match Google Maps distances          | Pass          | Confirms Haversine + Postcodes.io accuracy |


## User Stories

Each user story has been fulfilled.

| User Story | Screenshot |
| --- | --- |
| As a renter, I want to see total price including deposit, so I know the full cost.| ![screenshot](documentation/testing/USER_STORIES/renter_stories/1/1.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/1/2.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/1/3.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/1/4.png) |
| As a renter, I want to pay securely via Stripe, so I can complete my booking.| ![screenshot](documentation/testing/USER_STORIES/renter_stories/2/5.png), ![screenshot](documentation/testing/USER_STORIES/renter_stories/2/6.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/2/7.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/2/8.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/2/9.png) |
| As a user, I want to search by keyword and location, so I can find items near me. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/1/1.png), ![screenshot](documentation/testing/USER_STORIES/renter_stories/3/13.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/3/10.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/3/12.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/3/11.png)|
| As a user, I want to upload images for my listing, so that others can see what they’re renting. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/4/14.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/4/15.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/4/16.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/4/17.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/4/18.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/4/19.png)|
| As a user, I want to set a rental price per day, so I can earn income from my item. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/5/20.png) |
| As a renter, I want to choose rental dates, so I can reserve the item I want. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/1/3.png) |
| As a renter, I want to see my active and past rentals, so I can track my history. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/6/21.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/6/22.png)|
| As a user, I want to edit my profile info, so that I can update contact details or location. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/7/23.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/7/24.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/7/25.png)|
| As a user, I want to reset my password, so that I can recover account access. | ![screenshot](documentation/testing/USER_STORIES/renter_stories/8/26.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/8/27.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/8/28.png) ![screenshot](documentation/testing/USER_STORIES/renter_stories/8/29.png)|
| As a user, I want to browse listings by category, so I can find what I need easily. | ![screenshot](), ![screenshot]() |
| As a user, I want to view an item detail page, so I can learn more before renting. | ![screenshot](), ![screenshot]() |
| As a user, I want to sign up and log in, so that I can access my account. | ![screenshot](), ![screenshot](), ![screenshot]() |
| As a user, I want to list an item for rent, so that others can view and book it. | ![screenshot](), ![screenshot](), ![screenshot]() |
| As a user, I want to set a security deposit, so I can reduce the risk of damage. | ![screenshot](), ![screenshot](), ![screenshot]() |
| As a user, I want to receive email confirmations, so I know when bookings are made. | ![screenshot](), ![screenshot](), ![screenshot]() |

### Site Owner

| User Story | Screenshot |
| --- | --- |
| As an owner, I want to see all rentals for my listed items, so I can prepare item. | ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to show personalised dashboards, so users can manage their activity easily. | ![screenshot]()|
| As the site owner, I want to provide a clear and accessible FAQ and Terms & Conditions page, so that users understand their responsibilities and avoid misunderstandings. | ![screenshot]()|
| As the site owner, I want to delete inappropriate listings, so the site stays safe. | ![screenshot]() |
| As the site owner, I want to limit duplicate or spam accounts, so that the community remains safe and trustworthy. | ![screenshot](), ![screenshot]() |
| As the site owner, I want to support a wide variety of item types and categories, so that the platform appeals to diverse users. | ![screenshot]() |
| As the site owner, I want to ensure secure user authentication, so that only verified users can list or rent items. | ![screenshot]() |
| As the site owner, I want to moderate listings, so that I can remove inappropriate or fraudulent content from the platform. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to collect rental commissions via Stripe, so that I can generate revenue from the platform. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to allow users to browse listings without logging in, so that casual visitors are more likely to sign up. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to send automatic email confirmations, so users are informed about bookings and payments. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to store images on AWS S3, so media loads fast and doesn't slow down the server. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to make the site mobile-friendly, so users can browse and book rentals on the go. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |

### Notable Bugs and Problems Encountered

Throughout the development of Rent-It, a wide range of bugs were identified and fixed. While it is impossible to list them all, the most interesting and challenging ones included:

- **Stripe Card Element Not Rendering:**  
  At one stage the Stripe card input failed to load, showing `ERR_CONNECTION_REFUSED`. This was traced to a browser/network issue blocking Stripe’s CDN. Switching script sources and cleaning up the Stripe integration resolved it.

- **Session Data & Checkout Totals:**  
  Checkout initially only displayed one item with incorrect totals. The issue was caused by how session data was populated in the reservation views. Adjustments were made to ensure multiple items and deposits calculated correctly.

- **Image Carousel Bugs:**  
  Product image carousels sometimes displayed incorrectly (only working on mobile but not on desktop, or Safari scaling problems). Fixes included unique carousel IDs per item and refined CSS (object-fit, aspect-ratio) to ensure consistent display.

- **Template Context Errors:**  
  Emails to item owners originally failed with `VariableDoesNotExist` because the template expected `item.product` while only `product` was passed in context. Updating templates to use the correct variables fixed the issue.

- **Profile Validation Gaps:**  
  Profile editing allowed blank required fields (like last name). Additional validation was added to enforce proper data integrity.

- **OAuth Social Login:**  
  While GitHub logins worked, Google login returned errors due to a misconfigured redirect URI. This highlighted the importance of correct OAuth setup across providers.

- **Static & Media on AWS:**  
  Setting up AWS S3 and linking with Heroku caused multiple issues with permissions and missing files. Correct bucket configuration (ACLs, policies, static/media separation) resolved this.

- **Accessibility and Contrast Warnings:**  
  Automated audits flagged low-contrast footer links and missing ARIA labels. While some design choices were kept for branding, ARIA labeling was improved to make the site screen reader friendly.

These challenges helped shape Rent-It into a more stable and user friendly application. 
Each bug provided valuable learning, particularly around 
**session handling, third-party integrations (Stripe, AWS, OAuth), and accessibility best practices**.

  THERE ARE NO OTHER BUGS I AM AWARE OF

## README

Go back to the [README.md](README.md).
