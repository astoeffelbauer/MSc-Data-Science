# first make this file executable using chmod +x <filename>
# run this script using ./<filename>

# make directories
mkdir -p data/dblp
mkdir -p data/yelp

# download the data
wget -P data/dblp https://www.dropbox.com/sh/89xbpcjl4oq0j4w/AABrktOFt6ZSD4iRpjERe5Nca/dblp/author-large.txt
gsutil cp data/dblp/author-large.txt gs://st446-mybucket/data/ # copy to bucket
wget -P data/yelp https://www.dropbox.com/sh/89xbpcjl4oq0j4w/AAC4_qW_wKyGIXXYZOwZC-Wia/Yelp/yelp_academic_dataset_user.json
