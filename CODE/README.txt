This directory contains code that does the full BOXCOXROX data pipeline including importing data, running models
and producing the final csv, images and HTML files.

To run the pipeline execute this command:

python boxcoxrox_pipeline.py

Note:  This process will create the following files in the same directory as the program above:
pets.db:                    The full SQLite3 database of pet products and reviews
products.gz                 The downloaded compressed archive of pet products
products.json               The decompressed archive of products
reviews.gz                  The downloaded compressed archive of pet product reviews
reviews.json                The decompressed archive of reviews
categories.csv              The DFTI extracted mapping of products to product categories
pets_sentiment.csv          The Vader analyzed sentiment of pet reviews
pets_sentiment_grouped.csv  The aggregated sentiment analysis of reviews by on product ASIN
rankings.csv                The aggregated ranking (stars) of products based on review stars
product_validation.csv      All products that were able to be validated against Amazon's website


Once the pipeline program has completed, several files need to be copied over to the visualization app to view the
results.  (Note:  a copy of the files have been included with the application in the archive, so it is not necessary
to do this step.)

1.  Copy the products_prepped.csv to the /docs of the visualization app.  This file is the pipeline output file.
2.  Copy all the .png files into the visualization app /docs/img directory.
3.  Copy the products_prepped.csv file into the visualization /docs directory.


====================== LICENSE ======================

MIT License

Copyright 2021 Georgia Institute of Technology CSE 6242 Spring Semester Team 017 Team BoxCoxRox
N. Abramson, M. Kunnen, K. Matisko, K. McCanless, M. Porter and S. Tay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.