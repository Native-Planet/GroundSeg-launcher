<script>
  // Svelte
  import { onMount, createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  export let installing

  const dispatch = createEventDispatcher()

</script>

{#if installing}
  insert installing loading bar here
{:else}
  <button class="install-btn"
    on:click={()=> dispatch('click')}>
    Start GroundSeg
  </button>
{/if}
