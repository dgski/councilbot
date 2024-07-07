<script>
    import { onMount } from 'svelte';

    /**
     * @type {any[]}
     */
    let meetings = []

    onMount(() => {
        fetch('https://councilbot-api.xantasoft.com/meetings?city_id=84245ba6-50f4-4ecb-9ebd-918c38a349ef')
            .then(res => res.json())
            .then(data => {
                meetings = data;
            });
    });

    let toString = (seconds) => {
        let date = new Date(seconds * 1000);
        return date.toDateString();
    }
</script>

<style>
    :global(body) {
        font-family: Arial, sans-serif;
        margin: 0;
    }

    #hero {
        background-color: #f4f4f4;
        color: #333;
        padding: 10px;
        padding-bottom: 80px;
        width: 100%;
        margin: 0 auto;
        padding-top: 80px;
    }

    #hero-content {
        width: 800px;
        margin-left: calc(50% - 400px);
        font-size: 1.5em;
    }

    #hero-question {
        font-size: 1.5em;
        font-weight: 800;
    }

    #main {
        width: 800px;
        margin: 0 auto;
        line-height: 1.5em;
        margin-top: 2em;
    }

    @media (max-width: 800px) {
        #hero {
            padding: 0px;
            padding-top: 20px;
            padding-bottom: 20px;
        }
        #hero-content {
            width: calc(100% - 40px);
            margin-left: 0;
            padding-left: 20px;
            padding-right: 20px;
            font-size: 1em;
        }

        #main {
            width: calc(100% - 40px);
            padding: 20px;
            font-size: 1em;
            margin-top: 0;
        }
    }
</style>

<div id="hero">
    <div id="hero-content">
        <p id="hero-question">Do you know what the Waterloo City Council is doing with your tax money and city?</p>
        <p><b>councilbot</b> gives you a seat at the table by using AI to summarize hours of meetings.</p>
    </div>
</div>
<div id="main">
    <div id="main-content">
        {#each meetings as meeting}
            <div class="meeting">
                <h3><a href="/meeting/{meeting.meeting_id}">{toString(meeting.meeting_date)}</a></h3>
                <ul>
                    {#each meeting.meeting_decisions as decision}
                        <li>{decision}</li>
                    {/each}
                </ul>
            </div>
        {/each}
    </div>
</div>
