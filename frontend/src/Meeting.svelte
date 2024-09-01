<script>
    import keyword_extractor from "keyword-extractor";

    export let meeting;

    let toString = (seconds) => {
        let date = new Date(seconds * 1000);
        return date.toDateString();
    }

    let getKeywords = (text) => {
        text = text.join(" ");
        return keyword_extractor.extract(
            text ,{
            language:"english",
            return_changed_case:true,
            remove_duplicates: true,
            return_max_ngrams: 3,
            remove_digits: true,
            return_chained_words: true
        });
    }
</script>

<style>
    .keyword {
        font-size: 0.9em;
        font-weight: 800;
        background-color: #f4f4f4;
        color: #333;
        border-radius: 10px;
        padding: 8px;
        margin: 5px;
        margin-left: 0;
        display: inline-block;
    }

    @media (max-width: 800px) {
        .keyword {
            font-size: 0.8em;
            padding: 5px;
            margin: 3px;
        }
    }
</style>

<div class="meeting">
    <h2><a href="/meeting/{meeting.meeting_id}">{toString(meeting.meeting_date)}</a></h2>
        {#each getKeywords(meeting.meeting_decisions) as decision}
            <span class="keyword">{decision}</span>
        {/each}
</div>