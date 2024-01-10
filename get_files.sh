authorisation_header="Authorization: Bearer $(cat github_api_token.txt)"

curl_github_api()
{
  curl --request GET --url "$1" --header "$authorisation_header"
}

master_commits_url=https://api.github.com/repos/bots-hosting-account/psdwbot/commits/master

commit_url=$(curl_github_api $master_commits_url | cat | grep '"tree":' -a2 | tail -1)
commit_url=${commit_url:14:-1}

dir_url=$(curl_github_api $commit_url | grep '"path": "bot"' -a4 | tail -1)
dir_url=${dir_url:14:-1}

files=$(curl_github_api "$dir_url?recursive=1" | grep '"type": "blob"' -B2 | grep '"path":')
while IFS= read -r filename
do
  filename=${filename:15:-2}
  curl https://raw.githubusercontent.com/bots-hosting-account/psdwbot/master/bot/$filename -o bot/$filename
done <<< "$files"
