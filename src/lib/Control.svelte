<script>
  //import { invoke } from '@tauri-apps/api/tauri'
  //import { listen } from '@tauri-apps/api/event'
  import { onMount, createEventDispatcher } from 'svelte'
  import { fade } from 'svelte/transition'

  //import Fa from 'svelte-fa'
  //import { faArrowRotateLeft } from '@fortawesome/free-solid-svg-icons'

  // Components

  const dispatch = createEventDispatcher()


  let controlView = false
  onMount(()=> controlView = true)

  const stopGroundSeg = () => {
    console.log("stop groundseg")
    // prompt for sudo password
  }

  const restartGroundSeg = () => {
    console.log("restart groundseg")
    // prompt for sudo password
  }

</script>

{#if controlView}
  <div class="control-wrapper"
    in:fade={{duration:200, delay: 200}}
    out:fade={{duration:160}}>
    <div class="control-buttons">
      <button class="ctrl-btn stop" on:click={stopGroundSeg}>
        Stop GroundSeg
      </button>
      <button class="ctrl-btn restart" on:click={restartGroundSeg}>
        Restart GroundSeg
      </button>
    </div>
    <a 
      class="pop-open"
      target="_blank"
      href="http://hostname.local">
      Open GroundSeg WebUI
    </a>
  </div>
{/if}

<style>
  .control-wrapper {
    margin: 80px;
    display: flex;
    flex-direction: column;
    gap: 40px;
  }
  .control-buttons {
    display: flex; 
    gap: 12px;
  }
  .ctrl-btn {
    flex: 1;
    border: solid 1px white;
    border-radius: 12px;
    font-size: 14px;
    background: none;
    font-family: inherit;
    line-height: 48px
  }
  .ctrl-btn:active {
    opacity: .6;
  }
  .stop {
    color: red;
    border-color: red;
  }
  .restart {
    color: orange;
    border-color: orange;
  }
  .stop:hover {
    color: white;
    background: red;
    cursor: pointer;
  }
  .restart:hover {
    color: white;
    background: orange;
    cursor: pointer;
  }
  .pop-open {
    text-decoration: none;
    border: solid 1px lime;
    font-size: 16px;
    border-radius: 16px;
    line-height: 62px;
    color: lime;
  }
  .pop-open:hover {
    color: white;
    background: lime;
  }
  .pop-open:active {
    opacity: .6;
  }

</style>
