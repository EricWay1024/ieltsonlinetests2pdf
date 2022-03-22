# Genarating PDF files for IELTS reading mock tests on ieltsonlinetests.com

ieltsonlinetests.com is a free website for IELTS mock tests. In case you need to generate PDF files for the reading tests there (so that you can print them out or take notes using your iPad), this repo would be useful.

If you just want all the PDF files, please check the releases of this repo.

If you want to run the script yourself:

Install dependencies:

```
pip install requests beautifulsoup4 pdfkit
sudo apt-get install wkhtmltopdf
```

Run:

```
python3 main.py
```

You can modify the parameter to call `fetch_name_list` to adjust to your needs. A `test_name` is what follows `https://ieltsonlinetests.com/` in the test url, e.g. `ielts-mock-test-2022-february-reading-practice-test-1`, and you call `fetch_name_list` with a list of `test_name`s. The resultant PDFs will be saved to `OUTPUT_DIR`, default as `./res`.

The original website has the copyright of the tests.