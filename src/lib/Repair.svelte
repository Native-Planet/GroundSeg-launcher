<script>
  // Svelte
  import { onMount} from 'svelte'
  import { fade } from 'svelte/transition'

  // Components
  import SlideShow from '$lib/SlideShow.svelte'

  let installView = false
  onMount(()=> installView = true)

</script>
{#if installView}
  <div in:fade={{duration:200, delay: 200}} out:fade={{duration:160}}>
    <SlideShow />
    <slot />
  </div>
{/if}
