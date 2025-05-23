Trying to combine deep and shallow strategies in the DDFs


For configuration files, using convention that the first season a DDF is visible at all is season=0. Thus, season 0 (and season 9) are often partial seasons.


ocean1.dat:  First attempt at making a combination good for SNe and good for AGN strategy.

ocean2.dat:  Turned down u and y sequences

ocean3.dat:  Increase deep in EDFS_a so they are a full deep on each field.
             change u-3, y-4 for shallow, 15,20 for deep
             trying g2, r2, i2, z2 for shallow

ocean4.dat:  turning the nightly sequences down a bit so they are even/odd in shallow seasons.


Put in a detailer to try and reduce filter thrashing. 
Fixed a bug that was preventing even/odd from working properly. Put in a throttle so 
we wouldn't try to schedule more sequences than there were potenital days in a season.
Added a 10th season since the 0th season can exist, but not have valid timeslots.


Now getting many more observations than expected on the deep seasons. 
Before, had 278254 scheduled observations. Now at 275888. But I have 282585 executing? and had 183960 before. Is the detailer somehow preventing things from being marked as observed? That would be strange.
Looks like all the flush lengths were set to 2. Try again with the short ones set to the shorter flush length.


We are now quite a bit slower generating the DDF list, so we probably want to spin that off and have a saved script of planned DDF observations.


Make a nested dither detailer, so all the DDFs can be on a single script for gathering filters.

