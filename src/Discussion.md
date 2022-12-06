Team: Majed Salah, Sammy El-Sherif

# Experimental Results

## Gather Data
* After running each version of the program, namely _Sequential_, _Threaded_ and _Process_, we collect runtimes and
store those in the following table, for posterior discussion. 

| Program Type  | Many Small Files | Few Large Files |
|---------------|-----------------:|----------------:|
| Sequential    |            0.592 |          59.112 |
| Thread-based  |            0.699 |          54.112 |
| Process-based |           23.388 |          19.676 |
 | Shared        |            0.469 |          57.840 |

## Discussion
* Discuss with your team these questions:

**A) Did the Multi-threaded program (thread-based) improve the performance of the processing?** 

*If yes, explain why? If no, explain what do you think is the cause of that behavior*

*Your Answer here*

For the "Many Small Files" the Multi-threaded program did not improve performance, but for 
the "Few Large Files" it did. This is because the overhead of starting so many new threads for small
processing batches is greater than the speedup provided by multi-threading, especially for a language like
python with the GIL issue.



**B) Did the Multi-Processing program (process-based) improve the performance of the processing?** 

*If yes, explain why? If no, explain what do you think is the cause of that behavior*

*Your Answer here*

For the "Many Small Files", the multi-processing program was far slower. But, for the "Few Large Files"
it ran much faster. Similar to the threading implementation above, starting so many new processes for small processing
loads incurs a large overhead cost that is not worth it for the amount of work each process is doing.

However, for the large files it is much more worth it since the overhead is relatively small compared to the amount of
work being done and since each file takes so much longer to process, having it so that they can be done concurrently
provides a large speed increase.


**C) Which are the tradeoffs of achieving better performance?** 

*Your Answer here*

_ Data integrity with handling multiple threads/processes accessing or changing the same data

_ Larger memory costs since concurrent approaches require separate memory spaces and interpreters in the case of
processes

_ More work by the programmer to implement parallel execution techniques, handling locks and adequately splitting work
among workers

**EC) Advantages and disadvantages of Shared Dictionary vs. the Thread-Based implementation**

*Your Answer here*

The time spent processing "Many Small Files" was a whole 0.2s faster for the Shared Dictionary implementation. 
But, on the other hand the standard Thread-Based program beat the Shared Dictionary version by a whole 5 seconds.

The advantage of the Shared Dictionary implementation is that you are left with a single data structure
that you can then use for whatever you so please. In the standard Thread-Based implementation, each file has a subset
of word from the entire data set read in, so all of you computed data is seperated making it hard to handle.

The disadvantage of the Shared Dictionary implementation is that there is overhead incurred from the 
lock within the increment_key_by_value function. In the standard Thread-Based program, there was no waiting 
time for data updating, and therefore it completed faster. 

A disadvantage for the Standard Thread-Based program is that is incurs overhead from the amount of times 
that is has to perform I/O operations since it is writing to many files. 

After analyzing our results, we are able to see that for the "Many Small Files" data set, the Shared Dictionary 
approach is quite a bit faster since it does not incur the overhead of having to write to all the different
files that the Standard Thread-Based approach suffers from. But, when we use the "Large Files" data set,
the Standard Thread-Based approach wins since it does not have to incur all the overhead from the lock and there are much
less separate files to write to.
_
