## How to run on Docker

1. Dowload this repository as a zip file and extract the zip file OR clone the repository
2. Change working directory to the unzipped directory
```
cd receipt-processor-challenge/
```
3. Build the container image 
```
docker build -t receipt-processor-challenge .
```
4. Start the container using the docker run command
```
docker run -dp 5000:5000 receipt-processor-challenge
```
5. Test the deployed APIs, ```/receipts/process``` and ```/receipts/{receipt_id}/points```
