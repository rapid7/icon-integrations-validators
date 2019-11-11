CHANGELOG="$(tr -d '\n' < README.md | grep -o '\*[^\*]*' | head -n 1)"
VERSION="$(echo "${CHANGELOG}" | grep -o '[0-9]\+.[0-9]\+.[0-9]\+')"
CHANGELOG="$(echo "${CHANGELOG}" | cut -d "-" -f 2)"
curl -X POST -H "X-Api-Key: 73731a49-9906-4a3b-949e-059cac78bcc9" -d "{\"version\": \"${VERSION}\", \"changelog\": \"${CHANGELOG}\"}" https://us.api.insight.rapid7.com/connect/v1/workflows/aab1fd1c-eceb-40df-a5cd-038a3903cf48/events/execute