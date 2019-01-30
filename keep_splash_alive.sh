until docker run -p 8050:8050 scrapinghub/splash --max-timeout 3600; do
  echo "Retrying";
done 
