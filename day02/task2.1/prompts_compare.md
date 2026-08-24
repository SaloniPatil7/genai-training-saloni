# Task 2.1 — Prompt Comparison

## Prompt A — Simple

The model produced a detailed summary containing the issue, timeline, impact, complaint history, and reference number.

**Customer Complaint Summary**

* **Issue:** Unable to update the registered mobile number despite two branch visits to the MG Road branch.
* **Timeline:**

  * **Tuesday:** Waited 45 minutes but was turned away due to a system outage.
  * **Thursday:** Returned and was informed that a specific form was required, which had not been provided during the previous visit.
* **Impact:** UPI transactions have been failing since the 3rd, and the EMI payment due on the 10th is at risk.
* **History:** This is the third formal complaint regarding the issue.
* **Reference:** **CMP-88213**

## Prompt B — Structured

The structured prompt produced a concise and consistent output using predefined fields:

**issue:** Mobile number update failed due to system downtime and a missing form, causing UPI failures since the 3rd and putting the EMI payment due on the 10th at risk; this is the third complaint (Ref: CMP-88213).

**severity:** high

**requested_action:** Complete the mobile number update to restore UPI functionality and enable the EMI payment.

## Observation

The structured prompt made the output more predictable because it explicitly defined the required fields and the expected severity value. It also encouraged the model to use only the information provided in the complaint.

As a result, Prompt B produces a more consistent and machine-readable output, making it easier for a downstream program to parse, validate, and process. Prompt A, on the other hand, provides a more detailed and human-readable summary.