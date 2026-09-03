# Day 04 — RAG Results

## Objective

The objective of this experiment was to test a Retrieval-Augmented Generation (RAG) system using a persisted Chroma vector database.

The system retrieves the most relevant chunks from the knowledge base and provides them to the LLM as context. The retriever was configured with `k=3`, meaning that the top 3 relevant chunks were retrieved for every question.

The system was tested with:

* 6 answerable questions based on the knowledge base.
* 2 deliberately unanswerable questions.
* Source citations in the generated answers.
* A strict refusal response when the required information was not present in the knowledge base.

---

## RAG Configuration

| Setting             | Value                       |
| ------------------- | --------------------------- |
| Vector database     | Chroma                      |
| Retriever           | Similarity search           |
| Top-k (`k`)         | 3                           |
| Knowledge base      | NovaBank training documents |
| Answering method    | LLM + retrieved context     |
| Source citation     | Filename in square brackets |
| Unknown information | Exact refusal message       |

---

## Results

| Question                                               | Sources retrieved                                                                | Answer OK? | Refused correctly? |
| ------------------------------------------------------ | -------------------------------------------------------------------------------- | ---------- | ------------------ |
| What are the steps to hotlist a card?                  | `debit_card_hotlisting_process.txt`, `net_banking_activation.txt`                | Yes        | N/A                |
| What is the daily limit for UPI transactions?          | `upi_limits_and_failures.txt`, `savings_account_faq.txt`                         | Yes        | N/A                |
| What documents are required for KYC?                   | `kyc_requirements.txt`, `grievance_escalation_matrix.txt`                        | Yes        | N/A                |
| What is the minimum tenure for a fixed deposit (FD)?   | `fixed_deposit_basics.txt`, `savings_account_faq.txt`                            | Yes        | N/A                |
| What are the eligibility criteria for a loan?          | `personal_loan_eligibility.txt`, `kyc_requirements.txt`                          | Yes        | N/A                |
| What are the different levels of grievance escalation? | `grievance_escalation_matrix.txt`, `upi_limits_and_failures.txt`                 | Yes        | N/A                |
| What is today's USD–INR exchange rate?                 | `upi_limits_and_failures.txt`, `savings_account_faq.txt`, `charges_schedule.txt` | N/A        | Yes                |
| What are the charges for the Platinum Sapphire card?   | `credit_card_types.txt`, `charges_schedule.txt`                                  | N/A        | Yes                |

---

## Detailed Results

### 1. Hotlisting a Card

**Question:**

> What are the steps to hotlist a card?

**Retrieved sources:**

1. `debit_card_hotlisting_process.txt`
2. `debit_card_hotlisting_process.txt`
3. `net_banking_activation.txt`

**Result:** Answered correctly.

The answer provided the hotlisting process, including opening the Cards section, selecting the affected debit card, choosing Hotlist Card, selecting a reason, and confirming the request.

The answer also cited `debit_card_hotlisting_process.txt` for the facts.

**Answer OK:** Yes

---

### 2. UPI Daily Limit

**Question:**

> What is the daily limit for UPI transactions?

**Retrieved sources:**

1. `upi_limits_and_failures.txt`
2. `upi_limits_and_failures.txt`
3. `savings_account_faq.txt`

**Result:** Answered correctly.

The system answered that the daily UPI transaction limit is ₹50,000 for NovaBank customers.

The answer cited `upi_limits_and_failures.txt`.

**Answer OK:** Yes

---

### 3. KYC Documents

**Question:**

> What documents are required for KYC?

**Retrieved sources:**

1. `kyc_requirements.txt`
2. `kyc_requirements.txt`
3. `grievance_escalation_matrix.txt`

**Result:** Answered correctly.

The answer identified the required identity document and address document when required. It also mentioned mobile-number verification.

The facts were cited using `kyc_requirements.txt`.

**Answer OK:** Yes

---

### 4. Fixed Deposit Minimum Tenure

**Question:**

> What is the minimum tenure for a fixed deposit (FD)?

**Retrieved sources:**

1. `fixed_deposit_basics.txt`
2. `fixed_deposit_basics.txt`
3. `savings_account_faq.txt`

**Result:** Answered correctly.

The system answered that the minimum tenure for a NovaBank fixed deposit is 3 months.

The answer cited `fixed_deposit_basics.txt`.

**Answer OK:** Yes

---

### 5. Loan Eligibility

**Question:**

> What are the eligibility criteria for a loan?

**Retrieved sources:**

1. `personal_loan_eligibility.txt`
2. `personal_loan_eligibility.txt`
3. `kyc_requirements.txt`

**Result:** Answered correctly.

The answer provided multiple eligibility conditions, including:

* Minimum applicant age of 21 years.
* Maximum applicant age of 60 years at loan maturity.
* Minimum monthly income of ₹30,000.
* At least 12 months of employment history.
* Required identity and income documents.
* Consideration of existing repayment obligations.
* Approval subject to internal eligibility assessment.

The answer cited `personal_loan_eligibility.txt` and `kyc_requirements.txt`.

**Answer OK:** Yes

---

### 6. Grievance Escalation Levels

**Question:**

> What are the different levels of grievance escalation?

**Retrieved sources:**

1. `grievance_escalation_matrix.txt`
2. `grievance_escalation_matrix.txt`
3. `upi_limits_and_failures.txt`

**Result:** Answered correctly.

The system identified three escalation levels:

* Level 1 — Customer support team.
* Level 2 — Service resolution team.
* Level 3 — Grievance officer.

The answer cited `grievance_escalation_matrix.txt`.

**Answer OK:** Yes

---

## 7. Deliberately Unanswerable — USD–INR Exchange Rate

**Question:**

> What is today's USD–INR exchange rate?

**Retrieved sources:**

1. `upi_limits_and_failures.txt`
2. `savings_account_faq.txt`
3. `charges_schedule.txt`

The retrieved context did not contain today's USD–INR exchange rate.

Instead of inventing an exchange rate, the system returned exactly:

> I don't have that information in my knowledge base — let me connect you to a human agent.

**Answer OK:** N/A

**Refused correctly:** Yes

---

## 8. Deliberately Unanswerable — Platinum Sapphire Card Charges

**Question:**

> What are the charges for the Platinum Sapphire card?

**Retrieved sources:**

1. `credit_card_types.txt`
2. `credit_card_types.txt`
3. `charges_schedule.txt`

The retrieved context did not contain the charges for the Platinum Sapphire card.

The system correctly returned exactly:

> I don't have that information in my knowledge base — let me connect you to a human agent.

**Answer OK:** N/A

**Refused correctly:** Yes

---

## Overall Observations

### Answerable Questions

All 6 answerable questions received answers based on information available in the knowledge base.

The generated answers included source filenames in square brackets, allowing the facts to be traced back to the retrieved documents.

### Unanswerable Questions

Both deliberately unanswerable questions were handled correctly.

The system did not attempt to guess:

* The current USD–INR exchange rate.
* The charges for the Platinum Sapphire card.

Instead, it returned the exact refusal message required by the task.

### Retrieval Debugging

Printing the retrieved sources was useful because it showed which documents were selected by the retriever for each question.

For example, the hotlisting question primarily retrieved:

`debit_card_hotlisting_process.txt`

while the loan question primarily retrieved:

`personal_loan_eligibility.txt`

This makes it possible to inspect whether the retriever is finding relevant documents before evaluating the generated answer.

---

## Comparison with Task 1.2 — Hallucination Experiment

In the earlier hallucination experiment, the LLM could potentially answer questions using its own pretrained knowledge even when the information was not available in the application's knowledge base.

With RAG, the system first retrieves relevant information from the knowledge base and uses that retrieved context to generate the answer.

The two deliberately unanswerable questions demonstrate the benefit of this approach.

Instead of generating a potentially incorrect exchange rate or inventing charges for the Platinum Sapphire card, the system refused to answer because the required information was not available in the knowledge base.

Therefore, retrieval provides an important grounding mechanism for the LLM.

---

## Conclusion

The RAG experiment was successful.

The system:

* Retrieved the top 3 relevant chunks for each question.
* Answered the 6 questions whose information existed in the knowledge base.
* Included source filename citations in the answers.
* Refused both questions whose information was not available.
* Did not invent an exchange rate or card charges.

The key lesson is that **RAG grounds an LLM's responses in an external knowledge base**, making it possible to provide source-backed answers and safely refuse questions when the required information is unavailable.

> **RAG = Retrieve relevant knowledge → Give it to the LLM as context → Generate a grounded answer.**
