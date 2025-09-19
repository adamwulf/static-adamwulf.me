+++
title = "PikaPods and Umami for website metrics"
date = "2025-09-18T20:27:10+0000"
slug = "pikapods-and-umami-for-website-metrics"
type = "post"
+++

For the past many years, Muse has used [Fathom](https://usefathom.com/) for web analytics, and they've done a fantastic job. I highly recommend Fathom if you're looking for privacy-first analytics without any hassle. I don't mind a little hassle, especially if that hassle can save me $20, so I went looking for a free/cheaper alternative.

For the past few months, I've been on a cost-saving binge, and after cutting costs on the larger fruit, my eyes turned to my Fathom account. I started where any reasonable person would start: I asked Claude's deep research to find me alternatives for Fathom analytics. My constraints - it had to be cheaper than $15/mo and had to be privacy focused. I did not want to move to Google Analytics.

## Umami - simple open source analytics

Claude came back with a huge list that I don't remember, because the one service on that list I do remember is [Umami](https://umami.is/). They have a paid cloud option available, along with a generous free tier, and most importantly are [completely open source](https://github.com/umami-software/umami). They have the same privacy mindset that Fathom has, and they also guarantee access to all of the raw event and session data for export so that it's easy to migrate elsewhere. Great!

## Converting Fathom to Umami-compatible format

I rushed to sign up, I got all of my sites configured, and was excited to get my Fathom data imported into Umami. Unfortunately, Fathom doesn't export your full event data, which is what Umami needs. Fathom only provides daily summaries, but not per-visit event data.

To solve this, I created a [Fathom-to-Umami](https://github.com/adamwulf/fathom-to-umami) data converter, which generates synthetic event data that would have the same summary statistics that Fathom gives you. Claude was a great buddy, doing lots of the heavy lifting here, and by the end I was able to generate a massive csv file for each of my Fathom websites.

To generate the synthetic data, I unzipped the Fathom export to a museapp.com folder in my new tool's folder, and then ran:

``` bash
python3 fathom_to_umami_converter.py museapp.com
```

This created a single `output/museapp.com.csv` file that contained synthetic event data that exactly matched the Fathom hourly summaries.

## Importing Fathom into Umami cloud

I signed up for an Umami pro account, where they provide the service of bespoke data import, and they were able to process my event data into my Umami account - perfect!

So at this point, I've gone from $15/mo Fathom to $20/mo Umami pro account. However, now that my data was in Umami, I could more easily move to a self-hosted option.

This is when I found [PikaPods](https://www.pikapods.com/) which as a one-click Umami install. They charge based on usage, so for 25% of a single CPU, and 512Mb of memory, I could self-host an Umami install for $1.48/mo!

## Moving from cloud Umami to self-hosted Umami

Since PikaPods runs the open source version of Umami, I was expecting it to have one-click import/export for data, but surprisingly no! Getting the data from Umami cloud was easy, they do offer a 1 click export, so that was simple.

To import into my PikaPod, I turned on database access which opened a Adminer web-based mysql admin panel. To import the Umami data, I found this [open source import script](https://github.com/zouloux/umami-import-csv). Unfortunately, this imports into Postgres instead of Mysql, so Claude and I [hacked a fork together that imported into Mysql](https://github.com/adamwulf/umami-import-csv/tree/feature/mysql) instead.

Unfortunately, the PikaPod didn't export the mysql port directly, so I couldn't import straight into the Mysql database. Instead, I modified the script to batch 100 inserts into a single `INSERT` query, and then batch 1500 of those queries into a single `.sql` file with the following command:


``` bash
node --max-old-space-size=8192 --expose-gc index.js
```

For Muse, this resulted in 10 files each about ~40Mb. I could use the Adminer web interface to import these sql files.

## Import complete!

At this point, i have 100% of my data in my PikaPod running Umami. I've turned off my $20/mo Umami cloud account, and I now have web analytics for $1.48/mo. Not bad!
