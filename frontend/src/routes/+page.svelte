// Redirect to page
<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    onMount(() => {
        goto('/city/84245ba6-50f4-4ecb-9ebd-918c38a349ef');
    });
</script>