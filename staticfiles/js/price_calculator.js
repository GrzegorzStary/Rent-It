document.addEventListener("DOMContentLoaded", () => {
    console.log("Price calculator JS loaded");

    const startDateInput = document.getElementById("start-date");
    const endDateInput = document.getElementById("end-date");
    const priceData = document.getElementById("price-data");
    const breakdownDiv = document.getElementById("price-breakdown");

    if (!startDateInput || !endDateInput || !priceData || !breakdownDiv) {
        console.error("Missing one or more required elements");
        return;
    }

    const pricePerDay = parseFloat(priceData.dataset.price);
    const deposit = parseFloat(priceData.dataset.deposit);

    console.log(`pricePerDay: ${pricePerDay}, deposit: ${deposit}`);

    function calculate() {
        const startValue = startDateInput.value;
        const endValue = endDateInput.value;

        if (!startValue || !endValue) {
            breakdownDiv.innerHTML = `<p class="text-danger">Please select both dates.</p>`;
            return;
        }

        const start = new Date(startValue);
        const end = new Date(endValue);

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

        console.log(`Calculated for ${days} days: total = £${total.toFixed(2)}`);
    }

    startDateInput.addEventListener("change", calculate);
    endDateInput.addEventListener("change", calculate);
});
