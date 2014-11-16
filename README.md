## <h1>React: Drug Safety in Your Pocket</h1>

![React](http://i.imgur.com/LVCxUoM.png)<br>
**Team: scikit_hammertime**<br>
==================================<br>
Jake Beard: jake at minnow dot io <br>
Anjney Midha: anjney at stanford dot edu<br>
Ankit Kumar: ankitk at stanford dot edu<br>
Jay Hack: jhack at stanford dot edu<br>
Ross Lazerowitz: rosslazer at gmail dot com<br>

Bayes Impact Hackathon 2014<br>
==================================<br>
**The Problem:**<br>
- 100,000 Americans die each year due to known drug side effect
- Existing tools for users to search for adverse drug interactions are clunky, database level query interfaces
- Existing tools are limited to reported drug events - which are severely prone to underreporting

**Solution:**<br>
- We use a distributed representation of the AERS ( Federal Drug Adverse Event Reporting System) dataset classified by the RxNorm hierarchy, using neural networks to predict novel interactions for pairs of drugs that do not have a historical interaction record

==================================<br>
**acknowledgements:**<br>

**Libraries used:**<br>
- Word2vec (https://code.google.com/p/word2vec/)

**Papers Referenced:**<br>
- http://www.tatonetti.com/papers/CPT_2011_Tatonetti.pdf
- http://jamia.bmj.com/content/early/2013/02/05/amiajnl-2012-001482
