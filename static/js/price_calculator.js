document.addEventListener("DOMContentLoaded", () => {
    console.log("Price calculator JS loaded (Tempus Dominus)");

    const today = new Date();
    const priceData = document.getElementById("price-data");
    const breakdownDiv = document.getElementById("price-breakdown");

    const pricePerDay = parseFloat(priceData.dataset.price);
    const deposit = parseFloat(priceData.dataset.deposit);

    console.log(`pricePerDay: ${pricePerDay}, deposit: ${deposit}`);

    const startDatePicker = new tempusDominus.TempusDominus(
        document.getElementById('start-date-picker'),
        {
            restrictions: {
                minDate: today,
                disabledDates: unavailableDates
            },
            display: { components: { useTwentyfourHour: true, clock: false } },
            localization: {
                format: 'dd/MM/yyyy'
            }
        }
    );

    const endDatePicker = new tempusDominus.TempusDominus(
        document.getElementById('end-date-picker'),
        {
            restrictions: {
                minDate: today,
                disabledDates: unavailableDates
            },
            display: { components: { useTwentyfourHour: true, clock: false } },
            localization: {
                format: 'dd/MM/yyyy'
            }
        }
    );

    function parseEuropeanDate(dateStr) {
        const [day, month, year] = dateStr.split('/');
        return new Date(`${year}-${month}-${day}`);
    }

    function calculate() {
        const startValue = document.getElementById("start-date").value;
        const endValue = document.getElementById("end-date").value;

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
        const siteFee = 0.05 * basePrice;
        const total = basePrice + deposit + siteFee;

        breakdownDiv.innerHTML = `
            <p>Price per day: £${pricePerDay.toFixed(2)}</p>
            <p>Days: ${days}</p>
            <p>Deposit: £${deposit.toFixed(2)}</p>
            <p>Site Fee (5%): £${siteFee.toFixed(2)}</p>
            <hr>
            <p><strong>Total: £${total.toFixed(2)}</strong></p>
        `;

        console.log(`Calculated for ${days} days → £${total.toFixed(2)}`);
    }

    document.getElementById("start-date").addEventListener("change", calculate);
    document.getElementById("end-date").addEventListener("change", calculate);
});
