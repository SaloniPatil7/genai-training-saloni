# Day 5 — Multi-Query Retrieval Comparison

## Before / After Results

| Question                  | Day 4 Retrieval                                                                  | Day 5 Retrieval                                                                          | Answer Quality                                               | Refusal Still Works? |
| ------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------- |
| Hotlist a card            | `debit_card_hotlisting_process.txt`, `net_banking_activation.txt`                | `debit_card_hotlisting_process.txt`, `kyc_requirements.txt`, `credit_card_types.txt`     | Day 4 Correct / Day 5 Failed (`User Safety: safe`)           | N/A                  |
| UPI daily limit           | `upi_limits_and_failures.txt`, `savings_account_faq.txt`                         | `upi_limits_and_failures.txt`, `savings_account_faq.txt`, `fixed_deposit_basics.txt`     | Correct in both                                              | N/A                  |
| KYC documents             | `kyc_requirements.txt`, `grievance_escalation_matrix.txt`                        | `kyc_requirements.txt`, `grievance_escalation_matrix.txt`                                | Correct in both                                              | N/A                  |
| FD minimum tenure         | `fixed_deposit_basics.txt`, `savings_account_faq.txt`                            | `fixed_deposit_basics.txt`, `savings_account_faq.txt`                                    | Day 4 Correct / Day 5 Failed (`User Safety: safe`)           | N/A                  |
| Loan eligibility          | `personal_loan_eligibility.txt`, `kyc_requirements.txt`                          | `personal_loan_eligibility.txt`, `kyc_requirements.txt`                                  | Day 4 Correct / Day 5 Failed (`User Safety: safe`)           | N/A                  |
| Grievance escalation      | `grievance_escalation_matrix.txt`, `upi_limits_and_failures.txt`                 | `grievance_escalation_matrix.txt`, `upi_limits_and_failures.txt`, `charges_schedule.txt` | Correct in both                                              | N/A                  |
| USD–INR exchange rate     | `upi_limits_and_failures.txt`, `savings_account_faq.txt`, `charges_schedule.txt` | Same sources                                                                             | Day 4 refused correctly / Day 5 returned safety response     | **No**               |
| Platinum Sapphire charges | `credit_card_types.txt`, `charges_schedule.txt`                                  | Same sources                                                                             | Day 4 refused correctly / Day 5 returned `User Safety: safe` | **No**               |

## Conclusion

Multi-query retrieval helped generate different versions of questions and generally retrieved the correct primary documents.

For straightforward questions, it increased API calls and sometimes retrieved additional irrelevant documents without improving the answer.

In production, I would enable multi-query retrieval selectively for ambiguous queries and only after fixing JSON parsing and refusal handling.
