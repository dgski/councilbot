<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import Meeting from '../../../Meeting.svelte';
    import Nav from '../../../Nav.svelte';

    /**
     * @type {any[]}
     */
    let meetings = []
    let council_name = "";
    let city_id = undefined;

    page.subscribe(value => {
        city_id = value.params.id;

        fetch(`https://councilbot-api.xantasoft.com/meetings?city_id=${value.params.id}`)
            .then(res => res.json())
            .then(data => {
                meetings = data;
            });
        
        fetch(`https://councilbot-api.xantasoft.com/city/${value.params.id}`)
            .then(res => res.json())
            .then(data => {
                council_name = data.city_name;
            });
    });
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
<Nav selection={city_id} />
<div id="hero">
    <div id="hero-content">
        <p id="hero-question">Do you know what the {council_name} Council is doing with your tax money and city?</p>
        <p><b>councilbot</b> gives you a seat at the table by using AI to summarize hours of meetings.</p>
    </div>
</div>
<div id="main">
    <div id="main-content">
        {#each meetings as meeting}
            <Meeting {meeting} />
        {/each}
    </div>
</div>
