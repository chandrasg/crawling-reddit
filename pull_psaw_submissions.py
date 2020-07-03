import requests

url = "https://api.pushshift.io/reddit/search/submission"
subreddit_to_pull_submissions = "lonely" #MODIFY 
output_file = 'data.json' #MODIFY 

def crawl_page(subreddit: str, last_page = None):
  """Crawl a page of results from a given subreddit.

  :param subreddit: The subreddit to crawl.
  :param last_page: The last downloaded page.

  :return: A page or results.
  """
  params = {"subreddit": subreddit, "size": 500, "sort": "desc", "sort_type": "created_utc"}
  if last_page is not None:
    if len(last_page) > 0:
      # resume from where we left at the last page
      params["before"] = last_page[-1]["created_utc"]
    else:
      # the last page was empty, we are past the last page
      return []
  results = requests.get(url, params)
  if not results.ok:
    # something wrong happened
    raise Exception("Server returned status code {}".format(results.status_code))
  return results.json()["data"]

import time

def crawl_subreddit(subreddit, max_submissions = 100000):
  """
  Crawl submissions from a subreddit.

  :param subreddit: The subreddit to crawl.
  :param max_submissions: The maximum number of submissions to download.

  :return: A list of submissions.
  """
  submissions = []
  last_page = None
  while last_page != [] and len(submissions) < max_submissions:
    last_page = crawl_page(subreddit, last_page)
    submissions += last_page
    time.sleep(3)
  return submissions[:max_submissions]

lastest_submissions = crawl_subreddit(subreddit_to_pull_submissions)

import json
with open(output_file, 'w') as outfile:
    json.dump(lastest_submissions, outfile)