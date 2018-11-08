# Subset-Sum-Solver


## Problem Description

Camping groups for a music festival are to be sorted into different sections so there is minimal overflow to the center lane. Each group can be placed in any section but not split between sections.

This is a variation of the subset sum problem which is a common coding interview problem at Google and Amazon.


## Algorithium Description

There is no efficient solution to this problem so sections were filled by randomly selecting groups. 

The sections must be filled from biggest to smallest in order to minimize the variance that results from filling later sections.

The smallest and biggest possible number of groups per section were calculated to limit the number of tries per section.

The difference in the group area and section area must be within a certain error or the groups are rejected.
If after a certain number of tries, a set of groups that fits within the error is not found, the allowed error is incrementally increased until it does.

This script repeats the process of finding a solution 10 times. It then chooses the best solution based on the smallest range of errors for the sections and writes it to a file titled solutions.cvs in the same directory as the script.

The probability of finding the best solution is then

1-(1-P)^n

where P is the probabily of finding the best solution after one run and n is the number of runs.

A probability of 70% of finding the best solution from just one run yields over 99.99% probabilty of finding the best solution after 10 runs.

## Additional Files

Part of the original data I was given is included. The camp leader names were changed to first 2 letters of first name and last name to protect their identities.
The camp leader name was used as the identifier for each group in the python script because some group names had unrecognizable characters.

I wrote and included a VBA script to convert the solution to a more excel friendly format. 
The camp leader names can then be index matched to the get the camp group names.

EFF 2018 06-13-18 Group Camp Wk-1 is the final layout of all the camp groups, which was posted to the Electric Forest Facebook page before the festival. Solutions generated by the python script will probably not be the same due to randomization.



