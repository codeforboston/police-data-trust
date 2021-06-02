## Background

### Challenges of Police Data

Data relating to police misconduct is highly decentralized. Oftentimes, data on police misconduct may not exist. If it exists, it may be unavailable to the public. If it is available to the public, it may only be available through a process of time-consuming and expensive freedom of information requests, and the responses to these requests are only available to the requester and not the public at large.

Among those datasets available to the public, each data source reporting on police misconduct may be different from other data sources reporting on the same thing. Here are just a few of the problems:

- **The data being collected may differ:** Some may be reporting on killings by police officers, others may be reporting on officially filed complaints.

- **The method of collection may differ:** Some data sources aggregate media articles; others take from officially filed complaints through a police department; others may even collect their own data submitted by citizens.

- **The schemas of the data may differ:** There are lots of ways to record all the events that occur within a single police interaction with a member of the public, and data aggregators pick and choose what data they believe is salient in a format they prefer.

    - An example: Complaint filing systems differ based on different departments. For example, many complaint systems have encodings such as “improper use of force” or “illegal search.” These encoding systems may differ from department to department.

### Affected Stakeholders

This ecosystem of incomplete and inconsistent data creates problems for lawyers, activists, researchers, and concerned citizens who want to understand the dynamics of policing in America.

- 👩‍⚖️ **Lawyers** representing victims of police misconduct would have an easier time opening “[Monell cases](https://www.lawfareblog.com/municipal-liability-police-misconduct-lawsuits)” if they have access to a comprehensive record of data.

- 💪 **Activists** do not have access to accurate and comprehensive data regarding police misconduct in their communities.

- 🧑‍🔬 **Researchers** can’t conduct good research without good data.

- 👪 **Concerned citizens** will not have a good idea of what is happening in their local community or whether a police officer in their community has a history of complaints against them.

### Value in Aggregation and a Common Specification

There are many organizations that help address this problem and collect their own data (some of them are listed further down in the document), but they collect data in their own ways with their own schemas. Combining this data is extremely hard, but would be valuable for a lot of reasons. Some examples:

- Different datasets may contain distinct incidents concerning a single police officer. Aggregating as much data as possible about a single police officer’s history of misconduct assists lawyers in knowing whether a Monell claim is worth pursuing.

- A police officer with a history of alleged misconduct may be hired by different police departments over the course of their career. At the moment, this is hard to track for multiple reasons. (Some of these problems would not be immediately solved by our project.) One of the many problems involved with recording this information is inconsistency of data across multiple sources; another problem is the lack of any major attempt to aggregate all the data that exists.

## Our Mission

The Police Data Trust is a project through [Code For Boston](https://www.codeforboston.org/) with various partner organizations, namely [The Tubman Project](https://tubmanproject.com). This project is trying to solve this problem of data in multiple places reporting on different incidents in different ways.

Our end goal is a web application with a public facing API that is queryable by members of the public to provide information from various sources. The web application would also ingest data in a consistent way across these sources. Because of how this project would connect various stakeholders, the specification design and its live implementation are major parts of the end product, as opposed to being just implementation details.

## Public Police Data

Police Data Trust is not the first project to tackle this problem. If you want to understand police data in the United States, a good place to start are datasets compiled by organizations that already go through the hard work of collecting, cleaning, aggregating, and presenting that data to the public.

- **[Chicago Police Data Trust](https://cpdp.co/)** (via [Invisible Institute](https://invisible.institute/)) - Data received from FOIAs and discovery from a few legal cases involving police officers.

    - _Invisible Institute has a Github [here](https://github.com/invinst/)._

- **[Mapping Police Violence](https://mappingpoliceviolence.org/)** (via Campaign Zero) - Curated dataset of nationwide police killings. It appears they collect all of their data based on media coverage.

    - _Campaign Zero has a Github [here](https://github.com/campaignzero)._

- **[Texas Justice Initiative](https://texasjusticeinitiative.org/)** - Collects police shooting and deaths in custody data for Texas.

- **[Fatal Encounters](https://fatalencounters.org/)** - Similar to Mapping Police Violence.

- **[Measures for Justice](https://measuresforjustice.org/)** - Various state by state metrics of criminal justice outcomes.

- **[OpenPolice](https://openpolice.org/)** - Online platform for submissions of police complaints.
