# councilbot

Checks for new council meetings videos, downloads their transcripts and extracts summaries, decisions and segments using AI. Makes this data available via an API and webpage.

- **Backend**:
    - FastAPI for API.
    - Any SQL database for database (Currently; Postgres). Pretty much used as a Document store
    - Claude API with Instructor for AI analysis.
    - Config is json object string supplied as base64-encoded environment variable with the name **CONFIG** (Sample in backend directory).
    - Checking for new meetings and performing analysis is triggered via a job endpoint: `/jobs/download`. This is protected with a token which is confirmed as legitimate by an API request to an instance of `cronservice`.
- **Frontend**:
    - Run of the mill Svelte Kit application. Only supports City of Waterloo at this time.

## TODO

- [] Better frontend UI/UX.
- [] Support multiple cities in frontend (Or decide to have everything separate).
- [] Email subscription mechanism?
- [] Search Functionality