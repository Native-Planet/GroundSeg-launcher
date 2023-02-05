<script>
  import { onMount} from 'svelte'
  import { fade } from 'svelte/transition'
  let logoView = false
  onMount(()=> logoView = true)
</script>

{#if logoView}
<img in:fade={{duration:200, delay: 200}}
     class="logo" 
     src="nplogo.svg" 
     alt="Native Planet Logo"
/>
{/if}
