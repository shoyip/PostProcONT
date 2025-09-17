* demultiplexing  
* for input and output  
  * blast with variant library  
  * filter out bitscores lower than 400  
  * filter out reads with lengths that are small or long  
  * count  
  * filter out counts that are too low  
  * bootstrap sample, meaning resample with repicking  
  * compute mean and error from bootstrap

1. There are many gzipped FASTQ amounting to subsets of reads. We take those FASTQ files, convert them to FASTA and in one unique file.  
2. We can see the **histogram of read lengths**. Depending on this, we can choose to throw away reads that are too short (fragments) or too long (chymeras).  
3. Once this filtering has been carried out, we can match the reads to the library sequences. There are several options: among them minimap2 and BLAST. I was using minimap2, which is supposed to be purposefully written for fast assignment of sequencing reads to library variants. However, in order to have sufficient statistics I had to tweak the program in order to allow for more errors to be made in the matching process. The parameters of this matching though are not entirely clear to me. On the other side, BLAST is not made for library variant assignment. Meaning it takes more time to do the same thing. However it provides an important additional information: for each match an e-value and a bitscore is provided. We can then use the distribution of bitscores and choose only the matches of the bulk.  
4. Make a database of the variant library.  
   	makeblastdb \-in ./library\_variants.fasta \-dbtype nucl \-out variant\_db  
5. BLAST the reads against the variant library.  
   	blastn \-query input.fasta \-db variant\_db \-out assignments\_input.tsv \-outfmt 6  
6. Now plot the **histogram of the bitscores**. Choose only the matches such that the bitscore is in the range of the central bulk of the distribution.  
7. So now we have a table that assigns each read to each each variant. Per variant, as a way of checking that we are doing the right thing, we can **plot the sequences with a color code** per nucleotide.  
8. Now we can aggregate and count, per each variant, how many reads we have in input and in output.  
9. We choose the member of the library variant which is the reference variant of the given substrate. For example if we are assaying the activity of variants against AAPF, the reference will be the bovine chymotrypsin CTRA\_BOVIN.  
10. In order to have an estimate of the error over the matches we perform a bootstrapping. This is what happens: given the current assignment of reads to variants, we re-extract the same number of reads with replacement. We do this, say, Nb times with Nb=50. At the end, we will have for each of the Nb runs, a number of reads that each variant has. We can do the mean and the standard deviation, and these become the final values. However, instead of extracting 50 times, which is a slow process, we can think of it as a multinomial process and directly start from the frequencies. Then we can draw from the mutlinomial distribution, Nb times and this can be more than 50 (for example we do 1000 and it is still very fast). At the end we will have a mean and standard deviation for each variant.