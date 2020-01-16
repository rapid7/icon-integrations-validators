CHANGELOG="$(tr -d '\n' < README.md | grep -o '\*[^\*]*' | head -n 1)"
VERSION="$(echo "${CHANGELOG}" | grep -o '[0-9]\+.[0-9]\+.[0-9]\+')"
CHANGELOG="$(echo "${CHANGELOG}" | cut -d "-" -f 2)"


curl -X POST -H "X-Api-Key: ${ICON_TRIGGER_WORKFLOW_API_KEY}" \
-d "{\"version\": \"${VERSION}\", \"changelog\": \"${CHANGELOG}\"}" \
https://us.api.insight.rapid7.com/connect/v1/workflows/${ICON_TRIGGER_WORKFLOW_ID}/events/execute
