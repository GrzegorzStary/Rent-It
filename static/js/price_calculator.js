document.addEventListener("DOMContentLoaded", () => {
    console.log("Price calculator JS loaded (Tempus Dominus)");

    const today = new Date();
    today.setHours(0, 0, 0, 0); // Remove time component

    const priceData = document.getElementById("price-data");
    const breakdownDiv = document.getElementById("price-breakdown");

    if (!priceData || !breakdownDiv) {
        console.error("Missing #price-data or #price-breakdown element.");
        return;
    }

    const pricePerDay = parseFloat(priceData.dataset.price);
    const deposit = parseFloat(priceData.dataset.deposit || "0");

    console.log(`pricePerDay: ${pricePerDay}, deposit: ${deposit}`);

    // DOM elements
    const startPickerEl = document.getElementById('start-date-picker-detail');
    const endPickerEl = document.getElementById('end-date-picker-detail');

    const startInput = document.getElementById("start-date-detail");
    const endInput = document.getElementById("end-date-detail");

    if (!startPickerEl || !endPickerEl || !startInput || !endInput) {
        console.warn("Missing date picker or input elements.");
        return;
    }

    // Initialize pickers
    new tempusDominus.TempusDominus(startPickerEl, {
        restrictions: { minDate: today },
        display: { components: { useTwentyfourHour: true, clock: false } },
        localization: { format: 'dd/MM/yyyy' }
    });

    new tempusDominus.TempusDominus(endPickerEl, {
        restrictions: { minDate: today },
        display: { components: { useTwentyfourHour: true, clock: false } },
        localization: { format: 'dd/MM/yyyy' }
    });

    // European date format (dd/mm/yyyy)
    function parseEuropeanDate(dateStr) {
        const [day, month, year] = dateStr.split('/');
        return new Date(`${year}-${month}-${day}`);
    }

    function calculate() {
        const startValue = startInput.value;
        const endValue = endInput.value;

        if (!startValue || !endValue) {
            breakdownDiv.innerHTML = `<p class="text-danger">Please select both dates.</p>`;
            return;
        }

        const start = parseEuropeanDate(startValue);
        const end = parseEuropeanDate(endValue);

        if (isNaN(start) || isNaN(end)) {
            breakdownDiv.innerHTML = `<p class="text-danger">Invalid date format.</p>`;
            return;
        }

        if (end <= start) {
            breakdownDiv.innerHTML = `<p class="text-danger">End date must be after start date.</p>`;
            return;
        }

        const msPerDay = 1000 * 60 * 60 * 24;
        const days = Math.ceil((end - start) / msPerDay);

        const basePrice = pricePerDay * days;
        const siteFee = 0.10 * basePrice;
        const total = basePrice + deposit + siteFee;

        breakdownDiv.innerHTML = `
            <p>Price per day: £${pricePerDay.toFixed(2)}</p>
            <p>Days: ${days}</p>
            <p>Deposit: £${deposit.toFixed(2)}</p>
            <p>Site Fee (10%): £${siteFee.toFixed(2)}</p>
            <hr>
            <p><strong>Total: £${total.toFixed(2)}</strong></p>
        `;

        console.log(`Calculated for ${days} days → £${total.toFixed(2)}`);
    }

    // Event listeners outside of calculate()
    startInput.addEventListener("change", calculate);
    endInput.addEventListener("change", calculate);
});
