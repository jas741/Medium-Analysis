# medium
Medium Network Analysis

Taking a look at followers/followees network on medium without API. 

`MediumSampler.py` takes a list of followers of @mediumstaff (by scrolling down from the top a specified number of times) and then randomly samples until it finds 30 that have a specified minimum number followed (~40) and maximum number of followers (~30k). (popular non-institutional blogger range). 

`DevotedFanTester.py` takes the csv output of `MediumSampler.py` as input, and finds, for each source listed there, how many of the people they follow have no posts, and clap only for posts of the source.  A measure of vanity.
