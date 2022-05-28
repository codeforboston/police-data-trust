FILE DESCRIPTIONS:

* measures.csv

This table has 4 columns that list the identification code, name, format, and
calculation method for each of the measures.  This information corresponds to
the measure_id column on the state data table.

* locations-al.csv

This table has 3 columns that list the identification code, location type, and
name of all the locations in the selected state.  This information corresponds
to the location_id column on the state data table.

* filters.csv

This table has 2 columns that provide the identification code and description
for each of the filter groups.  This information corresponds to the filter_id
column on the state data table.

* data-<Time Period>-al.csv

This is a table listing the data displayed in the Data Portal broken down by
measure, filter, and location.  The name of the file refers to the time period
the data is generated against.  The missing column lists how many cases were
unknown/missing on the variable used for the numerator, and the
missing_percentage displays that as a percentage out of the denominator.  The
status column describes whether there are any warnings or availability notes
associated with that measure/filter/location combination.  For percentage
measures, the denominator column shows the pool of cases for that measure, the
numerator column shows the number of cases that meet the criteria for the
measure, and the value column displays the calculation.  For median measures,
the value column shows the median, and the count, sum, sum_squares, minimum,
maximum, standard_devation, and average columns provide the descriptive
statistics for that measure/filter/location.

* legal-context-<Time Period>-al.txt

This is a summary of information about state statutory laws relevant to our 
measures.  These data were collected by applying a standard set of questions
to the laws that were in place during the measurement period indicated in the 
file name.  The file lists the name of each measure, followed by an outline
of the legal context relevant to that measure.

USER NOTES:

* A STARTING POINT

Our Measures are meant to be a starting point for a conversation about the
criminal justice system that addresses what’s working well and what needs
further attention. The aim is to create transparency.

* ADULT CRIMINAL CASES

Our system measures only the performance of counties on the processing of adult
criminal cases. Therefore, we do not measure how juvenile, family, civil, and
other cases may fare. Nonetheless, our Measures can be filtered by the age group
of the defendant, including those under 18 (juvenile defendants who were waived
to adult court).

* FILTERS

Our Measures can be filtered by defendant characteristics (race/ethnicity,
indigent status, sex, and age) and by case characteristics (offense type,
offense severity, court type, attorney type, and drug type--only for
drug-specific Measures). We encourage users to explore the Measures using these
filters. Some filters calculate disparities between two groups. However, we
don't test the statistical significance of such disparities. 

* DATA QUALITY

Measures for Justice (MFJ) works with data extracted from administrative case
management systems. These data were originally collected by the sources for the
purpose of tracking the processing of individual cases and not necessarily for
the purpose of measurement. Nevertheless, they are suitable for measurement
provided they are handled correctly. Often, these data are reliable. Just as
often, they can be entered incorrectly or not at all, may be subject to errors
at any stage of the recording and collection process, and may not be
standardized across counties. MFJ has taken steps to account and adjust for
these problems but cannot correct entirely for errors in data entry. For these
reasons, and because jurisdictions use a variety of calculation methods, we
encourage examining overall patterns instead of exact percentages when comparing
to reports produced by local agencies.

* CASE DEFINITION

Criminal justice agencies use different methods to record cases. Some
jurisdictions file all charges against a defendant under the same docket number
and sometimes they do so even when the charges stemmed from different incidents.
Others file each charge under separate docket numbers even when the charges are
for the same incident. To standardize the definition of case across
jurisdictions, we count all charges associated with the same defendant that were
filed (or referred for prosecution, in the case of declinations) on the same
date as a single case. We assume that when a prosecutor files multiple charges
together, even when they originated from different incidents, they intend to
resolve these charges simultaneously. Since the focus of our Measures is case
processing, not case clearance, we believe this approach is currently the best
way to standardize case definition across jurisdictions.

* CASE SERIOUSNESS

Because cases often involve multiple charges of differing severities, we define
cases based on the most serious charge, according to the state's offense
severity classification, that was present at each stage of the case processing,
respectively referral, filing, and conviction.

* CAUSATION

MFJ’s research is descriptive and does not, by definition, tell us why things
happen. As such, we do not test hypotheses about the reasons for the patterns
the data reveal. When our Measures show differences between states, counties, or
groups (e.g., in medians, percentages, or rates), we make no claim about the
reasons for these differences.

* DISPARITIES

MFJ uses a Relative Rate Index (RRI) to assess disparities on case processing
outcomes between white defendants and defendants of color, males and females,
and indigent and non-indigent defendants. The RRI compares how two groups fare
on the same outcome by dividing the results of one group by those of the other.
An RRI equal to 1 indicates that there is no disparity in outcomes between the
two groups. Disparities are not calculated when there are fewer than four cases
in the denominator of the rate for either group. We also test the statistical
and substantive significance of disparities. Disparities that are neither
statistically nor substantively significant are suppressed from publication.

* STATISTICAL SIGNIFICANCE

MFJ estimates confidence intervals to test whether the disparity in outcomes for
the two groups is beyond what could be expected by random chance. In this sense,
statistical significance provides information about the precision and certainty
of the measurement. When a disparity is statistically significant, we can be 95%
confident that the rates for the two groups are unequal. Statistically
significant disparities are noted with an asterisk (*).

* SUBSTANTIVE SIGNIFICANCE

Because statistical significance is affected by sample size, MFJ also evaluates
whether the size of the disparity merits attention irrespective of statistical
significance. When a disparity is substantively significant, this means it is
large enough to warrant attention. Disparities equal to or greater than 1.05 are
considered substantively significant, and attempts should be made to understand
and address them.

* CONTEXT

Each Measure sheds light on a corner of a local criminal justice system, but to
evaluate the health of that system in a more comprehensive way, all available
Measures should be assessed together and interpreted with county context in
mind.

* COUNTY

We measure criminal justice performance at the county level because it is
usually at this level that charging, disposition, and sentencing decisions are
made.

* MISSINGNESS

The maximum permissible percentage of cases with missing values for any given
measure is 10 percent. Performance measures for counties with more than 10
percent of cases missing values in the numerator or in the pool to calculate the
median are suppressed from publication. In addition, performance measures for
counties with more than 5 percent and up to 10 percent of cases with missing
values display a “high missing rate” warning.

* MISSINGNESS BIAS

MFJ uses statistical simulations to estimate the amount of bias that may result
from missing data. The bias depends both on the percentage of missing data and
the actual value of the measure being estimated. For example, in a county where
the pretrial diversion rate is low (e.g., 3%) and there is a considerable
proportion of cases missing data (e.g., 7%), the estimate of the pretrial
diversion rate could be inaccurate. Bias is estimated as a function of the
sample mean and the percentage of missing data. Whenever the sample mean and the
percentage of missing data suggest a level of bias greater than 5 percent, MFJ
suppresses the data from publication.

* MORE DATA

MFJ continues to seek out more data—especially law enforcement data—as part of
our effort to measure all corners of the criminal justice system.

* TIMELINE

If you’ve given us data and don’t see them represented in the Portal yet, it’s
because we are still working on them to ensure accuracy. Thank you for your
participation and patience.

* PORTAL UPDATES

We provide a complete history of portal updates that allows you to track when
data changes or new data have been released to the portal or when new versions
of the portal are made available. 
