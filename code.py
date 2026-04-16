import re
import pandas as pd

CURRENCY_SYMBOLS = {
    '$': 'USD',
    '€': 'EUR',
    '£': 'GBP',
    '₹': 'INR',
    '₨': 'PKR'
}

def normalize_currency(value, target_currency='USD'):
    if pd.isna(value):
        return None
    
    value = str(value).strip()
    
    symbol = None
    for s in CURRENCY_SYMBOLS:
        if s in value:
            symbol = s
            break
    
    currency = CURRENCY_SYMBOLS.get(symbol, target_currency)
    
    cleaned = re.sub(r'[^\d.,-]', '', value)
    
    if cleaned.count(',') > 0 and cleaned.count('.') > 0:
        if cleaned.find(',') < cleaned.find('.'):
            cleaned = cleaned.replace(',', '')
        else:
            cleaned = cleaned.replace('.', '').replace(',', '.')
    else:
        cleaned = cleaned.replace(',', '')
    
    try:
        amount = float(cleaned)
    except:
        return None
    
    return {
        'original': value,
        'amount': amount,
        'currency': currency,
        'normalized': f"{currency} {amount:.2f}"
    }

def normalize_dataframe(df, column):
    return df[column].apply(normalize_currency)

data = pd.DataFrame({
    'price': ['$1,200.50', '€2.345,70', '£850', '₨ 15,000']
})

result = normalize_dataframe(data, 'price')
print(result.tolist())
