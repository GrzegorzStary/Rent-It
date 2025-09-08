(function () {

    var pkTag = document.getElementById('id_stripe_public_key');
    var csTag = document.getElementById('id_client_secret');

    if (!pkTag || !csTag) {
        console.error('Stripe JSON script tags not found (id_stripe_public_key / id_client_secret).');
        return;
    }

    var stripePublicKey, clientSecret;
    try {
        stripePublicKey = JSON.parse(pkTag.textContent);
        clientSecret    = JSON.parse(csTag.textContent);
    } catch (e) {
        console.error('Failed to parse Stripe keys from JSON script tags:', e);
        return;
    }

    if (!window.Stripe) {
        console.error('Stripe.js failed to load. Check network blockers or CSP (js.stripe.com).');
        return;
    }

    var stripe = Stripe(stripePublicKey);
    var elements = stripe.elements();

    var style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': { color: '#aab7c4' }
        },
        invalid: { color: '#dc3545', iconColor: '#dc3545' }
    };

    var mountTarget = '#card-element';
    var el = document.querySelector(mountTarget);
    if (!el) {
        console.error('Mount target #card-element not found.');
        return;
    }

    var card = elements.create('card', { style: style });
    card.mount(mountTarget);

    card.on('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (!errorDiv) return;
        if (event.error) {
            errorDiv.innerHTML = `
                <span class="icon" role="alert"><i class="fas fa-times"></i></span>
                <span>${event.error.message}</span>
            `;
        } else {
            errorDiv.textContent = '';
        }
    });

    var form = document.getElementById('payment-form');
    if (!form) {
        console.error('#payment-form not found.');
        return;
    }

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        card.update({ 'disabled': true });
        var submitBtn = document.querySelector('#submit-button');
        if (submitBtn) submitBtn.disabled = true;

        if (window.$) {
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
        }

        var csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
        var saveCheck = document.getElementById('id-save-info');

        var postData = {
            'csrfmiddlewaretoken': csrf ? csrf.value : '',
            'client_secret': clientSecret,
            'save_info': !!(saveCheck && saveCheck.checked),
        };

        var sendCache = window.$
            ? function () { return $.post('/checkout/cache_checkout_data/', postData); }
            : function () {
                return fetch('/checkout/cache_checkout_data/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(postData).toString(),
                    credentials: 'same-origin'
                }).then(function (r) {
                    if (!r.ok) throw new Error('cache_checkout_data failed');
                });
            };

        sendCache().then(function () {
            return stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: (form.full_name || {}).value?.trim(),
                        phone: (form.phone_number || {}).value?.trim(),
                        email: (form.email || {}).value?.trim(),
                        address: {
                            line1: (form.street_address1 || {}).value?.trim(),
                            line2: (form.street_address2 || {}).value?.trim(),
                            city: (form.town_or_city || {}).value?.trim(),
                            country: (form.country || {}).value?.trim(),
                            state: (form.county || {}).value?.trim(),
                        }
                    }
                },
                shipping: {
                    name: (form.full_name || {}).value?.trim(),
                    phone: (form.phone_number || {}).value?.trim(),
                    address: {
                        line1: (form.street_address1 || {}).value?.trim(),
                        line2: (form.street_address2 || {}).value?.trim(),
                        city: (form.town_or_city || {}).value?.trim(),
                        country: (form.country || {}).value?.trim(),
                        postal_code: (form.postcode || {}).value?.trim(),
                        state: (form.county || {}).value?.trim(),
                    }
                },
            });
        }).then(function (result) {
            if (!result) return;
            if (result.error) {
                var errorDiv = document.getElementById('card-errors');
                if (errorDiv) {
                    errorDiv.innerHTML = `
                        <span class="icon" role="alert"><i class="fas fa-times"></i></span>
                        <span>${result.error.message}</span>
                    `;
                }
                if (window.$) {
                    $('#payment-form').fadeToggle(100);
                    $('#loading-overlay').fadeToggle(100);
                }
                card.update({ 'disabled': false });
                if (submitBtn) submitBtn.disabled = false;
            } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }).catch(function (e) {
            console.error(e);
            location.reload();
        });
    });
})();