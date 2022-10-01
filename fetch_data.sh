echo "Make sure you have set an env-variable GITLAB_TOKEN"

DL_URL = 

rm -rf ./fackel-mas* && rm -rf downloaded_data && rm -rf ./data_orig && rm -rf ./tmp
wget -O downloaded_data --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" https://gitlab.oeaw.ac.at/api/v4/projects/33/repository/archive?path=${DL_URL}
tar -xf downloaded_data && rm downloaded_data
mv fackel-master-* ./tmp
mv tmp/${DL_URL} data_orig && rm -rf ./tmp
