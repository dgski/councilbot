<script>
    import { onMount } from "svelte";

    export let selection;
    let cities = []

    onMount(() => {
        fetch(`https://councilbot-api.xantasoft.com/cities`)
            .then(res => res.json())
            .then(data => {
                cities = data;
            });
    });
    
    let update = (e) => {
        selection = e.target.value;
        window.location.href = `/city/${selection}`;
    }
</script>

<style>
    #nav {
        width: 100%;
        margin: 0 auto;
        text-align: center;
        background-color: #f4f4f4;
        color: #333;
    }

    #nav-center {
        display: inline-block;
    }

    #nav-flex {
        display: flex;
        padding: 10px;
    }

    #logo {
        font-weight: 800;
        margin-right: 20px;
    }
</style>

<div id="nav">
    <div id="nav-center">
        <div id="nav-flex">
            <div id="logo">councilbot</div>
            <div id="dropdown">
                <select bind:value={selection} on:change={update}>
                    {#each cities as city}
                        <option value={city.city_id}>{city.city_name}</option>
                    {/each}
                </select>
            </div>
        </div>
    </div>
</div>