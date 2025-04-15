Time out to make sure new IntRounded isn't slower, and gives same results


on branch tickets/SP-2156:
python baseline.py --survey_length 60 --verbose

Flushed 1552 observations from queue for being stale
Completed 23809 observations
ran in 3 min = 0.1 hours
Writing results to  baseline_v4.3.1_0yrs.db

on main
Flushed 1552 observations from queue for being stale
Completed 23806 observations
ran in 3 min = 0.1 hours
Writing results to  baseline_v4.3.1_0yrs.db

Looks like no speed issue, but we have changed the evaluation sometimes.
Let's check if cross platform on the branch is still the same

