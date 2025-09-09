(function () {
    const pkTag = document.getElementById('id_stripe_public_key');
    const csTag = document.getElementById('id_client_secret');

    if (!pkTag || !csTag) {
        console.error('Stripe JSON script tags not found.');
        return;
    }

    let stripePublicKey, clientSecret;
    try {
        stripePublicKey = JSON.parse(pkTag.textContent);
        clientSecret = JSON.parse(csTag.textContent);
    } catch (e) {
        console.error('Failed to parse Stripe keys:', e);
        return;
    }

    if (!window.Stripe) {
        console.error('Stripe.js not loaded.');
        return;
    }

    const stripe = Stripe(stripePublicKey);
    const elements = stripe.elements();

    const style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': { color: '#aab7c4' }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };

    const mountTarget = '#card-element';
    const el = document.querySelector(mountTarget);
    if (!el) {
        console.error('Mount target #card-element not found.');
        return;
    }

    const card = elements.create('card', { style: style });
    card.mount(mountTarget);

    card.on('change', function (event) {
        const errorDiv = document.getElementById('card-errors');
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

    const form = document.getElementById('payment-form');
    if (!form) {
        console.error('#payment-form not found.');
        return;
    }

    form.addEventListener('submit', function (ev) {
        ev.preventDefault();

        const submitBtn = document.querySelector('#submit-button');
        card.update({ disabled: true });
        if (submitBtn) submitBtn.disabled = true;

        // Show loading overlay and spinner
        document.body.classList.add('show-spinner');

        // Wait 3 seconds
        setTimeout(() => {
            const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
            const saveCheck = document.getElementById('id-save-info');

            const postData = {
                'csrfmiddlewaretoken': csrf ? csrf.value : '',
                'client_secret': clientSecret,
                'save_info': !!(saveCheck && saveCheck.checked),
            };

            const sendCache = fetch('/checkout/cache_checkout_data/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(postData).toString(),
                credentials: 'same-origin'
            }).then(response => {
                if (!response.ok) throw new Error('cache_checkout_data failed');
            });

            sendCache.then(() => {
                return stripe.confirmCardPayment(clientSecret, {
                    payment_method: {
                        card: card,
                        billing_details: {
                            name: form.full_name?.value?.trim(),
                            phone: form.phone_number?.value?.trim(),
                            email: form.email?.value?.trim(),
                            address: {
                                line1: form.street_address1?.value?.trim(),
                                line2: form.street_address2?.value?.trim(),
                                city: form.town_or_city?.value?.trim(),
                                country: form.country?.value?.trim(),
                                state: form.county?.value?.trim(),
                            }
                        }
                    },
                    shipping: {
                        name: form.full_name?.value?.trim(),
                        phone: form.phone_number?.value?.trim(),
                        address: {
                            line1: form.street_address1?.value?.trim(),
                            line2: form.street_address2?.value?.trim(),
                            city: form.town_or_city?.value?.trim(),
                            country: form.country?.value?.trim(),
                            postal_code: form.postcode?.value?.trim(),
                            state: form.county?.value?.trim(),
                        }
                    },
                });
            }).then(result => {
                if (result.error) {
                    const errorDiv = document.getElementById('card-errors');
                    if (errorDiv) {
                        errorDiv.innerHTML = `
                            <span class="icon" role="alert"><i class="fas fa-times"></i></span>
                            <span>${result.error.message}</span>
                        `;
                    }

                    // Hide overlay/spinner
                    document.body.classList.remove('show-spinner');
                    form.style.opacity = '1';

                    card.update({ disabled: false });
                    if (submitBtn) submitBtn.disabled = false;
                } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }).catch(err => {
                console.error(err);
                location.reload(); // fallback
            });

        }, 3000); // 3s delay
    });
})();
