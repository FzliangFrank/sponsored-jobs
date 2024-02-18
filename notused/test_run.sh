# from the dropdown at the top of Cloud Console:
export GCLOUD_PROJECT="visa-sponsor-uk" 
# from Step 2.2 above:
export REPO="ukvisa-docker-repo"
# the region you chose in Step 2.4:
export REGION="europe-west2"
# whatever you want to call this image:
export IMAGE="sponsor-image:tag3"

# use the region you chose above here in the URL:
export IMAGE_TAG=${REGION}-docker.pkg.dev/$GCLOUD_PROJECT/$REPO/$IMAGE

echo $IMAGE_TAG
# Build the image:
docker build -t ${IMAGE_TAG} --platform linux/x86_64 .
docker run ${IMAGE_TAG}