
1.How an LLM Becomes a Helpful Assistant

An LLM starts with a huge amount of text collected from sources like books, websites, articles, and other internet text. The model cannot directly understand this text like a human does. First, the text is broken into smaller pieces called **tokens**. These tokens are converted into numbers so that a neural network can process them.

During **pretraining**, the model sees a lot of text and learns patterns in it. The basic task is to predict what token is likely to come next. For example, if the model sees “The sun rises in the”, it learns that “east” is a likely continuation. By doing this billions of times, the model learns grammar, facts, patterns, relationships between words, and different ways people communicate.

However, just predicting the next token does not automatically make the model a good assistant. The model then needs additional training to make its responses more useful and aligned with what humans expect. Techniques such as **instruction tuning and RLHF (Reinforcement Learning from Human Feedback)** help the model learn that it should follow instructions, be helpful, and produce responses that people prefer.

So, in simple terms, I think of the process like this:

Internet text → Tokens → Pretraining → Instruction tuning/RLHF → Helpful assistant


2.Why does an LLM hallucinate?

An LLM does not actually "know" things in the same way a human does. At its core, it is generating the next token based on patterns it learned during training. Because of this, it can sometimes produce an answer that sounds very confident and believable but is actually wrong.

For example, if the model does not have reliable information about a particular person or event, it may still generate an answer because it is trying to produce a likely continuation. This is called a **hallucination**.

I think the important point is that hallucination is not necessarily the model intentionally lying. It is more like the model generating a plausible answer without having a reliable way to verify whether the information is true.

3.What are reasoning models better at?

Normal language models are already good at generating and understanding text, but **reasoning models** are designed to spend more effort working through difficult problems before giving the final answer.

They are especially useful for tasks that require multiple steps, such as mathematics, coding, logic, planning, and complex problem solving. Instead of immediately jumping to an answer, they can work through intermediate reasoning and check different possibilities.

So I would describe the difference as:

Regular LLM → good at generating and understanding language

Reasoning model → better at solving complex, multi-step problems

Overall, my mental model is that an LLM first learns patterns from a huge amount of text, then gets trained to follow instructions and become more useful to humans. It is powerful because it has learned a huge number of patterns, but it can still make mistakes because generating a convincing answer is not the same as verifying that the answer is true. Reasoning models improve the ability to handle problems where simply predicting a quick answer is not enough.

Questions I Would Ask Another Trainee

1 If an LLM is mainly trained to predict the next token, how does additional training such as RLHF change its behavior from simply completing text to following instructions and acting like an assistant?

2 Why can an LLM give a confident and detailed answer even when the information is completely incorrect? Explain this using the difference between language generation and factual verification.

3 Suppose a normal LLM and a reasoning model are given a difficult multi-step programming problem. What makes the reasoning model potentially better at solving it, and does "reasoning" guarantee that its final answer will be correct??
