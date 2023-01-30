<script>
  // Tauri
  import { invoke } from '@tauri-apps/api/tauri'

  // Svelte
  import { onMount, onDestroy, createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  const dispatch = createEventDispatcher()

  let launchingView = false
  onMount(()=> {
    launchingView = true
    checkWebui()
  })
  onDestroy(()=> launchingView = false)
  const checkWebui = async () => {
    if (launchingView) {
      let res = await invoke('check_webui')
      if (res == "error")
        setTimeout(checkWebui,1000)
      else {
        dispatch('page',res)
      }
    }
  }

</script>

{#if launchingView}
  <div class="launching-wrapper"
    in:fade={{duration:200, delay: 200}}
    out:fade={{duration:160}}>
    <div class="loader"></div>
    <img class="launching-logo" src="nplogo.svg" />
    <div class="launching-text">Launching GroundSeg</div>
  </div>
{/if}

<style>
  .launching-wrapper {
    position: relative;
    margin: auto;
    width: 240px;
    height: 180px;
    margin-top: 120px;
  }
  .launching-logo {
    position: absolute;
    top: 37px;
    width: 60px;
    left: 90px;
    animation: breathe 4s linear infinite;
  }
  .launching-text {
    position: absolute;
    bottom: 0;
    text-align: center;
    width: inherit;
  }
  .loader {
    position: absolute;
    border: 4px solid transparent;
    border-top: 4px solid white;
    border-bottom: 4px solid white;
    border-radius: 50%;
    width: 110px;
    height: 110px;
    top: 0;
    left: 65px;
    animation: spin 1.5s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  @keyframes breathe {
    0% {opacity: 1}
    30% {opacity: 1}
    45% {opacity: 0}
    55% {opacity: 0}
    70% {opacity: 1}
    100% {opacity: 1}
  }
</style>
