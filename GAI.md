# GEN AI P5 Chatbot Feedback

### Example: Describe the bot UI Design that we had to use because of Maizey limitations. {: #Q01}
- [ ] Yum
- [x] Yuk

## Background

### How many ULCS courses has group member 1 taken including the current semester? {: #Q02}
FIXME
### How many ULCS courses has group member 2 taken including the current semester? {: #Q03}
FIXME (0 if only 1 group member)
### How many ULCS courses has group member 3 taken including the current semester? {: #Q04}
FIXME (0 if only 1-2 group members)

## General
### Approximately how many interactions did you have with the bot on project 5? {: #Q05}
- [ ] 0-3
- [x] 4-10
- [ ] 11-50
- [ ] 51+

### Mark all the topics where the bot was helpful: {: #Q06}
- [x] Spec questions
- [x] Design
- [ ] Debugging
- [ ] Conceptual questions
- [ ] Explaining test cases
- [ ] Setup / toolchain
- [ ] Implementation / code suggestions

### Would a similar bot be helpful for other projects? {: #Q07}
- [x] Yes
- [ ] No
- [ ] Unsure

### Our group used the bot instead of posting on Piazza {: #Q08}
- [ ] Never
- [ ] Rarely
- [x] Sometimes
- [ ] Often
- [ ] Always

### Our group used the bot instead of going to Office Hours {: #Q09}
- [ ] Never
- [x] Rarely
- [ ] Sometimes
- [ ] Often
- [ ] Always

### Using the bot instead of Piazza or Office Hours saved time {: #Q10}
- [x] Yes
- [ ] No
- [ ] Unsure

### The bot gave more helpful answers than ChatGPT {: #Q11}
#### (Reminder: Course policy permits the use of generative AI for projects (https://eecs485.org/syllabus.html#generative-ai-copilot-chatgpt))
- [ ] Never
- [ ] Rarely
- [x] Sometimes
- [ ] Often
- [ ] Always
- [ ] I did not use ChatGPT

### Given the choice, which bot would you prefer to use for project help? {: #Q12}
- [ ] EECS485 bot (Reducey)
- [ ] ChatGPT
- [x] Both
- [ ] Neither

### Please explain your answer to the previous question. {: #Q13}
Reducey is more good at spec or design questions and ChatGPT is better at general questions.

#### (Optional) Overall, do you have any feedback on the bot? {: #Q14}
FIXME

## Interaction 1
### Prompt {: #Q15}
can you help me design the inverted index pipeline?

### Response {: #Q16}
Certainly! To design an inverted index pipeline that calculates tf-idf and is comprised of sequential MapReduce programs, you'll have to follow a series of steps. I'll outline a basic design for your MapReduce pipeline to compute the tf-idf and construct an inverted index:



Calculate Total Number of Documents (Job 0)
Use map0.py to emit ('doc', 1) for each document. Then, reduce0.py sums up all values for key 'doc' to find the total number of documents in the corpus. The result of this job should be the total document count, which will be used in tf-idf calculations.



Data Preprocessing (Job 1)


a. map1.py: Processes each document to:



Convert text to lowercase.

Remove non-alphanumeric characters.

Remove stop words.


b. Emit (term, (docID, 1)) pairs for each remaining word occurrence.


c. reduce1.py: Sums the counts for (term, docID) pairs, emitting (term, (docID, count)).



Calculate Term Frequencies (Job 2)


Re-use or tweak map1.py or write map2.py depending on the preprocessing chosen:
Emit partial (term, (docID, count)) indices from mappers with term frequency (normalized counts within each document).


Write reduce2.py to simply pass along the data since the term frequency is a local document calculation.



Calculate Inverse Document Frequency (Job 3)


a. map3.py: For each (term, (docID, count)), emit (term, docID) to simply pass through but take the opportunity to also emit special keys that help in IDf calculation, for example (term, 'IDf_count') to count document frequency.


b. reduce3.py: Reducer receives per-term entries. Collect the doc frequency per term from 'IDf_count' messages and then compute and emit for each document term: (term, (docID, tf*IDf)).



Composite tf-idf Calculation (Job 3 continued)


Using the results from Job 3, you now have a situation where each machine handles one term. This makes it possible to finalize the calculation of tf-idf because the document frequency part of IDF will be a single value for all document instances of a term.



Sort and Partition Inverted Index (Job 4, 5,...)


Depending on specific performance requirements and reduce phase complexity, one or more jobs may be needed here to deal with sorting by term and docID, and then optionally partitioning the inverted index into segments. These extra jobs will accomplish the required sorting and segmenting.




Your pipeline script (pipeline.sh) will coordinate the execution of each MapReduce job using the madoop tool and manage the flow of output from one stage to the next, using each previous job's output as the next job's input. The inverse index will be one of the major results from this pipeline.


   a. map4.py and subsequent: Depending on your partitioning logic, tailor these map scripts to emit keys that cause terms to end up in the correct segment after reduce.


   b. reduce4.py and subsequent: Continues going through each (term, [(docID, tf-idf), (docID, tf-idf), ...]), sorting by docID and placing entries into one of the three segments.


Keep in mind that grouping between map and reduce is a natural occurrence in MapReduce frameworks, you leverage the shuffle and sort phase to ensure items with the same key (which changes depending on the job) arrive at the same reducer for processing. Any additional grouping needed (as mentioned for Job 4) may need special keys to facilitate this based on how your segmentation requirement is defined.


Remember that performance optimizations and avoiding data skews are also common issues when designing MapReduce jobs, so ensure your key space is well-distributed for parallel processing.



### Was this response helpful? {: #Q17}
- [x] Yes
- [ ] No

### To the best of your knowledge, did it answer your question correctly: {: #Q18}
- [x] Yes
- [ ] No
- [ ] Unsure

### (Optional) Anything else you want to tell us about this interaction? {: #Q19}
FIXME

## Interaction 2
### Prompt {: #Q20}
FIXME

### Response {: #Q21}
FIXME

### Was this response helpful? {: #Q22}
- [ ] Yes
- [ ] No

### To the best of your knowledge, did it answer your question correctly: {: #Q23}
- [ ] Yes
- [ ] No
- [ ] Unsure

### (Optional) Anything else you want to tell us about this interaction? {: #Q24}
FIXME

## Interaction 3
### Prompt {: #Q25}
FIXME

### Response {: #Q26}
FIXME

### Was this response helpful? {: #Q27}
- [ ] Yes
- [ ] No

### To the best of your knowledge, did it answer your question correctly: {: #Q28}
- [ ] Yes
- [ ] No
- [ ] Unsure

### (Optional) Anything else you want to tell us about this interaction? {: #Q29}
FIXME