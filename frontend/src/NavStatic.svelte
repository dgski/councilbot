<script>
    import { onMount } from "svelte";

    export let city_id = "";
    let city_name = "";

    $: fetch_city_info(city_id);

    let fetch_city_info = (city_id) => {
        fetch(`https://councilbot-api.xantasoft.com/city/${city_id}`)
            .then(res => res.json())
            .then(incoming => {
                city_name = incoming.city_name;
            });
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
            <div id="link">
                <a href="/city/{city_id}">{city_name}</a>
            </div>
        </div>
    </div>
</div>