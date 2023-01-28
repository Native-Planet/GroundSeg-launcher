<script>
  import { invoke } from '@tauri-apps/api/tauri'
  import { onMount } from 'svelte'
  import { fade } from 'svelte/transition'
  import SlideShow from '$lib/SlideShow.svelte'

  let installView = false, installing = false
  let status = 'nothing to see here'

  const installGroundSeg = async () => {
    installing = true
    status = await invoke('install')
  }

  onMount(()=> installView = true)
</script>

{#if installView}
  <div in:fade={{duration:200, delay: 160}} out:fade={{duration:200}} class="wrapper">
    <img class="logo" src="nplogo.svg" alt="Native Planet Logo"/>
    <SlideShow />
    {#if !installing}
      <button
        on:click={installGroundSeg}
        class="wrapper">
        Install GroundSeg
      </button>
    {:else}
      <div 
        class="installing"
        in:fade={{duration:400, delay: 160}}>
      {status}
      </div>
    {/if}
  </div>
{/if}

<style>
  button {
    margin-top: 28px;
    font-family: inherit;
    border-radius: 16px;
    border: solid 1px white;
    color: inherit;
    background: none;
    width: 240px;
    line-height: 40px;
  }
  button:hover {
    background: var(--action-color);
    border-color: var(--action-color);
    cursor: pointer;
  }
  button:active {
    opacity: 0.6;
  }

</style>
