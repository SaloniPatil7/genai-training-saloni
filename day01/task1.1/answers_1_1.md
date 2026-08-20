# Task 1.1 — See Tokens With Your Own Eyes

## Token counts

| Sentence | Language | Tokens |
|---|---|---|
| I want to block my debit card immediately | English | 8 |
| मेरा डेबिट कार्ड खो गया है | Hindi | 9 |
| Mera card kho gaya hai, please block karo | Hinglish | 10 |
| Account number 3021 4456 8890 1123 | Numeric | 14 |
| Please help me reset my net banking password | English (mine) | 8 |
| मुझे अपना नेट बैंकिंग पासवर्ड रीसेट करना है | Hindi (mine) | 14 |

## (a) Why did the Hindi sentence produce more tokens than the English one?

The tokenizer's vocabulary was built mostly from English (and other Latin-script)
text, so common English words often map to a single token. Hindi, written in
Devanagari script, appeared far less often during vocabulary training, so the
tokenizer has fewer efficient multi-character merges for it — it often falls
back to smaller fragments per character. That's why my Hindi sentence (~7 words)
took 14 tokens while a similarly-sized English sentence took 8.

## (b) What does that imply for cost and latency of a multilingual bot?

Since providers bill per token, not per word, serving Hindi-speaking customers
costs more for the same conversation length purely because of the script —
not because the conversation is more complex. It also means slower responses,
since more tokens have to be generated for the same amount of meaning.

## (c) What happened to the account number — why did it split the way it did?

It took 14 tokens for what looks like "one number" — digit sequences aren't
merged into single tokens; they're typically chunked into small groups
(1-3 digits each). So the model doesn't see the account number as one clean
unit, which matters for tasks like redaction or exact-match validation.

## Cost exercise

Pricing used: gpt-4o-mini — $0.15 per 1,000,000 input tokens
(checked on openai.com/api/pricing — verify the date/price before submitting)

Average tokens per utterance from my samples: (8+9+10+14+8+14)/6 ≈ **10.5 tokens**

50,000 utterances/day × 10.5 tokens = 525,000 tokens/day
525,000 × 30 days = 15,750,000 tokens/month
15,750,000 / 1,000,000 × $0.15 = $2.36/month (input only)