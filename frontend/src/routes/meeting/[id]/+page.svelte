<script>
// @ts-nocheck

    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import NavStatic from '../../../NavStatic.svelte';

    /**
     * @type {{ meeting_date: any; meeting_keywords: any; meeting_segments: any; meeting_decisions: any; } | null}
     */
    let data = null;
    let city_name = "";
    let city_id = "";

    // Get id from URL
    page.subscribe(value => {
        fetch(`https://councilbot-api.xantasoft.com/meeting/${value.params.id}`)
            .then(res => res.json())
            .then(incoming => {
                console.log(incoming);
                data = incoming;
                city_id = data.city_id;
            });
    });

    let toString = (seconds) => {
        let minutes = Math.floor(seconds / 60);
        let remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }
</script>

<style>
    :global(body) {
        font-family: Arial, sans-serif;
        margin: 0;
    }

    #main {
        width: 800px;
        margin: 0 auto;
        line-height: 1.5em;
        padding-top: 50px;
    }

    h1 {
        font-size: 2em;
        margin-bottom: 2em;
    }

    h3 {
        font-size: 1.5em;
        margin-top: 1em;
    }

    @media (max-width: 800px) {
        #main {
            width: calc(100% - 40px);
            padding: 20px;
            font-size: 1em;
            margin-top: 0;
        }
    }
</style>
<NavStatic {city_id} />
<div id="main">
    {#if data}
        <h1>{new Date(data.meeting_date * 1000).toDateString()}</h1>
        <h3>Decisions</h3>
        <ul>
            {#each data.meeting_decisions as decision}
                <li>{decision}</li>
            {/each}
        </ul>
        <h3>Segments</h3>
        <ul>
            {#each data.meeting_segments as segment}
                <li><b>{toString(segment.start_time_seconds)} - {toString(segment.end_time_seconds)}</b>: {segment.text}</li>
            {/each}
        </ul>
        <h3>Keywords</h3>
        <p>
            {#each data.meeting_keywords as keyword}
                {keyword},&nbsp;
            {/each}
        </p>
        <h3>Summary</h3>
        <p>
            {data.meeting_summary ? data.meeting_summary : "No summary available"}
        </p>
        <h3>Video Link</h3>
        <a href={data.meeting_link}>{data.meeting_link}</a>
    {:else}
        <h1>No ID</h1>
    {/if}
</div>