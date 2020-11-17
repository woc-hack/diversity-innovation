# Is there a diversity-innovation paradox in open-source software (OSS)?

A replication of [The Diversity–Innovation Paradox in Science](https://www.pnas.org/content/117/17/9284#sec-4)

## Members
- José Bayoán Santiago Calderón
- Lavínia Paganini
- Sam Yong
- Sophie Qiu

## What is the diversity paradox?
Diversity breeds innovation, yet underrepresented groups that diversify organizations have less successful careers within them.

## Research Questions
1. How do we detect scientific innovations of repositories?
2. Are diverse groups ([in terms of gender and tenure](https://cmustrudel.github.io/papers/chi15.pdf)) more likely to generate innovations at Open Source Communities? 
3. Are the innovations of diverse groups more often adopted and rewarded?

## Variables

### Novelty

We first construct cooccurance graphs of pypi libraries.
We remove spurious links (due to chance, combinations of extremely rare terms, etc.) by computing a significance score for each link: the log-odds ratio of the probability of link occurrence (computed over all extracted concepts and all documents in the corpus) to the probability of each component concept term occurring independently over the corpus (37, detailed in the SI Appendix)

### Impactful Novelty

We count the total number of times projects in following years use the links first introduced by a prior project, normalized by the number of new links. We use the resulting metric, uptake per new link, to quantify the average scientific impact of an individual project.

### Distal Novelty

### Careers

How long they stay on GH

### Average of diversity measures of the teams they worked for
