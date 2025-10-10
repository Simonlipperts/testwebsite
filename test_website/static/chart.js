console.log('Dit script werkt!')

let tradingViewWidget;
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing TradingView widget...');
    
    new TradingView.widget({
        container_id: "chart",
        autosize: true,
        symbol: "NASDAQ:AAPL", // Voorbeeld: Apple aandelen
        interval: "15", // Tijdframe: 15 minuten
        timezone: "Etc/UTC",
        theme: "light",
        style: "1", // Candlestick stijl
        locale: "en",
        toolbar_bg: "#1e1e1e",
        enable_publishing: false,
        hide_side_toolbar: false,
        allow_symbol_change: true,
        show_popup_button: true,
        popup_width: "1000",
        popup_height: "650",
    });
});



function getCurrentTicker() {
    // controleren of het widget object bestaat en of de opties beschikbaar zijn
    if (window.tradingViewWidget && window.tradingViewWidget.options) {
        // haalt de ticker direct uit de widget
        console.log(window.tradingViewWidget.options.symbol)
        return window.tradingViewWidget.options.symbol;
    }
    CSSConditionRule.log('Widget not ready!')
    return "NASDAQ:AAPL"; // fallback
}

function startQuotes() {
    const ticker = getCurrentTicker();
    console.log(`Starting quotes for: ${ticker}`);

    // Stuur ticker direct naar Python script
    fetch('/start-quotes', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ticker: ticker})
    });
}
// Button om quotes te starten
document.getElementById('start-quotes-btn').addEventListener('click', startQuotes);
