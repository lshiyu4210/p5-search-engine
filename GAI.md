# GEN AI P5 Chatbot Feedback

### Example: Describe the bot UI Design that we had to use because of Maizey limitations. {: #Q01}
- [ ] Yum
- [x] Yuk

## Background

### How many ULCS courses has group member 1 taken including the current semester? {: #Q02}
3
### How many ULCS courses has group member 2 taken including the current semester? {: #Q03}
3
### How many ULCS courses has group member 3 taken including the current semester? {: #Q04}
0

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
how can I fix the code style error of this:
R0914: Too many local variables (17/15) (too-many-locals), I felt that it's hard to cut down any more local variables

### Response {: #Q21}
Hello there! When you encounter the error "R0914: Too many local variables (17/15) (too-many-locals)" with a linter, it does mean that your function has more local variables than recommended by the style guide or the rules configured for the project. To resolve this, consider the following strategies:


Refactor into Smaller Functions: If possible, break down the function into smaller functions where each does a part of what the original function did. This better adheres to the single responsibility principle and makes your code more readable and maintainable.


Use Data Structures: Group related variables into a dictionary, list, set, or a custom object. This allows you to pass around and manage one or a few composite objects instead of many individual variables.


Global Variables: If some of the variables are meant to be constant or shared across functions, consider making them global. However, use globals judiciously as they can make the code harder to understand and maintain.


Object-Oriented Programming (OOP): Perhaps you might employ a class to encapsulate some of the state if it represents a cohesive module of data.



Here is a rough example of how you might refactor a function using (1) and (2) for too many local variables:

Before Refactoring:

def process_data():
    var1 = ...
    var2 = ...
    # ...
    var17 = ...
    # Function body that uses all 17 variables

After Refactoring:

def process_part1(data):
    # Logic for part 1
    pass

def process_part2(data):
    # Logic for part 2
    pass

def process_data():
    data = {
        'var1': ...,
        'var2': ...,
        # Put as many variables as make sense together
    }
    process_part1(data)
    process_part2(data)
    # Continue with reduced number of variables

Remaining careful to keep the refactored code readable and maintainable. If these modifications seem inconvenient or disrupt your logic significantly, then consider consulting with the course supervisor to see if there's a threshold adjustment that can be made for the linter in the context of your projects.

Hope that helps, and keep up the good work! If you need anything else, feel free to ask.

### Was this response helpful? {: #Q22}
- [x] Yes
- [ ] No

### To the best of your knowledge, did it answer your question correctly: {: #Q23}
- [y] Yes
- [ ] No
- [ ] Unsure

### (Optional) Anything else you want to tell us about this interaction? {: #Q24}
FIXME

## Interaction 3
### Prompt {: #Q25}
Does this project need to worry about runtime and memory issue


### Response {: #Q26}
Based on the information provided, it seems like there isn't a strict requirement to optimize for time and memory for project 5 (p5), as long as your code doesn't hang during tests or automated grading (AG). However, you should not store the entire input in any single data structure within a map or reduce stage, as it can cause your program to time out during tests. The primary focus should be on passing input through the stages rather than on time/memory optimization.

To answer your question directly: The project does not need to explicitly worry about runtime and memory issues, aside from ensuring that your code executes without timing out or hanging. Always aim for clean, efficiently structured code, but you don't need to employ advanced optimization techniques for p5. Just make sure to follow best practices to prevent unnecessary waste of resources, which might indirectly help you to avoid performance-related issues.

### Was this response helpful? {: #Q27}
- [x] Yes
- [ ] No

### To the best of your knowledge, did it answer your question correctly: {: #Q28}
- [y] Yes
- [ ] No
- [ ] Unsure

### (Optional) Anything else you want to tell us about this interaction? {: #Q29}
FIXME