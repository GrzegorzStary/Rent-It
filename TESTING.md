## HTML Validation

I used the [HTML W3C Validator](https://validator.w3.org) to validate my HTML files.

#### Template syntax:
- Some of the reported errors (e.g., “Bad value {% url ... %} for attribute href” or “Stray doctype”) are not actual code issues. They occur because the validator processes the raw Django template files, which include template tags such as {% load static %} or {% url '...' %}. These tags are not part of standard HTML, so the validator flags them as invalid. Once the templates are rendered by Django, they produce valid HTML output, and those errors disappear.

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
Cause: I use single-line return statements (e.g. if (!errorDiv) return;).
Explanation: This is valid ES6 syntax but JSLint prefers full block statements ({}).
- “Expected ';' and instead saw ','”
Cause: I declare multiple variables in one line (e.g. let stripePublicKey, clientSecret;).
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

- I did not make any changes to settings.py because the warnings are only style-related (long lines, whitespace, inline comment spacing) and do not affect functionality. Since this file controls critical project configuration (database, AWS, Stripe, etc.), modifying it only for PEP8 compliance could introduce unnecessary risks. It is safer to keep the file as it is, since it already works correctly in development and production.

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
-To complete real-world testing, I shared the website with an older user who has only basic computer experience. Their assigned task was to:

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

All pages flagged a contrast issue related to the orange button with white text. While this does not meet standard contrast requirements, the button contains large text and is prominently sized. As it aligns with our established design patterns, we have decided to retain this styling.

| TOOL | Screen |Screenshot | 
| --- | --- | --- | 
| WAVE | Home page | ![screenshot]() |
| WAVE | Our Rooms | ![screenshot]() | 
| WAVE | Contact Us | ![screenshot]() | 
| WAVE | Reviews | ![screenshot]() |
| WAVE | About | ![screenshot]() |
| WAVE | Add Review | ![screenshot]() | 
| WAVE | Logout| ![screenshot]() |

## Manual Testing

I have thoroughly tested each aspect of the website as shown below.

| **Feature**            | **User Action**                       | **Expected Result**                                                                                            | **Pass/Fail** | **Comments** |
| ------------------- | ------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------- | ------------ |
| **Navbar**          |                                       |                                                                                                                |               |              |
|                     | Click on Logo                         | Redirects to the Home page                                                                                     | Pass          |              |
|                     | Click on Home link                    | Redirects to the Home page                                                                                     | Pass          |              |
|                     | Click on Our Room link                | Redirects to the Our Room page                                                                                 | Pass          |              |
|                     | Click on Contact link                 | Redirects to the Contact Form page                                                                             | Pass          |              |
|                     | Click on Reviews link                 | Redirects to the Reviews page                                                                                  | Pass          |              |
|                     | Click on About link                   | Redirects to the About page                                                                                    | Pass          |              |
|                     | Click on Add Review link              | Redirects to the Login page if the user is **not** authenticated; otherwise, redirects to the Add Review page  | Pass          |              |
|                     | Click on My Bookings link             | Redirects to the Login page if the user is **not** authenticated; otherwise, redirects to the My Bookings page | Pass          |              |
|                     | Click on Login link                   | Redirects the user to the Login screen                                                                         | Pass          |              |
|                     | Click on Register link                | Redirects the user to the Registration screen                                                                  | Pass          |              |
|                     | Click on Logout link                  | Redirects the user to a confirmation screen                                                                    | Pass          |              |
| **Footer**          |                                       |                                                                                                                |               |              |
|                     | Click on GITHUB ICON                  | Redirects to the GitHub page, opens in a new tab                                                               | Pass          |              |
|                     | Click on LINKEDIN ICON                | Redirects to the LinkedIn page, opens in a new tab                                                             | Pass          |              |
|                     | Click on FACEBOOK ICON                | Redirects to the Facebook page, opens in a new tab                                                             | Pass          |              |
|                     | Click on INSTAGRAM ICON               | Redirects to the Instagram page, opens in a new tab                                                            | Pass          |              |
| **OUR ROOM BUTTON** |                                       |                                                                                                                |               |              |
|                     | Click on OUR ROOM button              | Redirects to the Our Room page                                                                                 | Pass          |              |
|                     | Scroll to see our rooms               | Page presents a range of room types                                                                            | Pass          |              |
| **BOOK NOW BUTTON** |                                       |                                                                                                                |               |              |
|                     | Click on BOOK NOW button              | Redirects to the booking form                                                                                  | Pass          |              |
|                     | Scroll to see the form                | Form is visible and ready to be filled                                                                         | Pass          |              |
|                     | Click RESERVE button                  | After submitting the form, the user is redirected to My Bookings                                               | Pass          |              |
| **Your Bookings**   |                                       |                                                                                                                |               |              |
|                     | Select a booking from the table       | User selects a booking of interest                                                                             | Pass          |              |
|                     | Click EDIT button                     | User is redirected to the Edit form                                                                            | Pass          |              |
|                     | Update your booking                   | User makes changes and clicks **Update Booking**                                                               | Pass          |              |
|                     | Redirected back to MY BOOKINGS        | User sees the updated booking details                                                                          | Pass          |              |
|                     | Click DELETE                          | User is redirected to the Confirmation page                                                                    | Pass          |              |
|                     | Click CONFIRM button                  | Cancellation confirmed, user is redirected to MY BOOKINGS                                                      | Pass          |              |
|                     | Click BOOK NOW again                  | User can repeat the booking process                                                                            | Pass          |              |
| **Contact**         |                                       |                                                                                                                |               |              |
|                     | Fill the Contact Us form              | Form is filled with valid details                                                                              | Pass          |              |
|                     | Click SEND! button                    | Message is sent, and a confirmation message is shown                                                           | Pass          |              |
| **Registration**    |                                       |                                                                                                                |               |              |
|                     | Input valid email, username, password | Fields are completed correctly                                                                                 | Pass          |              |
|                     | Click Sign-Up button                  | Account is created, user is redirected to the Home page                                                        | Pass          |              |
**Login**           |                                       |                                                                                                                |               |              |
|                     | Click on Login button                 | Form appears; user fills in login credentials                                                                  | Pass          |              |
|                     | Click on Login button again           | Account is logged in                                                                                           | Pass          |              |
| **Logout**          |                                       |                                                                                                                |               |              |
|                     | Click on Logout button                | User is redirected to the confirmation page                                                                    | Pass          |              |
|                     | Click on Logout button again          | Account is logged out                                                                                          | Pass          |              |

## User Stories

Each user story has been fulfilled.

### First-time User

| User Story | Screenshot |
| --- | --- |
| As a first-time user, I want to know where the condo hotel is located. | ![screenshot]() |
| As a first-time user, I want to see room prices and availability. | ![screenshot](documentation/images/user_stories/first_time/first_user2.1.png), ![screenshot]()|
| As a first-time user, I want to understand what experiences and services the condo hotel provides. | ![screenshot](), ![screenshot]() |
| As a first-time user, I want to view real photos of the rooms and facilities. | ![screenshot]() |
| As a first time user, I want to see real peoples reviews. | ![screenshot]() |
| As a first time user I want easly navigate to booking section and create a booking. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |

### Returning User

| User Story | Screenshot |
| --- | --- |
| As a returning user, I want to quickly view the hotel’s location and nearby points of interest. | ![screenshot]() |
| As a returning user, I want an easy way to contact the hotel for questions or updates to my booking. | ![screenshot]()|
| As a returning user, I want to find and follow the condo hotel on social media to stay updated on news and special offers. | ![screenshot]() |
| As a returning user, I want to find my booking. | ![screenshot](), ![screenshot]() |
| As a returning user, I want to edit or delete the booking. | ![screenshot](), ![screenshot]() |
| As a returning user, I want to leave the honest review about my stay. | ![screenshot](), ![screenshot](), ![screenshot]() |

### Site Owner

| User Story | Screenshot |
| --- | --- |
| As the site owner, I want to significantly reduce admin time by making essential information easily accessible on the website. | ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want users to recognize and trust STARY CONDOHOTEL as a reliable and professional accommodation provider. | ![screenshot]()|
| As the site owner, I want users to be able to contact us easily for inquiries, support, or special requests. | ![screenshot]()|
| As the site owner, I want to capture new business opportunities through the contact form and store user data securely. | ![screenshot]() |
| As the site owner, I want users to view high-quality images and videos that accurately represent the rooms, facilities, and surroundings. | ![screenshot](), ![screenshot]() |
| As the site owner, I want users to easily find our location through an interactive map or clear directions. | ![screenshot]() |
| As the site owner, I want to see guests reservations. | ![screenshot]() |
| As the site owner, I want to edit or delete guests reviews. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |
| As the site owner, I want to see messages that potential guests left by using our contact form. | ![screenshot](), ![screenshot](), ![screenshot](), ![screenshot]() |

### BUGS

Throughout the development process, I encountered numerous bugs in my code. While it would be difficult to detail all of them here, I will highlight a few notable examples.

- Reservation Form Validation: Prevented users from selecting a check-in date in the past or a check-out date earlier than the check-in.

- Tab Title Formatting: Standardized tab title structure across all pages by adding a missing " - " (dash and space).
About Page Layout: Corrected a custom CSS class error that caused the button to stick to the footer.

- Form Layout: Fixed a typo that caused the submit button to align left instead of remaining centered.
Responsive Navigation: Repaired a broken Bootstrap link that prevented the hamburger menu from functioning on smaller screens.

- My Booking View Layout: Fixed layout issues for small screens to ensure proper responsiveness.

- 404 Page Display: Resolved an issue that prevented the custom 404 page from displaying correctly.

- Review Template Image: Corrected the image source reference to use the appropriate variable in the review template.

  THERE ARE NO OTHER BUGS I AM AWARE OF

## README

Go back to the [README.md](README.md).
