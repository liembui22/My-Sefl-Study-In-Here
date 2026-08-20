const currencyFirstEl = document.getElementById('currency-first');
const worthFirstEl = document.getElementById('worth-first');
const currencySecondEl = document.getElementById('currency-second');
const worthSecondEl = document.getElementById('worth-second');
const exchangeRateEl = document.getElementById('exchange-rate');

function updateExchangeRate() {
    fetch(`https://v6.exchangerate-api.com/v6/262e67e0b813ff446170b7bc/latest/${currencyFirstEl.value}`)
    .then((res) => res.json())
    .then((data) => {
        const rate = data.conversion_rates[currencySecondEl.value];
        exchangeRateEl.innerText = `1 ${currencyFirstEl.value} = ${rate} ${currencySecondEl.value}`;
        worthSecondEl.value = (worthFirstEl.value * rate).toFixed(2);
    });
}

currencyFirstEl.addEventListener('change', updateExchangeRate);
currencySecondEl.addEventListener('change', updateExchangeRate);
worthFirstEl.addEventListener('input', updateExchangeRate);
worthSecondEl.addEventListener('input', updateExchangeRate);
